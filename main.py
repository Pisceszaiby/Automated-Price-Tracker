from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
from constants import EMAIL,PASSWORD,TO_ADDRESS,FROM_ADDRESS

url = "https://www.amazon.com/SteelSeries-Apex-Gaming-Keyboard-Anti-Ghosting/dp/B09FTNMT84/ref=sr_1_1_sspa?keywords=gaming+keyboard&pd_rd_r=8cb2dd30-38b4-44c2-9151-192b727ba6f3&pd_rd_w=63Ng0&pd_rd_wg=c8dTq&pf_rd_p=12129333-2117-4490-9c17-6d31baf0582a&pf_rd_r=DQZBSH81WFEVSPCNNWM4&qid=1659036056&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzQTk4T1ZZVlNRT01BJmVuY3J5cHRlZElkPUEwNzY3MDQ4MllINlhHQUdFT1Y3JmVuY3J5cHRlZEFkSWQ9QTA4NDM3NDIxRkpYSUU5NFQwRjdQJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
amazon_response = requests.get(
    url,
    headers={
        'Accept-Language':
        "en-US,en;q=0.9",
        'User-Agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    })

forex_response = requests.get(
    "https://www.forex.pk/currency-usd-to-pkr-to-us-dollar.php")
amazon_webpage = amazon_response.text
forex_webpage = forex_response.text

amazon_soup = BeautifulSoup(amazon_webpage, "lxml")
forex_soup = BeautifulSoup(forex_webpage, "html.parser")

dollar_rate = float((forex_soup.find(id="RATESPAN")).getText())
price_dollar = float(
    ((amazon_soup.find(name="span", class_="a-offscreen")).getText()).split("$")[1])
title = (amazon_soup.find(id="productTitle")).getText()
price_pkr = price_dollar * dollar_rate

if 12000 > price_pkr:
    message = f"{title} is now at a price of {price_pkr} PKR and ${price_dollar}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(EMAIL,PASSWORD)
        connection.sendmail(
            from_addr=FROM_ADDRESS,
            to_addrs=TO_ADDRESS,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode(
                "utf-8"))
