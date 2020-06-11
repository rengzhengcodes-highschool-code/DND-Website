#! /usr/bin/python
import cgi
import codecs
import requests
def html_page():
    page = codecs.open('template.html', 'r', 'utf-8').read()
    body_code = body_format()
    page.format(title = 'homepage', body = body_code)
    print('Content-type:text/html\n\n' + page)
    print('<p>' + body_code + '<p>')

def body_format():
    response = requests.get('https://api.open5e.com/spells/?page=1')
    return str(response)
try:
    html_page()
except:
    print(cgi.print_exception())