from flask import Flask,render_template, render_template, redirect, request
from bokeh.charts import TimeSeries
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8
import requests as requests
import pandas as pd
import simplejson as json

#from plots import build_plot
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
		dat1 = json.loads(r.text)
		df = pd.DataFrame(dat1['dataset']['data'], columns=dat1['dataset']['column_names'])
		df['Date'] = pd.to_datetime(df['Date'])

		if app.vars['feature'] == 'Close':
			ylab = "Closing price"
		if app.vars['feature'] == 'Adj. Close':
			ylab = "Adjusted closing price"
		if app.vars['feature'] == 'Volume':
			ylab = "Volume"
		fig = TimeSeries(df[str(app.vars['feature'])], df['Date'], title=str(app.vars['ticker']), ylabel=ylab)
		
      	resources = RESOURCES.render(
        js_raw=INLINE.js_raw,
        css_raw=INLINE.css_raw,
        js_files=INLINE.js_files,
        css_files=INLINE.css_files,
        )

        script, div = components(fig, INLINE)
        html = render_template(
		'index_post.html',
		plot_script=script, plot_div=div, plot_resources=resources)
	return encode_utf8(html)

if __name__ == '__main__':
    app.run(debug=True)
	