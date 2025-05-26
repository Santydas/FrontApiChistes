from dash import Dash, dcc, html, callback_context
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import requests


BASE_URL = "https://apichistesdef-production.up.railway.app/chistesyfrases"


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Gestión de Chistes"), width={"size": 6, "offset": 3}),
    ], className="my-4"),

    dbc.Row([
        dbc.Col(dcc.Input(id='joke_id', type='text', placeholder="ID del chiste"), width=4),
        dbc.Col(dbc.Button("Obtener Chiste", id='get_joke_button', color="primary"), width=2),
    ], className="my-3"),

    dbc.Row([
        dbc.Col(html.Div(id="joke_details"), width=12),
    ], className="my-3"),

    dbc.Row([
        dbc.Col(dcc.Input(id='joke_text', type='text', placeholder="Texto del chiste"), width=8),
        dbc.Col(dbc.Button("Crear Chiste", id='create_joke_button', color="success"), width=4),
    ], className="my-3"),

    dbc.Row([
        dbc.Col(dbc.Button("Eliminar Chiste", id='delete_joke_button', color="danger"), width=4),
    ], className="my-3"),
])


@app.callback(
    Output('joke_details', 'children'),
    [
        Input('get_joke_button', 'n_clicks'),
        Input('create_joke_button', 'n_clicks'),
        Input('delete_joke_button', 'n_clicks'),
    ],
    [
        State('joke_id', 'value'),
        State('joke_text', 'value')
    ]
)
def handle_jokes(get_clicks, create_clicks, delete_clicks, joke_id, joke_text):
    ctx = callback_context
    if not ctx.triggered:
        return ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    try:
        if button_id == 'get_joke_button':
            if not joke_id:
                return "Por favor, ingresa un ID."
            response = requests.get(f"{BASE_URL}/{joke_id}")
            if response.status_code == 200:
                data = response.json()
                joke_text = data.get('Chiste', {}).get('ChisteOFrase', 'Texto no disponible')
                return html.Div([
                    html.H4("Chiste:"),
                    html.P(joke_text)
                ])
            else:
                return "Chiste no encontrado."

        elif button_id == 'create_joke_button':
            if not joke_text:
                return "Por favor, ingresa el texto del chiste."
            response = requests.post(BASE_URL, json={"ChisteOFrase": joke_text})
            if response.status_code in [200, 201]:
                return "Chiste creado con éxito."
            else:
                return f"Error al crear el chiste: {response.text}"

        elif button_id == 'delete_joke_button':
            if not joke_id:
                return "Por favor, ingresa un ID."
            response = requests.delete(f"{BASE_URL}/{joke_id}")
            if response.status_code in [200, 202, 204]:
                return "Chiste eliminado con éxito."
            else:
                return "Error al eliminar el chiste."

    except Exception as e:
        return f"Error de conexión: {str(e)}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)
