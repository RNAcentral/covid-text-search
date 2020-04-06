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

from pathlib import Path

import pytest
from Bio import SeqIO

from covid.ncbi import _fetch as fetch


@pytest.mark.parametrize('filename,ans', [
    ('test_data/beta-sample.fasta', [
        'AY606204.1',
        'DQ355402.1',
        'EU401988.1',
        'JN234472.1',
        'JQ732189.1',
        'KR607988.1',
        'KT002194.1',
        'KX034097.1',
        'LC506938.1',
        'MT159715.1',
    ])
])
def test_can_get_all_ids(filename, ans):
    with open(filename, 'r') as raw:
        assert fetch.extract_ids(raw) == ans


def test_can_generate_expected_filename():
    ids = [
            'AY606204.1',
            'DQ355402.1',
            'EU401988.1',
            'JN234472.1',
            'JQ732189.1',
            'KR607988.1',
            'KT002194.1',
            'KX034097.1',
            'LC506938.1',
            'MT159715.1',
        ]
    val = fetch.filename(Path('here'), ids)
    assert val == Path('here/87485c1da2d2201cae06cb1d2c6aec5c.gbff')


def test_can_fetch_a_set_of_ids():
    ids = ['AY606204.1', 'DQ355402.1', 'MT159715.1']
    raw = fetch.query_ncbi(ids)
    val = set(r.id for r in SeqIO.parse(raw, 'genbank'))
    assert val == set(ids)


def test_can_validate():
    ids = ['MT111896.1', 'DQ355402.1']
    path = Path('test_data/example1.gbff')
    with pytest.raises(AssertionError):
        fetch.validate(path, ids)
