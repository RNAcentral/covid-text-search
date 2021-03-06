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

from covid.ncbi import _parser as parser

import pytest


@pytest.mark.parametrize('filename,count', [
    ('test_data/example1.gbff', 1),
    ('test_data/1xjr-a.gbff', 1),
    ('test_data/collection-date-year.gbff', 1),
])
def test_can_parse_initial_example(filename, count):
    with open(filename, 'r') as raw:
        assert len(list(parser.parse(filename))) == count


def test_can_parse_initial_example():
    with open('test_data/example1.gbff', 'r') as raw:
        data =  list(parser.parse(raw))
        assert data[0] == {
            'id': 'MT111896.1',
            'accession': 'MT111896',
            'name': 'MT111896.1',
            'description': 'Severe acute respiratory syndrome coronavirus 2 isolate SARS-CoV-2/QLD05/human/2020_FSS918/AUS ORF3a (orf3a) and envelope protein (E) genes, partial cds',
            'dates': {
                'collection_date': 'February 2020',
            },
            'cross_references': [
                {'name': 'ena', 'key': 'MT111896.1'},
                {'name': 'ncbi_taxonomy_id', 'key': '2697049'},
            ],
            'additional_fields': {
                'isolate': 'SARS-CoV-2/QLD05/human/2020_FSS918/AUS',
                'isolation_source': 'sputum',
                'country': 'Australia',
                'location': 'Australia: Queensland',
                'sequencing_method': 'Sanger dideoxy sequencing',
                'host': 'Homo sapiens',
                'popular_species': 'True',
            },
        }


def test_can_parse_without_dates():
    with open('test_data/1xjr-a.gbff', 'r') as raw:
        data =  list(parser.parse(raw))
        assert data[0] == {
            'id': '1XJR_A',
            'accession': '1XJR_A',
            'name': '1XJR_A',
            'description': 'Chain A, S2m Rna',
            'dates': {},
            'cross_references': [
                {'key': '1XJR_A', 'name': 'ena'},
                {'name': 'ncbi_taxonomy_id', 'key': '742000'},
            ],
            'additional_fields': {
                'isolate': 'unknown',
                'isolation_source': 'unknown',
                'country': 'unknown',
                'location': 'unknown',
                'sequencing_method': 'unknown',
                'host': 'unknown',
                'popular_species': 'False',
            },
        }
