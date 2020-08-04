import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore


class Browser:
    def __init__(self):
        """
        class Browser can print the text from a website when called with or without 'https://'
        param site_request:: str representing a website
        """
        self.tabs_history = []
        self.tabs_library = {}

    def new_site(self, website):
        nick_name = website.lstrip('https://').rsplit('.', 1)[0]
        path_now = os.path.join(path, nick_name) + '.txt'
        useful_text = self.parse_site(website)
        with open(path_now, 'w') as saving_site:
            saving_site.write(useful_text)
        self.tabs_library[nick_name] = path_now
        self.known_site(website, path_now)

    def is_only_string_in_tag(self, s):
        """Return True if this string is the only child in the parent tag"""
        tag_list = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li']
        return s == s.parent.string and s.parent.name in tag_list

    def parse_site(self, website):
        r = requests.get(website)
        soup = BeautifulSoup(r.content, 'html.parser')
        text_list = soup.find_all(string=self.is_only_string_in_tag)
        for i, string in enumerate(text_list):
            for link in soup.find_all('a'):
                if string in link:
                    blue_string = Fore.BLUE + string
                    text_list.pop(i)
                    text_list.insert(i, blue_string)
        text = '\n'.join(text_list)
        return text

    def known_site(self, site, path_to_file):
        self.tabs_history.append(site)
        # r = requests.get(site)
        # print(r.text)
        with open(path_to_file, 'r') as open_site:
            print(open_site.read())

    def back(self):
        if len(self.tabs_history) > 1:
            self.tabs_history.pop()
            yield self.tabs_history.pop()

    def main(self, website_request):
        if 'back' in website_request:
            return_site = self.back()
            self.known_site(return_site, self.tabs_library[return_site])
        elif website_request in self.tabs_library:
            self.known_site(website_request, self.tabs_library[website_request])
        elif '.' not in website_request[-4:-2]:
            print('Error: Incorrect URL')
        elif 'https://' not in website_request:
            website_url = f'https://{website_request}'
            self.new_site(website_url)
        else:
            self.new_site(website_request)

    def run(self):
        url_request = input()
        while 'exit' not in url_request:
            self.main(url_request)
            url_request = input()
        exit()


try:
    path = sys.argv[1]
    os.mkdir(path)
except FileExistsError:
    pass

browser = Browser()
browser.run()
exit()
