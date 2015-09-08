from flask import Flask,render_template, redirect, request
from bokeh.charts import TimeSeries, output_file, show
from bokeh.plotting import figure
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

		x = [1, 2, 3, 4, 5]
		y = [6, 7, 8, 9, 10]

		# output to static HTML file
		output_file("lines.html", title="line plot example")

		# create a new plot with a title and axis labels
		p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

		# add a line renderer with legend and line thickness
		p.line(x, y, legend="Temp.", line_width=2)

		# show the results
		return show(p)	
		#r = requests.get(url)
		#dat1 = json.loads(r.text)
		#df = pd.DataFrame(dat1['dataset']['data'], columns=dat1['dataset']['column_names'])
		#df['Date'] = pd.to_datetime(df['Date'])

		#output_file("prices.html", title="stock prices")
		#if app.vars['feature'] == 'Close':
	#		ylab = "Closing price"
	#	if app.vars['feature'] == 'Adj. Close':
	#		ylab = "Adjusted closing price"
	#	if app.vars['feature'] == 'Volume':
	#		ylab = "Volume"
	#	p = TimeSeries(df[str(app.vars['feature'])], df['Date'], title=str(app.vars['ticker']), ylabel=ylab)

	#	return show(p)
	#	return url
if __name__ == '__main__':
    app.run(port=int(os.environ.get("Port", 5000)), host='0.0.0.0', debug=False)
