from flask import Flask, render_template
from visualization import create_housing_price_chart
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/housing')
def housing():
    conn = psycopg2.connect(dbname="londondata", user="mahamadoucamara", password="", host="localhost")
    cur = conn.cursor()
    cur.execute("""SELECT EXTRACT(YEAR FROM "Month") AS year, AVG(housing_price_index."London_Value") AS avg_london_value, 
                AVG(housing_price_index."UK_Value") AS avg_uk_value FROM housing_price_index 
                GROUP BY year 
                ORDER BY year;""")
    
    rows = cur.fetchall()
    years = [int(row[0]) for row in rows]
    avg_london_values = [float(row[1]) for row in rows]
    avg_uk_values = [float(row[2]) for row in rows]


    
    return render_template('housing_chart.html', years=years, avg_london_values=avg_london_values, avg_uk_values=avg_uk_values)

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
