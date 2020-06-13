#! /usr/bin/python
import cgi
import codecs
import random
import requests


def get_spell(): #retrieves name of a random spell
    with open('dependencies/index/slugs.txt') as file:
        spells = list(file)
        spell = (spells[random.randint(0, len(spells) - 1)]).rstrip('\n')
        return spell


spell_api_import = lambda spell: requests.get('https://api.open5e.com/spells/?slug__iexact={spell}'.format(spell=spell)).json()['results'][0]


def markdown_to_html_marker(string, markdown_marker, html_marker):
    markdown_marker_length = len(markdown_marker)
    markdown_marker_count = string.count(markdown_marker)
    for i in range(markdown_marker_count):
        index = string.find(markdown_marker)
        if i % 2 == 0:
            string = string[:index] + html_marker.format('') + string[index + markdown_marker_length:]
        else:
            string = string[:index] + html_marker.format('/') + string[index + markdown_marker_length:]
    return string


def markdown_to_html(string):
    string = markdown_to_html_marker(string, '**', '<{}b>')
    return string


def python_to_html_marker(string, python_marker, html_marker):
    return string.replace(python_marker, html_marker)


def python_to_html(string):
    string = python_to_html_marker(string, '\n', '<br>')
    string = python_to_html_marker(string, '\"', '"')#this isn't actually inherently a python marker but a work around to removing the " from earlier
    return string


def spell_html_format():
    spell = spell_api_import(get_spell())
    container = codecs.open('dependencies/index/spell.html', 'r', 'utf-8').read()
    name = spell['name']
    if spell['material']: #combines components and flavortext materials line if materials line exists
        spell_components = '{components} ({materials})'.format(components = spell['components'], materials = spell['material'])
    else:
        spell_components = spell['components']
    if spell['higher_level']: #adds what happens at a higher level, if anything
        higher_level = '<br> <b>At Higher Levels: </b>' + spell['higher_level']
    else:
        higher_level = ''
    container = container.format(name = name, level = spell['level'], school = spell['school'], classes = spell['dnd_class'], archetypes = spell['archetype'], 
    range=spell['range'], duration=spell['duration'], components=spell_components, concentration=spell['concentration'], ritual=spell['ritual'], spelldesc = spell['desc'], 
    higher_level=higher_level, source=spell['page'], license = spell['document__license_url'])
    container = markdown_to_html(python_to_html(container))
    return container


def main():
    spell = spell_html_format()
    page = 'Content-type:text/html\n\n' + codecs.open('dependencies/index/index.html', 'r', 'utf-8').read().format(title='homepage', body=spell)
    print(page)


try:
    main()
except:
    print(cgi.print_exception())