from flask import Flask, render_template
from visualization import create_housing_price_chart
from flask_sqlalchemy import SQLAlchemy
import psycopg2





app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the data analysis web app!"

@app.route('/housing')
def housing():
    # Here we're using dummy data for demonstration purposes.
    data = [
        {'year': 1995, 'avg_london_value': 74330.86, 'avg_uk_value': 199735.06},
        # ... You'll add other data points here, fetched from your database or any other source.
    ]
    fig = create_housing_price_chart(data)
    fig_div = fig.to_html(full_html=False)
    return render_template('chart.html', chart_div=fig_div)

@app.route('/unemployment-chart')
def unemployment_chart():
    conn = psycopg2.connect(dbname="londondata", user="mahamadoucamara", password="", host="localhost")
    cur = conn.cursor()

    cur.execute("""SELECT "Quarter", AVG("labour_market"."London_Unemployment") AS avg_london_unemployment, 
                          AVG("labour_market"."UK_Unemployment") AS avg_uk_unemployment 
                   FROM "labour_market" 
                   GROUP BY "Quarter" 
                   ORDER BY "Quarter";""")
    
    rows = cur.fetchall()

    # Splitting data into separate lists for easy consumption in charting libraries
    quarters = [row[0] for row in rows]
    london_unemployment = [row[1] for row in rows]
    uk_unemployment = [row[2] for row in rows]

    cur.close()
    conn.close()
    # Sending data to a template for visualization
    #return render_template('unemploymentChart.html', quarters=quarters, london=london_unemployment, uk=uk_unemployment)
    return render_template('unemployment_chart.html', quarters=quarters, london=london_unemployment, uk=uk_unemployment)


if __name__ == '__main__':
    app.run(debug=True)
