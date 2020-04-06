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

import click

from covid import ncbi
from covid import nextstrain
from covid.search_index import writer
from covid.blast import fetch as blast


@click.group()
def cli():
    """
    Command for dealing with generating COVID data.
    """
    pass

@cli.command('update')
@click.option('--data', default='data', type=click.Path(dir_okay=True, file_okay=False))
@click.argument('nextstrain-metadata', default='data/nextstrain.tsv', type=click.File('r'))
@click.argument('output', default='current.xml', type=click.File('w'))
def cli_update(nextstrain_metadata, output, data=None):
    dir = Path(data)
    fasta = blast.fetch(dir)
    genbank = ncbi.fetch(fasta, dir)
    sequences = ncbi.parse(genbank)
    strains = nextstrain.index(nextstrain_metadata)
    writer.write(sequences, strains, output)



@cli.command('blast-db')
@click.argument('output', default='data', type=click.Path(dir_okay=True, file_okay=False))
def cli_blast_db(output):
    blast.fetch(Path(output))


@cli.command('fetch')
@click.argument('fasta', type=click.File('r'))
@click.argument('output', default='data', type=click.Path(dir_okay=True, file_okay=False))
def cli_fetch(fasta, output):
    ncbi.fetch.fetch(fasta, Path(output))


@cli.command('search-index')
@click.argument('genbank', type=click.File('r'))
@click.argument('output', type=click.File('a'))
def search_index(genbank, output):
    data = ncbi.parser.parse(genbank)
    writer.write(data, output)
