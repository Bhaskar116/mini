from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import requests
import requests_cache

requests_cache.install_cache(
    'exchange_api_cache', backend='sqlite', expire_after=36000)

app = Flask(__name__)

symbol_url = 'https://forex.1forge.com/1.0.3/symbols?api_key={key}'
convert_url = 'https://forex.1forge.com/1.0.3/convert?from={fromCurrency}&to={toCurrency}&quantity={qty}&api_key={key}'
quotes_url = 'https://forex.1forge.com/1.0.3/quotes?pairs={pairs}&api_key={key}'
history_url = 'http://apilayer.net/api/historical?access_key={key}&date={date}&currencies={currency}'
quote_url = 'https://api.exchangeratesapi.io/latest?base={base}'
history_time_url = 'https://api.exchangeratesapi.io/history?start_at={start}&end_at={end}&symbols={symbols}&base={base}'

MY_API_KEY_FOREX = 'vBNPGoabV5FyTlgv1WA1IuKPX5ZaybbJ'
MY_API_KEY_HIST = 'a396917c6b46215ad0578d2312ad6f10'


@app.route('/exchange', methods=['GET'])
def convert():
    fromCurrency = request.args.get('from')
    toCurrency = request.args.get('to')
    qty = request.args.get('qty')

    url = convert_url.format(
        fromCurrency=fromCurrency, toCurrency=toCurrency, qty=qty, key=MY_API_KEY_FOREX)
    print(url)
    resp = requests.get(url)
    if resp.ok:
        response = resp.json()
        return jsonify(response)
    else:
        return (resp.reason)


@app.route('/symbol', methods=['GET'])
def symbol():

    url = symbol_url.format(key=MY_API_KEY_FOREX)
    print(url)
    resp = requests.get(url)
    if resp.ok:
        response = resp.json()
        return jsonify(response)
    else:
        return (resp.reason)


@app.route('/quotes', methods=['GET'])
def quotes():
    pairs = request.args.get('pairs')

    url = quotes_url.format(
        pairs=pairs, key=MY_API_KEY_FOREX)
    print(url)
    resp = requests.get(url)
    if resp.ok:
        response = resp.json()
        return jsonify(response)
    else:
        return (resp.reason)


@app.route('/quotebase', methods=['GET'])
def quoteBase():
    base = request.args.get('base')

    url = quotes_url.format(
        base=base, key=MY_API_KEY_FOREX)
    resp = requests.get(url)
    if resp.ok:
        response = resp.json()
        return jsonify(response)
    else:
        return (resp.reason)


@app.route('/histCurrency', methods=['GET'])
def history():
    date = request.args.get('date')
    currency = request.args.get('currency')

    url = quotes_url.format(
        date=date, currency=currency, key=MY_API_KEY_HIST)
    print(url)
    resp = requests.get(url)
    if resp.ok:
        response = resp.json()
        return jsonify(response)
    else:
        return (resp.reason)


@app.route('/history', methods=['GET'])
def historical_data():
    start = request.args.get('start')
    end = request.args.get('end')
    base = request.args.get('base')
    symbols = request.args.get('currency')

    url = history_time_url.format(
        start=start, end=end, base=base, symbols=symbols, key=MY_API_KEY_HIST)
    print(url)
    resp = requests.get(url)
    if resp.ok:
        response = resp.json()
        return jsonify(response)
    else:
        return (resp.reason)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
