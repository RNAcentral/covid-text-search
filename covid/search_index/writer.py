# -*- coding: utf-8 -*-

"""
Copyright [2009-2020] EMBL-European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from datetime import date  as dt

from lxml import etree
from lxml.builder import E

from datetime import date

def dates(dates):
    data = []
    for name, value in dates.items():
        data.append(E.date(type=name, value=value))
    return data


def cross_references(xrefs):
    data = []
    for xref in xrefs:
        data.append(E.ref(dbkey=xref['key'], dbname=xref['name']))
    return data


def additional_fields(fields):
    data = []
    for name, value in fields.items():
        data.append(E.field(value, name=name))
    return data


def as_entry(result):
    return E.entry(
        E.name(result['name']),
        E.description(result['description']),
        E.dates(*dates(result['dates'])),
        E.cross_references(*cross_references(result['cross_references'])),
        E.additional_fields(*additional_fields(result['additional_fields'])),
        id=result['id'],
    )


def write_entries(sequences, strains, handle):
    for sequence in sequences:
        extra = strains.get(sequence['id'], {})
        sequence['additional_fields'].update(extra)

        entry = as_entry(sequence)
        xml = etree.tostring(entry).decode('utf-8')
        handle.write(xml)
        handle.write('\n')


def write_notes(count, handle):
    stamp = dt.strftime(dt.today(), "%d-%B-%Y")
    handle.write("release=14\n")
    handle.write("release_date=%s\n" % stamp)
    handle.wrte("entries=%i\n" % count)


def write(sequences, strains, output_handle, note_handle):
    """
    This will create the required root XML element and place all the given
    XmlEntry objects as ElementTree.Element's in it. This then produces the
    string representation of that document which can be saved.
    """

    # pylint: disable=no-member
    output_handle.write('<database>')
    output_handle.write(etree.tostring(E.name('COVID-2019')).decode())
    output_handle.write(etree.tostring(E.description('a search index for COVID-2019 sequences')).decode())
    output_handle.write(etree.tostring(E.release('1.0')).decode())
    output_handle.write(etree.tostring(E.release_date(date.today().strftime('%d/%m/%Y'))).decode())
    output_handle.write('\n')

    output_handle.write('<entries>')
    count = write_entries(sequences, strains, output_handle)
    output_handle.write('</entries>')
    output_handle.write('</database>')

    write_notes(count, note_handle)
