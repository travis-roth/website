import plotly.graph_objs as go

def generate_plot():
    # Generate some sample data
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 30, 40, 50]

    # Create a Plotly scatter plot
    trace = go.Scatter(x=x, y=y, mode='lines+markers', name='Sample Data')
    data = [trace]

    # Create layout for the plot
    layout = go.Layout(title='Sample Plot', xaxis=dict(title='X-axis'), yaxis=dict(title='Y-axis'))

    # Combine data and layout into a figure
    fig = go.Figure(data=data, layout=layout)

    # Convert the figure to JSON
    plot_json = fig.to_json()

    return plot_json