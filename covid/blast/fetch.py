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

import tarfile
import subprocess as sp
from pathlib import Path

import requests


def db_md5(db_name):
    response = requests.get(f'https://ftp.ncbi.nlm.nih.gov/blast/db/{db_name}.tar.gz.md5')
    response.raise_for_status()
    raw = response.text
    return raw.split()[0]


def fetch(base_path, db_name='Betacoronavirus'):
    md5 = db_md5(db_name)
    fasta = base_path / f'{md5}.fasta'
    if fasta.exists():
        return fasta

    tar_file = f'{db_name}.tar.gz'
    response = requests.get(f'https://ftp.ncbi.nlm.nih.gov/blast/db/{db_name}.tar.gz')
    with open(tar_file, 'wb') as out:
        out.write(response.content)

    with tarfile.open(tar_file) as tar:
        tar.extractall('.')
    sp.check_call(['blastdbcmd', "-entry", 'all', '-db', db_name, '-out', str(fasta)])
    return fasta
