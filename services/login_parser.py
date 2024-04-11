import urllib.parse
import requests
from lxml import etree
import json
import re
from bs4 import BeautifulSoup


class EcampusSession:
    BASE_URL = 'https://ecampus.ncfu.ru'
    VERIFICATION_TOKEN_URL = BASE_URL + '/account/login'
    LOGIN_URL = BASE_URL + '/Account/Login'
    DETAILS_URL = BASE_URL + '/details'
    ZACHETKA_URL = BASE_URL + '/details/zachetka'
    BASE_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9,en-RU;q=0.8,en;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "ecampus.ncfu.ru",
        "Origin": "https://ecampus.ncfu.ru",
        "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36",
    }
    VERIFICATION_TOKEN_HEADERS = {
        "Referer": "https://ecampus.ncfu.ru/"
    }
    LOGIN_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://ecampus.ncfu.ru/account/login"
    }

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.session.headers.update(self.BASE_HEADERS)

    def _get_verification_token(self):
        token_request = self.session.get(self.VERIFICATION_TOKEN_URL, headers=self.VERIFICATION_TOKEN_HEADERS)
        parser = etree.HTMLParser()
        tree = etree.fromstring(token_request.text, parser=parser)
        self.verification_token = tree.xpath("//*[@id='page']/section/form/input["
                                             "@name='__RequestVerificationToken']/@value")[0]
        self.session_cookies = token_request.cookies

    def login_to_ecampus(self):
        self._get_verification_token()
        payload = {
            "__RequestVerificationToken": self.verification_token,
            "Login": self.login,
            "Password": self.password,
            "Code": "1",
            "RememberMe": "false",
        }
        raw = urllib.parse.urlencode(payload)
        self.session.cookies.set("captcha", "010817-8111-1040-035104-c2df2d12-7c55-46d0-9fa9-da5d699e0b65")
        login_request = self.session.post(self.LOGIN_URL, headers=self.LOGIN_HEADERS, cookies=self.session_cookies,
                                          data=raw)
        if login_request.status_code == 200:
            print("Login successful!")
        else:
            print("Login failed!")

    def parse_details(self):
        details_request = self.session.get(self.DETAILS_URL)
        if details_request.history:
            print("Failed to fetch details. Logging in...")
            self.login_to_ecampus()
            details_request = self.session.get(self.DETAILS_URL)

        html = details_request.text
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', string=re.compile('viewModel'))
        json_text = re.search(r'\s*viewModel\s*=\s*({.*?})\s*;\s*$', script.string,
                              flags=re.DOTALL | re.MULTILINE).group(1)
        data = json.loads(json_text)
        return data

    def parse_zachetka(self):
        zachetka_request = self.session.get(self.ZACHETKA_URL)
        if zachetka_request.history:
            print("Failed to fetch details. Logging in...")
            self.login_to_ecampus()
            zachetka_request = self.session.get(self.DETAILS_URL)

        html = zachetka_request.text
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', string=re.compile('viewModel'))
        json_text = re.search(r'\s*viewModel\s*=\s*({.*?})\s*;\s*$', script.string,
                              flags=re.DOTALL | re.MULTILINE).group(1)
        json_text = json_text.replace('JSON.parse("\\"', '"').replace('\\"")', '"')
        data = json.loads(json_text)
        return data


if __name__ == "__main__":
    login = ""
    password = ""
    ecampus_session = EcampusSession(login, password)
    # ecampus_session.login_to_ecampus()
    details_data = ecampus_session.parse_details()
    print(details_data)
    zachetka_data = ecampus_session.parse_zachetka()
    print(zachetka_data)
