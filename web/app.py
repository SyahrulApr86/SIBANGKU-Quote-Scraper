from flask import Flask, render_template
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask app initialization
app = Flask(__name__)

# Get database connection credentials from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'quotesdb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_PORT = os.getenv('DB_PORT', '5555')

# Function to connect to PostgreSQL database
def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

# Route to display all quotes
@app.route('/')
def show_quotes():
    # Connect to the database
    conn = connect_db()
    cur = conn.cursor()

    # Execute query to fetch all quotes
    cur.execute("SELECT quote, name, year FROM quotes")
    quotes = cur.fetchall()

    # Close connection
    cur.close()
    conn.close()

    # Pass quotes data to the template
    return render_template('quotes.html', quotes=quotes)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
