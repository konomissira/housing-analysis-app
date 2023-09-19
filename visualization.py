import plotly.graph_objects as go

def create_housing_price_chart(data):
    years = [row['year'] for row in data]
    london_values = [row['avg_london_value'] for row in data]
    uk_values = [row['avg_uk_value'] for row in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=london_values, mode='lines', name='London'))
    fig.add_trace(go.Scatter(x=years, y=uk_values, mode='lines', name='UK'))

    fig.update_layout(title='Average Housing Price Over the Years',
                      xaxis_title='Year',
                      yaxis_title='Average Price (£)')
    return fig
