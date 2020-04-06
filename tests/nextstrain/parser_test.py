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

from covid.nextstrain.parser import parse
from covid.nextstrain.parser import index

import pytest


@pytest.mark.parametrize('filename,count', [
    ('test_data/nextstrain.tsv', 9),
])
def test_can_parse_all_data(filename, count):
    with open(filename, 'r') as raw:
        assert len(list(parse(raw))) == count


def test_produces_expected_data():
    with open('test_data/nextstrain.tsv', 'r') as raw:
        data = list(parse(raw))

    assert data[0] == {
        'strain_id': 'Wuhan/WH01/2019',
        'country': 'China',
        'genbank_accession': 'LR757998',
        'gisaid_epi_isl': 'EPI_ISL_406798',
    }


def test_indexes_as_expected():
    with open('test_data/nextstrain.tsv', 'r') as raw:
        data = index(raw)
    assert data['MN996527'] == {
        'strain_id': 'Wuhan/WIV02/2019',
        'country': 'China',
        'genbank_accession': 'MN996527',
        'gisaid_epi_isl': 'EPI_ISL_402127',
    }
