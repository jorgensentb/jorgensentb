import json
import plotly.graph_objs as go
import requests

def call_api():
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': 'NVDA',
        'interval': '5min',
        'apikey': 'your_api_key_here'  # Replace with your actual API key
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def transform_data(data):
    try:
        if 'Time Series (5min)' in data:
            time_series = data['Time Series (5min)']
            transformed_data = []
            for timestamp, values in time_series.items():
                price = float(values['1. open'])  # Extracting the opening price
                transformed_data.append([timestamp, price])
            return transformed_data
        else:
            print("Error: Couldn't find Time Series data in the API response.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Call the API
api_data = call_api()

# Transform the data
if api_data:
    transformed_data = transform_data(api_data)
    if transformed_data:
        # Print the transformed data
        print("Transformed Data:")
        for entry in transformed_data:
            print(entry)

        # Save transformed data to a JSON file
        with open('market_data.json', 'w') as json_file:
            json.dump(transformed_data, json_file, indent=4)
        print("Data saved to market_data.json")

        # Plotly chart creation
        timestamps = [entry[0] for entry in transformed_data]
        prices = [entry[1] for entry in transformed_data]

        # Create Plotly trace
        trace = go.Scatter(x=timestamps, y=prices, mode='lines+markers', name='Market Data')

        # Create Plotly layout
        layout = go.Layout(title='Market Chart', xaxis=dict(title='Timestamp'), yaxis=dict(title='Price'))

        # Create Plotly figure
        fig = go.Figure(data=[trace], layout=layout)

        # Save the figure as an HTML file
        fig.write_html('market_chart.html', auto_open=True)

        print("Chart generated successfully!")
