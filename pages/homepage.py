#! /usr/bin/python
import cgi
import codecs
import requests
def html_page():
    print('Content-type:text/html\n\n' + 
    codecs.open('template.html','r', 'utf-8').read().format('homepage')
    )
html_page()
