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

from datetime import datetime as dt

from Bio import SeqIO

POPULAR_SPECIES = set([
     2697049,
])

SEQUENCING_CORRECTIONS = {
    'Sanger dideoxy sequencing; Illumina': 'Illumina; Sanger dideoxy sequencing',
    'Illumian NextSeq 500': 'Illumina NextSeq 500',
    'MGISEQ 2000': 'Illumina; MGISEQ 2000',
}


def source_field(source, name, missing='unknown'):
    values = source.qualifiers.get(name, [])
    if len(values) == 0:
        return missing
    assert len(values) == 1
    return values[0]


def parse_date(raw, missing=None):
    try:
        date = dt.strptime(raw, r'%b-%Y')
    except:
        return missing
    return dt.strftime(date, r'%B %Y')


def dates(source):
    fields = [
        'collection_date',
    ]
    data = {}
    for field in fields:
        raw = source_field(source, field, missing=None)
        if raw:
            value = parse_date(raw)
            if value:
                data[field] = value
    return data


def cross_references(record, source):
    data = [ 
        {'name': 'ena', 'key': record.id},
    ]
    xrefs = source.qualifiers.get('db_xref', [])
    for xref in xrefs:
        if xref.startswith('taxon'):
            _, key = xref.split(':', 1)
            data.append({'name': 'ncbi_taxonomy_id', 'key': key})
    return data


def country(source):
    location = source_field(source, 'country')
    return location.split(':', 1)[0]


def sequencing_method(record, missing='unknown'):
    comments = record.annotations.get('structured_comment', {})
    assemblies =  comments.get('Assembly-Data', {})
    raw = assemblies.get('Sequencing Technology', missing)
    return SEQUENCING_CORRECTIONS.get(raw, raw)


def taxid(source):
    xrefs = source.qualifiers.get('db_xref', [])
    for xref in xrefs:
        if xref.startswith('taxon'):
            _, taxid = xref.split(':', 1)
            return int(taxid)


def popular_species(source):
    return str(taxid(source) in POPULAR_SPECIES)


def parse(handle):
    for record in SeqIO.parse(handle, 'genbank'):
        source = record.features[0]
        yield {
            'id': record.id,
            'accession': record.id.split('.')[0],
            'name': record.id,
            'description': record.description,
            'dates': dates(source),
            'cross_references': cross_references(record, source),
            'additional_fields': {
                'country': country(source),
                'location': source_field(source, 'country'),
                'sequencing_method': sequencing_method(record),
                'isolate': source_field(source, 'isolate'),
                'isolation_source': source_field(source, 'isolation_source'),
                'host': source_field(source, 'host'),
                'popular_species': popular_species(source),
            }
        }
