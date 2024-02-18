from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv"
df = pd.read_csv(url)
app = Dash(__name__)
server = app.server
# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='World GDP Visualization'),
    # Choropleth map
    dcc.Graph(
        id='world-map',
        figure=px.choropleth(
            df,
            locations='CODE',
            color='GDP (BILLIONS)',
            hover_name='COUNTRY',
            title='World GDP Choropleth Map',
            color_continuous_scale='Viridis'
        )
    ),
    # Dropdown for GDP range selection
    html.Label('Select GDP Range:'),
    dcc.Dropdown(
        id='gdp-range-dropdown',
        options=[
            {'label': '0-5 Billion', 'value': '0-5'},
            {'label': '5-10 Billion', 'value': '5-10'},
            {'label': '10-15 Billion', 'value': '10-15'},
            {'label': '15-20 Billion', 'value': '15-20'},
            {'label': '20+ Billion', 'value': '20+'},
        ],
        value='0-5',
        multi=False
    ),

    # Bar chart
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(
            df,
            x='COUNTRY',
            y='GDP (BILLIONS)',
            title='World GDP Bar Chart'
        )
    )
])

# Define callback to update bar chart based on selected GDP range
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('gdp-range-dropdown', 'value')]
)
def update_bar_chart(selected_range):
    if selected_range == '20+':
        filtered_df = df[df['GDP (BILLIONS)'] >= 20]
    else:
        range_values = selected_range.split('-')
        filtered_df = df[(df['GDP (BILLIONS)'] >= int(range_values[0])) & (df['GDP (BILLIONS)'] < int(range_values[1]))]

    bar_chart = px.bar(
        filtered_df,
        x='COUNTRY',
        y='GDP (BILLIONS)',
        title=f'World GDP Bar Chart - {selected_range}',
    )

    return bar_chart.update_layout(title_text=f'World GDP Bar Chart - {selected_range}')

# Run the app
if __name__ == '__main__':
        app.run_server()
