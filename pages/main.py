#! /usr/bin/python
import random
import cgi
import codecs
def html_top(name):
    print('''Content-type:text/html\n\n
<!DOCTYPE html>
<html lang="en-US">
	<head>
		<link rel='stylesheet' type='text/css' href='style.css'>
        <title>{}</title>
	</head>
	<body>'''.format(name))

def html_bottom():
    print('''
            </body>
        </html>
        ''')

def navbar():
    print('''
        <div class="topnav">
            <a href="#">How to Play</a>
            <a href="#">Designing Your First Character</a>
            <a href="how_to_dm.html">How to DM</a>
            <a href="about_us.html">About Us</a>
        </div>
        ''')

def main():
    f=codecs.open('homepage.html', 'r', 'utf-8')
    html_top('Introduction to DND')
    navbar()
    print(f.read())
    html_bottom()
    

if __name__ == '__main__':
    try:
        main()
    except:
        cgi.print_exception()
