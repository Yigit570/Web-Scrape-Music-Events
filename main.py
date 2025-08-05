import requests
import selectorlib
import os, dotenv
import smtplib, ssl

URL = "https://programmer100.pythonanywhere.com/tours/"

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
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read():
    with open("data.txt", "r") as file:
        return file.read()

scraped = scrape(URL)
extracted = extract(scraped)
print(extracted)

content = read()

message = f"""\
Subject: Hey new event appeared

New event: {extracted}
"""

if extracted != "No upcoming tours":
    if extracted not in content:
        store(extracted)
        send_mail(message)