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

import hashlib
import shutil
import logging
from pathlib import Path

from Bio import SeqIO
from Bio import Entrez

from . import utils


SIZE = 200

LOGGER = logging.getLogger(__name__)

Entrez.email = 'rnacentral@gmail.com'


def extract_ids(fasta):
    ids = set()
    for record in SeqIO.parse(fasta, 'fasta'):
        ids.add(record.id)
    return sorted(ids)


def query_ncbi(ids):
    return Entrez.efetch(db='nucleotide', id=ids, rettype="gb", retmode="text")


def filename(directory, ids):
    md5 = hashlib.md5()
    for id in ids:
        md5.update(id.encode('utf8'))
    prefix = md5.hexdigest()
    return directory / f"{prefix}.gbff"


def validate(path, ids):
    required = set(ids)
    with path.open('r') as raw:
        found = set(r.id for r in SeqIO.parse(raw, 'genbank'))

    missing = required - found
    if missing:
        LOGGER.error("Missing ids: %s", missing)

    extra = found - required
    if extra:
        LOGGER.error("Extra ids: %s", extra)

    assert found == required, "Ids do not match"


def fetch(fasta, directory: Path):
    ids = extract_ids(fasta)
    path = filename(directory, ids)
    if path.exists():
        LOGGER.info("Dump file already exists, skipping")
        return None

    with path.open('w') as output:
        chunked = utils.grouper(ids, SIZE)
        for chunk in chunked:
            embl = query_ncbi(chunk)
            shutil.copyfileobj(embl, output)
    validate(path, ids)
