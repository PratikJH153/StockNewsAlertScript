import requests
import datetime as dt
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API = ""
NEWS_API = ""

today_date = "2022-01-21"
yesterday_date = "2022-01-20"


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# today_date = dt.date.today()
# yesterday_date = today_date - dt.timedelta(days=1)
def stock_data():
    STOCK_URL = "https://www.alphavantage.co/query"
    stock_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_API
    }

    response = requests.get(STOCK_URL, params=stock_parameters)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]
    today_stock_data = data[today_date]
    yesterday_stock_data = data[yesterday_date]

    previous_close = float(yesterday_stock_data["4. close"])
    initial_close = float(today_stock_data["4. close"])

    difference = ((previous_close - initial_close) / previous_close) * 100

    return difference


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def news_data():
    new_url = f"https://newsapi.org/v2/everything"
    news_parameters = {
        "q": "tesla",
        "from": today_date,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API
    }

    response = requests.get(new_url, params=news_parameters)
    response.raise_for_status()

    data = response.json()

    return data


is_stock_data_important = stock_data()

if abs(is_stock_data_important) > 5:
    news_data = news_data()["articles"]

    sign = "🔼" if is_stock_data_important > 5 else "🔽"

    news_format = f"{STOCK}: {sign}{round(is_stock_data_important)}%\nHeadline: {news_data[0]['title']}\nBrief: {news_data[0]['description']}"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        EMAIL = ""
        PASSWORD = ""
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=f"Subject:Stock News Alert!\n\n{news_format}")


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

