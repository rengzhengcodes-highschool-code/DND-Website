#! /usr/bin/python
import random
import cgi
import codecs


def getData(x): #imports cgi formdata
    form = cgi.FieldStorage()
    if form.getvalue(x):
        subject = form.getvalue(x)
    else:
        subject = "none"
    return subject


dependencies = 'dependencies/questionaire/' #dependency relative path


def main():
    print('Content-type:text/html\n\n') 
    template = codecs.open('template.html', 'r', 'utf-8')
    class_type = getData("class_type")
    dnd_class = getData("class1")
    race = getData("race")
    background = getData("background")
    show_menu = True
    page = template.read().format(title='Questionaire', body='''
    <center>
        <div class = "text">
            <form method='get' action = 'questionaire.py'>
                {}
            </form>
        </div>
    </center>
    ''', update='6/12/2020 by M. Rudin-Aulenbach')
    if background != "none": #gives results and enables a reset
        page = page.format('''<h1>Congratulations! You used to be a {background} but now you are a {race} {dnd_class}!</h1>
                 <form action = 'questionaire.py'>
                    <input type='reset' value='reset'/>'''.format(background=background, race=race, dnd_class=dnd_class))
        race = "none"
        dnd_class = "none"
        print(page)
        show_menu = False
        show_menu = False
    elif race != "none": #asks questions to determine your dnd race
        sub = codecs.open(dependencies + 'what_background_are_you.html', 'r', 'utf-8').read()
        page = page.format('''<div class = "text">
                                <input type='hidden' NAME = 'class_type' VALUE="{class_type}"/>
                                <input type='hidden' NAME = 'class1' VALUE="{dnd_class}"/>
                                <input type='hidden' NAME = 'race' VALUE="{race}"/>
                                {sub}'''.format(class_type = class_type, dnd_class = dnd_class, race = race, sub = sub))
        print(page)
        show_menu = False
    elif dnd_class != "none": #asks questions to determine your class
        sub=codecs.open(dependencies + 'what_race_are_you.html', 'r', 'utf-8')
        page = page.format('''<input type='hidden' NAME = 'class_type' VALUE="{class_type}"/>
                    <input type='hidden' NAME = 'class1' VALUE="{dnd_class}"/>'''.format(class_type = class_type, dnd_class = dnd_class) + sub.read())
        print(page)
        show_menu = False
    elif class_type == "martial": #martial character questions
        sub=codecs.open(dependencies + 'martial_class.html', 'r', 'utf-8')
    elif class_type == "both": #both character questions
        sub=codecs.open(dependencies + 'both.html', 'r', 'utf-8')
    elif class_type == "spellcaster": #spellcaster questions
        sub=codecs.open(dependencies + 'spell_class.html', 'r', 'utf-8')
    if class_type != "none" and dnd_class == "none" and background == "none":
        page = page.format(''' <input type='hidden' NAME = 'class_type' VALUE="{class_type}"/>'''.format(class_type=class_type) + sub.read())
        print(page)
        show_menu = False
    if show_menu:
        page = page.format(codecs.open(dependencies + 'what_class_are_you_survey.html', 'r', 'utf-8').read()) #start page
        print(page)

if __name__ == '__main__':
    try:
        main()
    except:
        cgi.print_exception()
