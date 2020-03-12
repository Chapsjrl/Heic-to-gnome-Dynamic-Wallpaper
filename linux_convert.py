"""
This script converts an XML metadata from extract_heic.py script to a json file for WDD and makes a .dww file
"""

import os
import sys

from bs4 import BeautifulSoup as Soup

inp_dir = sys.argv[1]


# def solar_convert(input_data, json):
# TODO: Implement this solution


def h24_convert(input_data, xml):
    # * Will use a list of tuples for de index an time
    img_time = []
    input_data.seek(0, 0)

    for string in input_data:
        if string == 'i\n':
            index = int(input_data.readline())
            input_data.readline()
            time = round(float(input_data.readline()) * 24 * 60 * 60, 1)
            img_time.append((index, time))

    # + Sorting by the hour in the day
    img_time.sort(key=lambda tuple: tuple[1])

    # ? Write the times an transitions on xml
    for i in range(len(img_time)):
        if i == len(img_time)-1:
            duration = 86400 - img_time[i][1]
            xml.write('<static>\n' +
                      f'  <duration>{duration*(2/3)}</duration>\n' +
                      f'  <file>/usr/share/backgrounds/gnome/{inp_dir}-timed/{inp_dir}_{img_time[i][0]+1}.jpg</file>\n' +
                      '</static>\n\n')

            xml.write('<transition type="overlay">\n' +
                      f'  <duration>{duration*(1/3)}</duration>\n' +
                      f'  <from>/usr/share/backgrounds/gnome/{inp_dir}-timed/{inp_dir}_{img_time[i][0]+1}.jpg</from>\n' +
                      f'  <to>/usr/share/backgrounds/gnome/{inp_dir}-timed/{inp_dir}_{img_time[0][0]+1}.jpg</to>\n' +
                      '</transition>\n\n\n')
        else:
            duration = img_time[i+1][1] - img_time[i][1]

            xml.write('<static>\n' +
                      f'  <duration>{duration*(2/3)}</duration>\n' +
                      f'  <file>/usr/share/backgrounds/gnome/{inp_dir}-timed/{inp_dir}_{img_time[i][0]+1}.jpg</file>\n' +
                      '</static>\n\n')

            xml.write('<transition type="overlay">\n' +
                      f'  <duration>{duration*(1/3)}</duration>\n' +
                      f'  <from>/usr/share/backgrounds/gnome/{inp_dir}-timed/{inp_dir}_{img_time[i][0]+1}.jpg</from>\n' +
                      f'  <to>/usr/share/backgrounds/gnome/{inp_dir}-timed/{inp_dir}_{img_time[i+1][0]+1}.jpg</to>\n' +
                      '</transition>\n\n\n')


if __name__ == "__main__":
    # ? Open metadata.xml and create out.xml
    inp = open(inp_dir + '/metadata.xml', mode='r')
    meta = Soup(inp.read(), features="lxml")
    out = open(inp_dir + '/' + inp_dir + '-timed.xml', mode='w')

    # ? Create a work and copy the bs format
    temp = open(inp_dir + '/temp.txt', mode='w+')
    temp.write(meta.get_text())
    temp.seek(0, 0)

    # + Add the theme to gnome backgrounds with this file
    template = open('Template.xml', mode='r')
    gwppr = open(inp_dir + '/' + inp_dir + '.xml', mode='w+')

    # * Replace the name of the theme in the template
    for line in template:
        o_line = line.replace('Template', inp_dir)
        gwppr.write(o_line)

    template.close()
    gwppr.close()

    # ? Start the xml file for times and transitions
    out.write('<background>\n'
              '  <starttime>\n' +
              '    <year>2020</year>\n' +
              '    <month>2</month>\n' +
              '    <day>1</day>\n' +
              '    <hour>00</hour>\n' +
              '    <minute>00</minute>\n' +
              '    <second>00</second>\n' +
              '  </starttime>\n\n\n')

    # ? Choose the kind of xml and convert
    for line in temp:
        if line.find('a\n') != -1:
            # solar_convert(temp, out)
            print("\nUNSOPPORTED YET!!")
            break
        if line.find('t\n') != -1:
            h24_convert(temp, out)
            break

    out.write('</background>\n')

    inp.close()
    out.close()
    temp.close()

    #os.remove(inp_dir + '/metadata.xml')
    os.remove(inp_dir + '/temp.txt')
