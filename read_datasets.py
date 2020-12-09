"""Reads a single dataset file from Azure Data Factory and appends the relevant parts 
  of its contents to an existing Markdown file. 

This file is part of ADF Documentation Generation.

ADF Documentation Generation is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Module: read_datasets.py
import logging
import json

def read_dataset(dataset_file_name, markdown_file_name):
  """Reads a single dataset file from Azure Data Factory and appends the relevant parts 
  of its contents to an existing Markdown file. 

  The following information will be contained in the resulting markdown file:

  * the name of the dataset, 
  * the type of the dataset,
  * if possible, the location (folder) where it is defined 
  * if available the schema of the dataset (schema definition is not available for all data source types)

  Parameters
  ----------
  dataset_file_name : str
    The full path of the ADF json file to be read
  markdown_file_name : str
    The full path of the markdown file to which the contents will be appended
  """

  datasets_file = open(markdown_file_name, 'a')
  logging.info('\t reading %s' % (dataset_file_name))
  with open(dataset_file_name) as json_file:
    datasets_data = json.load(json_file)
    datasets_file.write('\n\n ## %s \n' % datasets_data['name'])
    datasets_file.write('Type: %s \n' % datasets_data['properties']['type'])
    if 'folder' in datasets_data['properties']:
      datasets_file.write('\n Defined in %s \n' % datasets_data['properties']['folder']['name'])
    if 'schema' in datasets_data['properties']:
      datasets_file.write('\n\n ### Schema \n')
      datasets_file.write('\n | Name | Type | ')
      datasets_file.write('\n |---|---| ')
      if type(datasets_data['properties']['schema']) is list: 
        for val in datasets_data['properties']['schema']:
          if 'name' in val and ';' not in val['name']:
            datasets_file.write('\n |{name}|{type}| '.format(
              name=(val['name'] if 'name' in val else 'n/a'), 
              type=(val['type'] if 'type' in val else 'n/a')))
          elif 'name' not in val:
            datasets_file.write('\n |{name}|{type}| '.format(
              name='n/a', 
              type=(val['type'] if 'type' in val else 'n/a')))
          else:
            for colname in val['name'].split(';'):
              datasets_file.write('\n |{name}|{type}| '.format(
              name=colname, 
              type='string'))

      else:
        datasets_file.write('\n |{name}|{type}|'.format(
          name=(datasets_data['properties']['schema']['name'] if 'name' in datasets_data['properties']['schema'] else 'n/a'), 
          type=(datasets_data['properties']['schema']['type'] if 'type' in datasets_data['properties']['schema'] else 'n/a')))

  datasets_file.close()
