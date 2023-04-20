from flask import Flask, render_template, request
import requests
import pygal

app = Flask(__name__)

@app.route('/')
def index():
    symbols = ['AAPL', 'GOOG', 'MSFT']  
    chart_types = ['Line Chart', 'Bar Chart']  
    return render_template('index.html', symbols=symbols, chart_types=chart_types)

@app.route('/chart', methods=['POST'])
def chart():
    symbol = request.form['symbol']
    chart_type = request.form['chart_type']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey=WNHA95VNGXUV2S6K'
    response = requests.get(url)
    
    data = response.json()['Time Series (Daily)']
    dates = sorted(data.keys())
    close_values = [float(data[date]['4. close']) for date in dates if start_date <= date <= end_date]
    
    if chart_type == 'Line Chart':
        line_chart = pygal.Line()
        line_chart.title = f'{symbol} Daily Closing Prices'
        line_chart.x_labels = dates
        line_chart.add('Close', close_values)
        chart = line_chart.render()
        chart = chart.decode('utf-8') 
    else:
        bar_chart = pygal.Bar()
        bar_chart.title = f'{symbol} Daily Closing Prices'
        bar_chart.x_labels = dates
        bar_chart.add('Close', close_values)
        chart = bar_chart.render()
        chart = chart.decode('utf-8')

    return render_template('chart.html', chart=chart)

if __name__ == '__main__':
    app.run(debug=True)
