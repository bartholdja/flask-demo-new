from flask import Flask,render_template, redirect, request
from bokeh.charts import TimeSeries, output_file, show
import requests as requests
import pandas as pd
import simplejson as json

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		#request was a POST
		app.vars['ticker'] = request.form['ticker']
		app.vars['feature'] = request.form['features']
		
		url = 'https://www.quandl.com/api/v3/datasets/WIKI/' + str(app.vars['ticker']) + '.json?order=asc&rows=31&start_date=2015-08-01&end_date=2015-08-31'
		r = requests.get(url)
		dat = r.text
		dat1 = json.loads(dat)
		df = pd.DataFrame(dat1['dataset']['data'], columns=dat1['dataset']['column_names'])
		df['Date'] = pd.to_datetime(df['Date'])

		output_file("prices.html", title="stock prices")
		if app.vars['feature'] == 'Close':
			ylab = "Closing price"
		if app.vars['feature'] == 'Adj. Close':
			ylab = "Adjusted closing price"
		if app.vars['feature'] == 'Volume':
			ylab = "Volume"
		p = TimeSeries(df[str(app.vars['feature'])], df['Date'], title=str(app.vars['ticker']), ylabel=ylab)

		return show(p)
if __name__ == "__main__":
    app.run(port=5000, debug=True)
