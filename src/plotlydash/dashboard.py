import plotly.express as px
from dash import Dash, dcc, html


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        # external_stylesheets=[
        #     "/static/dist/css/styles.css",
        # ],
    )
    dash_app.title = "Book Visualizations"

    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x="year", y="pop")

    dash_app.layout = html.Div(
        children=[
            html.A("click me", href="/index"),
            dcc.Graph(figure=fig),
        ]
    )

    init_callbacks(dash_app)
    return dash_app.server


def init_callbacks(dash_app):
    pass
