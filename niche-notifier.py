#!/usr/bin/python3
import config
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import pytz

NICHE_URL = "https://vgoffice.catholic.org.hk/cemetery/niche_eng.aspx"


def parse_html(url):
    """Extracting a long string from the HTML"""
    response = requests.get(url, headers={
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'})
    if response.ok:
        soup = BS(response.text, 'html.parser')
        print("LOG ~ parse_html: Successfully retrieved and parsed html")
        return soup
    else:
        raise Exception("Failed to retrieve web page with status code ",
                        response.status_code, " and followint response content: ", response.content)


def get_AM_info(soup):
    """
    Takes html soup and get the AM row and column number.
    Returns a dictionary of row and column. Both are texts.
    """
    print("LOG ~ get_AM_info : Start retrieving AM info")
    row = soup.find(id="TB_AM_CW_ROW").text
    column = soup.find(id="TB_AM_CW_NUMBER").text
    print(
        f"LOG ~ get_AM_info : Retrieved AM info, row {row}, column {column} ")
    return {'row': row, 'column': column, }


def get_PM_info(soup):
    """
    Takes html soup and get the PM row and column number.
    Returns a dictionary of row and column. Both are texts.
    """
    print("LOG ~ get_PM_info : Start retrieving PM info")
    row = soup.find(id="TB_PM_CW_ROW").text
    column = soup.find(id="TB_PM_CW_NUMBER").text
    print(
        f"LOG ~ get_PM_info : Retrieved PM info, row {row}, column {column} ")
    return {'row': row, 'column': column}


def send_email(email_content):
    sendgrid_send_mail_url = "https://api.sendgrid.com/v3/mail/send"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {config.sendgrid_api_key}"}
    email_data = {'personalizations': [
        {
            'to': [
                  {'email': '<your_email_here>'},
                  ]
        },
    ],
        'from': {
        'email': '<your_sender_email>',
        'name': 'Ho Family'
    },
        'reply_to': {
        'email': '<your_sender_email>'
    },
        'subject': 'Holy Cross Cemetery Niches Allocation',
        'headers': {'Priority': 'urgent', 'Importance': 'high', 'X-Priority': '1'},
        'content': [{
            'type': 'text/plain',
            'value': email_content
        }]}
    response = requests.post(sendgrid_send_mail_url,
                             json=email_data, headers=headers)
    if not response.ok:
        print("LOG ~ send_email: Failed to send email. Response status code " +
              response.status_code)
        print(
            "LOG ~ send_email: Failed to send email. Response content: " + response.content)
    else:
        print("LOG ~ send_email: Successfully send email")


if __name__ == '__main__':
    soup = parse_html(NICHE_URL)
    tz_HK = pytz.timezone('Asia/Hong_Kong')
    now = datetime.now(tz_HK)
    print("LOG ~ __main__: Script started at " +
          now.strftime("%d %B, %Y %H:%M:%S"))
    if now.isoweekday() != 7:
        if 0 <= now.hour < 16:
            data = get_AM_info(soup)
        else:
            data = get_PM_info(soup)
        email_content = f'Currently allocating up to niche row {data["row"]}, column {data["column"]} as of {now.strftime("%d %B, %Y %H:%M:%S")}'
        print("LOG ~ __main__: email content " + email_content)
        send_email(email_content)
        print("LOG ~ __main__: Script ended")
