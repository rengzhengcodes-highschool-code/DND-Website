#! /usr/bin/python
import random
import cgi
import codecs


get_data = lambda name: cgi.FieldStorage().getvalue(name)
get_dependency = lambda filename, path='dependencies/questionaire/forms/': codecs.open(path + filename, 'r', 'utf-8').read()


image_source = {'artificer': '<a href = "https://nerdarchy.com/turn-up-the-heat-in-5e-dd-with-a-go-to-artificer-spell/">https://nerdarchy.com/turn-up-the-heat-in-5e-dd-with-a-go-to-artificer-spell</a>',
                'barbarian': 'phb', 'bard': 'phb', 'cleric': 'phb', 'druid': 'phb', 'fighter': 'phb', 'monk': 'phb', 'paladin': 'phb', 'ranger':'phb', 'rogue': 'phb', 'sorcerer': 'phb', 'warlock': 'phb', 'wizard': 'phb'}


def main():
    page = 'Content-type:text/html\n\n' + get_dependency(path='dependencies/questionaire/', filename='form_template.html')
    if get_data('background'): #gives results and enables a reset
        sub = get_dependency('result.html').format(background = get_data('background'), race = get_data('race'), dnd_class = get_data('dnd_class'), 
        class_image = 'dependencies/questionaire/images/class/{dnd_class}.png'.format(dnd_class = get_data('dnd_class')), image_source = image_source[get_data('dnd_class')])
    elif get_data('race'): #asks questions to determine your dnd race
        sub = get_dependency('what_background_are_you.html').format(dnd_class = get_data('dnd_class'), race = get_data('race'))
    elif get_data('dnd_class'): #asks questions to determine your class
        sub = get_dependency('what_race_are_you.html').format(dnd_class = get_data('dnd_class'))
    elif get_data('class_type') == "martial": #martial character questions
        sub = get_dependency('martial_class.html').format(class_type = get_data('class_type'))
    elif get_data('class_type') == "both": #both character questions
        sub = get_dependency('both_class.html').format(class_type = get_data('class_type'))
    elif get_data('class_type') == "spellcaster": #spellcaster questions
        sub = get_dependency('spell_class.html').format(class_type = get_data('class_type'))
    else:
        sub = get_dependency('what_class_are_you_survey.html') #start page
    print(page.format(sub))


if __name__ == '__main__':
    try:
        main()
    except:
        cgi.print_exception()