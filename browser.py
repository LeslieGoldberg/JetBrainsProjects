import os
import sys
import requests

tabs_library = {}
tabs_history = []


def new_site(website):
    nickname = website.lstrip('https://').rsplit('.', 1)[0]
    path_now = os.path.join(path, nickname) + '.txt'
    r = requests.get(website)
    with open(path_now, 'w') as saving_site:
        saving_site.write(r.text)
    tabs_library[nickname] = path_now
    known_site(path_now)


# for calling a site already in the directory
def known_site(path_now):
    with open(path_now, 'r') as open_site:
        print(open_site.read())
    tabs_history.append(path_now)


def back():
    if len(tabs_history) > 1:
        tabs_history.pop()
        last_opened = tabs_history.pop()
        with open(last_opened, 'r') as open_site:
            print(open_site.read())
    else:
        pass


def web_browser(tab_request):
    if 'back' in tab_request:
        back()
    elif tab_request in tabs_library:
        known_site(tabs_library[tab_request])
    elif '.' not in tab_request[-4:-2]:
        print('Error: Incorrect URL')
    elif 'https://' not in tab_request:
        website = f'https://{tab_request}'
        new_site(website)
    else:
        new_site(tab_request)


path = sys.argv[-1]
# what if there is no argument passed there?
try:
    os.mkdir(path)
except FileExistsError:
    pass


site_req = input()
while 'exit' not in site_req:
    web_browser(site_req)
    site_req = input()
exit()
