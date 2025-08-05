import requests
import selectorlib
import os, dotenv
import smtplib, ssl
import sqlite3
import time

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")

def scrape(url):
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_mail(message):
    host = "mail.yigitac.com"
    port = 465

    sender = "info@yigitac.com"

    dotenv.load_dotenv()
    password = os.getenv("PASSWORD")

    reciever = "info@yigitac.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, reciever, message)

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read():
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows

while True:
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    if extracted != "No upcoming tours":
        row = read()
        if not row:
            store(extracted)
            message = f"""\
    Subject: Hey, new event appeared!

    New event: {extracted}
    """
            send_mail(message)
    
    time.sleep(2)