#app.py
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from DB import Database
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_args
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test:jjh3733990!@localhost:3306/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

RECORDS_PER_PAGE = 60

class Sensor(db.Model):
    __tablename__ = 'sensor'
    date = db.Column(db.String(255), primary_key=True)
    hum = db.Column(db.Float)
    temper = db.Column(db.Float)

@app.route('/')
def latest_record():
    db = Database()
    real_time_data = db.show_realtime()[-1]  # Assuming the data is ordered by date, adjust if needed
    return render_template('index.html', real_time_data=real_time_data)

@app.route('/record', methods=['GET', 'POST'])
def record():
    if request.method == 'GET':
        db = Database()
        sql_all = db.show()

        # Pagination 설정
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        total = len(sql_all)
        print(total)
        offset = RECORDS_PER_PAGE * (page - 1)
        print(offset)
        pagination_sql_all = sql_all[offset: offset + RECORDS_PER_PAGE]

        pagination = Pagination(page=page, per_page=RECORDS_PER_PAGE, total=total, css_framework='bootstrap4')

        return render_template('record.html', list=pagination_sql_all, pagination=pagination)

@app.route('/graph')
def graph():
    db = Database()
    sql_all = db.show()

    plot_data(sql_all)
    
    # Embed the plot in the HTML template
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_data = base64.b64encode(img_stream.read()).decode('utf-8')
    
    plt.close()  # Close the plot to free up resources
    
    return render_template('graph.html', img_data=img_data)

def plot_data(data):
    df = pd.DataFrame(data, columns=['Date', 'Humidity', 'Temperature'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    plt.figure(figsize=(10, 6))
        
    plt.plot(df.index, df['Humidity'], label='Humidity')
    plt.plot(df.index, df['Temperature'], label='Temperature')
    plt.title('Humidity and Temperature Over Time')
    plt.xlabel('M')
    
    plt.ylabel('Value')
    plt.legend()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
