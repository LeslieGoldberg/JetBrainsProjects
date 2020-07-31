import os
import sys
import requests


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
        r = requests.get(website)
        with open(path_now, 'w') as saving_site:
            saving_site.write(r.text)
        self.tabs_library[nick_name] = path_now
        self.known_site(website, path_now)

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
