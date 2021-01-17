from bs4 import BeautifulSoup
import requests
import lxml
import smtplib

URL_TO_TRACK = "YOUR_URL_HERE"
PRICE_TO_TRACK = "YOUR_PRICE_HERE"
MY_EMAIL = "YOUR_EMAIL_HERE"
PWD = "YOUR_PWD_HERE"

header = {
    "User-Agent" : "YOUR_USER_AGENT_HERE",
    "Accept-Language" : "YOUR_ACCEPT_LANGUAGE_HERE"
}

response = requests.get(URL_TO_TRACK, headers=header)
response.raise_for_status()
page_contents = response.text

soup = BeautifulSoup(page_contents, "lxml")

currentPrice = float(soup.select_one("#priceblock_ourprice").getText().split("$")[1])
print(currentPrice)
product_name = soup.select_one("#productTitle").getText()

if currentPrice < PRICE_TO_TRACK:
    message = f"Subject:AMAZON PRICE ALERT!\n\n{product_name} is now ${currentPrice}.\nGet it here: {URL_TO_TRACK}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PWD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=message)
