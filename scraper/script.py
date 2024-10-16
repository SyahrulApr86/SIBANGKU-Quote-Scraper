import os
from dotenv import load_dotenv
import requests
import html
import psycopg2
from datetime import datetime
import time

# Load environment variables from .env file
load_dotenv()

# Get username and password from .env
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Define headers used in the requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Ch-Ua": '"Chromium";v="129", "Not=A?Brand";v="8"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Accept-Encoding": "gzip, deflate, br",
}

# Connect to PostgreSQL database
def connect_db():
    # Get database connection parameters from environment variables
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'quotesdb')
    DB_USER = os.getenv('DB_USER', 'user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_PORT = os.getenv('DB_PORT', '5432')  # Ganti dengan port yang sesuai jika perlu

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn


# Function to retrieve all existing quotes and return as a set for quick lookup
def get_existing_quotes(conn):
    cur = conn.cursor()
    cur.execute("SELECT quote, name, year FROM quotes")
    rows = cur.fetchall()
    existing_quotes = {(row[0], row[1], row[2]) for row in rows}  # Set of (quote, name, year)
    cur.close()
    return existing_quotes

# Function to insert new quote into database if it doesn't exist
def insert_quote_if_not_exists(quote, name, year, conn, existing_quotes):
    if (quote, name, year) not in existing_quotes:
        cur = conn.cursor()
        first_found = datetime.now()
        cur.execute("INSERT INTO quotes (quote, name, year, first_found) VALUES (%s, %s, %s, %s)",
                    (quote, name, year, first_found))
        conn.commit()
        print(f"Inserted: {quote}")
        # Add the new quote to the existing set to avoid future duplicates
        existing_quotes.add((quote, name, year))
        cur.close()
    else:
        print(f"Quote already exists: {quote}")

def login(session):
    # Initial GET request to /sibangku/
    url1 = "https://ujian.cs.ui.ac.id/sibangku/"
    session.get(url1, headers=headers, cookies={
        "csrftoken": "SN3tAzJ0nC8s4bvKe6KtfJUHC5aZRjB6JPazd6eC44Ma4wh1Ful54QPmMD8js0bi",
        "sessionid": "yc26x0zsy21l0ei14vdfoutrdn5blhx6"
    })

    # GET request to SSO
    url3 = "https://sso.ui.ac.id/cas2/login?service=https%3A%2F%2Fujian.cs.ui.ac.id%2Fsibangku%2Flogin%2F"
    session.get(url3, headers=headers)

    # POST login to SSO
    url4 = "https://sso.ui.ac.id/cas2/login;jsessionid=F4C4215EC1CD043DF8219DE91A389A65?service=https%3A%2F%2Fujian.cs.ui.ac.id%2Fsibangku%2Flogin%2F"
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "lt": "LT-652-IOi2Jzk3Dnhhcche4ytZsKiaK2jhC9",
        "execution": "e1s1",
        "_eventId": "submit"
    }
    session.post(url4, headers=headers, data=data)

def get_quote_name_year(session):
    # Final GET request to /sibangku/jadwal/
    url5 = "https://ujian.cs.ui.ac.id/sibangku/jadwal/"
    response5 = session.get(url5, headers=headers, cookies={
        "csrftoken": "SN3tAzJ0nC8s4bvKe6KtfJUHC5aZRjB6JPazd6eC44Ma4wh1Ful54QPmMD8js0bi",
        "sessionid": "yc26x0zsy21l0ei14vdfoutrdn5blhx6"
    })

    # Extract quote, name, and angkatan directly from the response text
    html_content = response5.text

    # Find the quote part
    quote_start = html_content.find('<p class="h6"')  # Locate the start of the quote
    quote_end = html_content.find('</p>', quote_start)  # Locate the end of the quote
    quote = html_content[quote_start:quote_end].split(">")[-1].strip()

    # Use html.unescape to decode HTML entities in the quote
    quote = html.unescape(quote)

    # Find the name and year part
    name_start = html_content.find('<cite title="Source Title">')  # Locate the start of the name
    name_end = html_content.find('</cite>', name_start)  # Locate the end of the name
    name_and_year = html_content[name_start:name_end].split(">")[-1].strip()

    name = name_and_year.split(",")[0].strip()
    parts = name_and_year.split(",")

    # Fallback jika elemen dengan indeks 1 tidak ada
    if len(parts) > 1:
        year_part = parts[1].strip()
    else:
        year_part = parts[0].strip()

    # Lanjutkan split dengan spasi dan berikan fallback untuk indeks terakhir atau pertama
    year_parts = year_part.split(" ")

    if len(year_parts) > 1:
        year = year_parts[-1]
    else:
        year = year_parts[0]

    # Return the extracted information
    return quote, name, year

def main():
    while True:
        # Your existing code here
        session = requests.Session()
        conn = connect_db()
        existing_quotes = get_existing_quotes(conn)
        login(session)
        for i in range(10_000):
            quote, name, year = get_quote_name_year(session)
            insert_quote_if_not_exists(quote, name, year, conn, existing_quotes)
        conn.close()

        # Wait for 2 hours (7200 seconds)
        time.sleep(7200)


if __name__ == "__main__":
    main()
