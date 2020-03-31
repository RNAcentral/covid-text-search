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

import click

from covid.sequence import parser
from covid.search_index import writer


@click.group()
def cli():
    """
    Command for dealing with generating COVID data.
    """
    pass


@cli.command('search-index')
@click.argument('genbank', type=click.File('r'))
@click.argument('output', type=click.File('a'))
def search_index(genbank, output):
    data = parser.parse(genbank)
    writer.write(data, output)
