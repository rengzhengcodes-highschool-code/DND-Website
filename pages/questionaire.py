#! /usr/bin/python
import random
import cgi
import codecs


get_data = lambda name: cgi.FieldStorage().getvalue(name)
get_dependency = lambda filename: codecs.open('dependencies/questionaire/' + filename, 'r', 'utf-8').read()


def main():
    page = 'Content-type:text/html\n\n' + get_dependency('form_template.html')
    form_names = ['class_type', 'dnd_class', 'race', 'background']
    form_values = dict()
    for name in form_names: form_values[name] = get_data(name)
    if form_values['background']: #gives results and enables a reset
        sub = get_dependency('result.html').format(background = form_values['background'], race = form_values['race'], dnd_class = form_values['dnd_class'])
    elif form_values['race']: #asks questions to determine your dnd race
        sub = get_dependency('what_background_are_you.html').format(dnd_class = form_values['dnd_class'], race = form_values['race'])
    elif form_values['dnd_class']: #asks questions to determine your class
        sub = get_dependency('what_race_are_you.html').format(dnd_class = form_values['dnd_class'])
    elif form_values['class_type'] == "martial": #martial character questions
        sub = get_dependency('martial_class.html')
    elif form_values['class_type'] == "both": #both character questions
        sub = get_dependency('both.html')
    elif form_values['class_type'] == "spellcaster": #spellcaster questions
        sub = get_dependency('spell_class.html')
    else:
        sub = get_dependency('what_class_are_you_survey.html') #start page
    print(page.format(sub))


if __name__ == '__main__':
    try:
        main()
    except:
        cgi.print_exception()