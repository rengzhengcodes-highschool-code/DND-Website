#! /usr/bin/python
import cgi
import codecs
import random
import requests


def get_spell(): #retrieves name of a random spell
    with open('dependencies/index/slugs.txt') as file:
        spells = list(file)
        spell = (spells[random.randint(0, len(spells) - 1)]).rstrip('\n')
        file.close()
        return spell


def spell_api_import():
    spell = get_spell()
    response = requests.get('https://api.open5e.com/spells/?slug__iexact={spell}'.format(spell=spell))
    data = response.content.decode('utf-8')
    data = str(data)
    data = data[data.find('[')+3: data.rfind(']')-2] #removes extraneous characters
    level_int_location = data.find('"level_int"') + 12 #this is a data point that isnt stored as a string in the api, which messes up the splitter function. We're adding a character in so it splits at the desired location.
    data = data[: level_int_location] + data[level_int_location] + '"' + data[level_int_location + 1:] #Adds character so split() can process the split correctly.
    data = list(data.split('","'))
    for i in range(len(data)):
        data[i] = data[i].replace('"', '', 2) #removes extraneous "
    spell_attributes = dict()
    for attribute in data.copy():
        colon_separator_location = attribute.find(':')
        category, value = attribute[0:colon_separator_location], attribute[colon_separator_location + 1:] #sometimes colons are used besides demarcating a split between category and information, necessitating we split only on this colon.
        spell_attributes[category] = value
    return spell_attributes


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
    string = python_to_html_marker(string, '\\n', '<br>')
    string = python_to_html_marker(string, '\"', '"')#this isn't actually inherently a python marker but a work around to removing the " from earlier
    return string


def attribute_html_format(info, header=''):
    info = python_to_html(info)
    info = markdown_to_html(info)
    attribute_format = '<b>{header}</b>{information} <br>\n'
    attribute_format = attribute_format.format(header = header, information = info)
    return attribute_format


def spell_html_format():
    spell = spell_api_import()
    container = '''<div class = "header">
                        <h2 class = "heading">Learn a New Spell: {name}</h2>
                    </div>
                    <div class = "text">
                        <p>{spelldesc}<p>
                        <p style = "font-size: 24px;"><a href='{license}'>License to SRD Material</a></p>
                    </div>'''
    name = spell['name']
    spell_restrictions = '<i>{level} {school}</i> | {classes} | {archetypes}'.format(level = spell['level'], school = spell['school'],classes = spell['dnd_class'], archetypes = spell['archetype']) #puts all the spell restrictions in 1 string
    spelldesc = attribute_html_format(spell_restrictions) + '<br>' #formats spell restrictions for html
    spelldesc += attribute_html_format(spell['range'], 'Range: ')
    spelldesc += attribute_html_format(spell['duration'], 'Duration: ')
    if spell['material']: #combines components and flavortext materials line if materials line exists
        spell_components = '{components} ({materials})'.format(components = spell['components'], materials = spell['material'])
    else:
        spell_components = spell['components']
    spelldesc += attribute_html_format(spell_components, 'Components: ')
    spell_properties = 'Concentration: {concentration} | Ritual: {ritual}'.format(concentration = spell['concentration'], ritual = spell['ritual'])
    spelldesc += attribute_html_format(spell_properties)
    spelldesc += '<br>' + attribute_html_format(spell['desc']) #adds spell flavortext.
    if spell['higher_level']: #adds what happens at a higher level, if anything
        spelldesc += '<br>' + attribute_html_format(spell['higher_level'], 'At Higher Levels: ')
    spelldesc += '<br>' + attribute_html_format(spell['page'], 'Source: ')
    container = container.format(name = name, spelldesc = spelldesc, license = spell['document__license_url'])
    return container


def main():
    page = codecs.open('dependencies/index/index.html', 'r', 'utf-8').read()
    spell = spell_html_format()
    page = 'Content-type:text/html\n\n' + page.format(title='homepage', body=spell)
    print(page)


try:
    main()
except:
    print(cgi.print_exception())