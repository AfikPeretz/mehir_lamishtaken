from twilio.rest import Client
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests as rq
from dotenv import load_dotenv
import os
from handle_json import HandleJson



load_dotenv()
URL = 'https://www.gov.il/api/moch/viewlist/Loaddata/ViewList/yitrat_dirot_lemchira'
HEADERS = {
	'Accept': 'application/json, text/plain, */*',
	'Accept-Language': 'en-US,en;q=0.9',
	'Connection': 'keep-alive',
	'Referer': 'https://www.gov.il/apps/moch/viewlist/list/yitrat_dirot_lemchira',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'same-origin',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
	'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"macOS"',
    "host": "www.gov.il",
    "referer": "https://www.gov.il/apps/moch/viewlist/list/yitrat_dirot_lemchira"
}


def start_scraping():
    try:
        with rq.Session() as session:
            session.headers.update(HEADERS)
            response = session.get(URL)
            response.raise_for_status()
            response_content = response.content.decode('utf-8')
            json_list = json.loads(response_content)
            cities = [item['field3'] for item in json_list]
            prices_for_meter = [item['field8'] for item in json_list]
            return cities, prices_for_meter
    except rq.exceptions.RequestException as e:
        print("Error during HTTP request:", e)
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print("Error parsing JSON data:", e)
        return None


def send_whatsapp(city, price):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
      from_='whatsapp:+14155238886',
      body=f'התפנתה דירה של המחיר למשתכן ב{city}, במחיר של {price} למטר',
      to=f"whatsapp:{os.getenv('MY_PHONE_NUMBER')}"
    )


def send_email(city, price):
    send_from_email = "smtpforpythoncode@gmail.com"
    password = os.getenv('EMAIL_PASSWORD')
    subject = f"דירה חדשה ב{city}"
    msg_body = f'התפנתה דירה של המחיר למשתכן ב{city}, במחיר של {price} למטר'
    msg = MIMEMultipart()
    msg['From'] = send_from_email
    msg['To'] = os.getenv('MY_EMAIL_ADDRESS')
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_body, 'plain', 'utf-8'))
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=send_from_email, password=password)
        connection.sendmail(from_addr=send_from_email, to_addrs=os.getenv('MY_EMAIL_ADDRESS'), msg=msg.as_string())


def check_if_need_to_let_me_know(list_of_lists_of_cities_and_prices, json_of_already_existing_cities):
    is_need_to_let_me_know = False
    for i in range(len(list_of_lists_of_cities_and_prices[0])):
        if list_of_lists_of_cities_and_prices[0][i] not in json_of_already_existing_cities.keys():
            send_whatsapp(list_of_lists_of_cities_and_prices[0][i], list_of_lists_of_cities_and_prices[1][i])
            send_email(list_of_lists_of_cities_and_prices[0][i], list_of_lists_of_cities_and_prices[1][i])
            is_need_to_let_me_know = True
        elif list_of_lists_of_cities_and_prices[0][i] in json_of_already_existing_cities.keys() and \
                list_of_lists_of_cities_and_prices[1][i] < \
                json_of_already_existing_cities[list_of_lists_of_cities_and_prices[0][i]]:
            send_whatsapp(list_of_lists_of_cities_and_prices[0][i], list_of_lists_of_cities_and_prices[1][i])
            send_email(list_of_lists_of_cities_and_prices[0][i], list_of_lists_of_cities_and_prices[1][i])
            is_need_to_let_me_know = True
    return is_need_to_let_me_know


def updated_json(list_of_lists_of_cities_and_prices):
    dict_to_json = {}
    for i in range(len(list_of_lists_of_cities_and_prices[0])):
        if list_of_lists_of_cities_and_prices[0][i] not in dict_to_json.keys():
            dict_to_json[list_of_lists_of_cities_and_prices[0][i]] = list_of_lists_of_cities_and_prices[1][i]
        else:
            dict_to_json[list_of_lists_of_cities_and_prices[0][i]] = \
                min(dict_to_json[list_of_lists_of_cities_and_prices[0][i]], list_of_lists_of_cities_and_prices[1][i])
    return dict_to_json


def main():  # def lambda_handler(event, context):
    handle_json = HandleJson()
    list_of_lists_of_cities_and_prices = start_scraping()
    if list_of_lists_of_cities_and_prices:
        json_of_already_existing_cities = handle_json.read_data_from_json()
        if check_if_need_to_let_me_know(list_of_lists_of_cities_and_prices, json_of_already_existing_cities):
            handle_json.empty_json_file()
            dict_to_json = updated_json(list_of_lists_of_cities_and_prices)
            handle_json.write_data_to_json(dict_to_json)


if __name__ == "__main__":
    main()
