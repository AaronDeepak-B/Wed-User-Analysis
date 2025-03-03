from flask import Flask, request, session, render_template
import sqlite3
import time
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import geocoder
import pandas as pd
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize SQLite database
def init_db():
    with sqlite3.connect('user_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_activity (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT,
                            event TEXT,
                            timestamp REAL,
                            time_spent REAL,
                            ip_address TEXT,
                            location TEXT)''')
        conn.commit()

init_db()

# Function to log user activity
def log_event(user_id, event, ip_address=None, location=None, time_spent=None):
    with sqlite3.connect('user_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO user_activity (user_id, event, timestamp, time_spent, ip_address, location) VALUES (?, ?, ?, ?, ?, ?)''',
                       (user_id, event, time.time(), time_spent, ip_address, location))
        conn.commit()

@app.route('/')
def home():
    session['visit_time'] = time.time()
    session['user_id'] = request.cookies.get('user_id') or str(uuid.uuid4())
    ip_address = request.remote_addr
    location = geocoder.ip(ip_address).city if ip_address else "Unknown"
    log_event(session['user_id'], 'visit', ip_address, location)
    return "Welcome to the website! <a href='/login'>Login</a> or <a href='/signup'>Sign Up</a>"

@app.route('/login')
def login():
    ip_address = request.remote_addr
    location = geocoder.ip(ip_address).city if ip_address else "Unknown"
    log_event(session['user_id'], 'login', ip_address, location)
    return "Logged in successfully. <a href='/'>Home</a>"

@app.route('/signup')
def signup():
    ip_address = request.remote_addr
    location = geocoder.ip(ip_address).city if ip_address else "Unknown"
    log_event(session['user_id'], 'signup', ip_address, location)
    return "Signed up successfully. <a href='/'>Home</a>"

@app.route('/logout')
def logout():
    if 'visit_time' in session:
        time_spent = time.time() - session['visit_time']
        ip_address = request.remote_addr
        location = geocoder.ip(ip_address).city if ip_address else "Unknown"
        log_event(session['user_id'], 'logout', ip_address, location, time_spent)
    session.clear()
    return "Logged out successfully. <a href='/'>Home</a>"

# Dash App for Data Visualization
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/', suppress_callback_exceptions=True)

def generate_dashboard():
    with sqlite3.connect('user_data.db') as conn:
        df = pd.read_sql_query("SELECT event, COUNT(*) as count FROM user_activity GROUP BY event", conn)
        location_df = pd.read_sql_query("SELECT location, COUNT(*) as count FROM user_activity GROUP BY location", conn)
    
    fig_events = px.bar(df, x='event', y='count', title='User Activity')
    fig_locations = px.pie(location_df, names='location', values='count', title='User Locations')
    
    return html.Div([
        dcc.Graph(figure=fig_events),
        dcc.Graph(figure=fig_locations)
    ])

dash_app.layout = html.Div([
    html.H1("Website User Activity Dashboard"),
    html.Div(id='dashboard-content'),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
])

@dash_app.callback(Output('dashboard-content', 'children'), [Input('interval-component', 'n_intervals')])
def update_dashboard(n):
    return generate_dashboard()

if __name__ == '__main__':
    app.run(debug=True)