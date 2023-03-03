import json
import os

from bs4 import BeautifulSoup

home = os.getenv("HOME")
prolific_html_file_path = f"{home}/compair-adapted-uc/compair/static/modules/comparison/comparison-form-partial.html"
login_html_path = f"{home}/compair-adapted-uc/compair/static/modules/login/login-partial.html"


def thread_data():
    with open('update.json') as update:
        dump_data = json.load(update)
        print("Reading data from the json config file...\n")
        is_link = bool(dump_data['update_prolific']['is_link'])
        data = str(dump_data['update_prolific']['data'])
        g_link = str(dump_data['g_form_update']['link'])
        login_text = str(dump_data['login_text'])
        print("Data collected file...\n")
    match dump_data['info_to_update']:
        case "all":
            print("Updating all modules...\n")
            update_prolific_id(is_link=is_link, data=data)
            print("Prolific Information updated...\n")
            update_google_form_link(link=g_link)
            print("Google form link updated...\n")
            update_login_text(data=login_text)
            print("Login text updated...\n")
            pass
        case "prolific":
            update_prolific_id(is_link=is_link, data=data)
            print("Prolific Information updated...\n")
            pass
        case "g_form":
            update_google_form_link(link=g_link)
            print("Google form link updated...\n")
        case "login":
            update_login_text(data=login_text)
            print("Login text updated...\n")


def update_google_form_link(link=""):
    with open(login_html_path) as gpath:
        soup = BeautifulSoup(gpath, "html.parser")
    iframe = soup.find('iframe')
    iframe['src'] = link
    with open(login_html_path, 'w') as new_f:
        new_f.write(soup.prettify())


def update_login_text(data=""):
    with open(login_html_path) as path:
        soup = BeautifulSoup(path, "html.parser")
    paragraph = soup.find("p", {"id": "login"})
    paragraph.replaceWith(BeautifulSoup(data, 'lxml').p)
    with open(login_html_path,'w') as path:
        path.write(soup.prettify())


def update_prolific_id(is_link=False, data=""):
    with open(prolific_html_file_path) as fp:
        soup = BeautifulSoup(fp, "html.parser")
    default_text = "You have now completed this task. Thank you for taking part! "

    link_provider = f'<a href={data} target="_blank">link</a>'
    m = f'<p id="prolific"><strong>{default_text}Your Prolific completion code is {str(data)}</strong> </p>' \
        if not is_link \
        else f'<p id="prolific"><strong>{default_text}Your prolific completion code is via this {link_provider} ' \
             f'</strong> </p>'
    paragraph = soup.find("p", {"id": "prolific"})
    paragraph.replaceWith(BeautifulSoup(m, 'lxml').p)
    with open(prolific_html_file_path, "w") as fp:
        fp.write(soup.prettify())


thread_data()
