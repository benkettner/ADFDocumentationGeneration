"""Reads a single pipeline file from Azure Data Factory and appends the relevant parts 
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

def read_pipeline(pipeline_file_name, markdown_file_name):
  """Reads a single pipeline file from Azure Data Factory and appends the relevant parts 
  of its contents to an existing Markdown file. 

  The following information will be contained in the resulting markdown file:

  * the name of the pipeline
  * the description of the pipeline if available
  * a list of its activities
  * a list of its dependencies together with the dependency condition

  Parameters
  ----------
  pipeline_file_name : str
    The full path of the ADF json file to be read
  markdown_file_name : str
    The full path of the markdown file to which the contents will be appended
  """

  pipelines_file = open(markdown_file_name, 'a')
  logging.info('\t reading %s' % (pipeline_file_name))
  with open(pipeline_file_name) as json_file:
    pipelines_data = json.load(json_file)
    pipelines_file.write('\n\n ## %s \n' % pipelines_data['name'])
    if 'description' in pipelines_data['properties']:
      pipelines_file.write('\n Description: {0} \n'.format(pipelines_data['properties']['description']))
    pipelines_file.write('\n\n ### Steps \n')
    for act in pipelines_data['properties']['activities']:
      pipelines_file.write('\n * Name: __{0}__, Type: {1} \n'.format(act['name'], act['type']))
      if len(act['dependsOn']) > 0:
        pipelines_file.write('\n   Dependencies:')
        for dep in act['dependsOn']:
          pipelines_file.write('\n   * [{0}]({1}) ({2}) \n'.format(dep['activity'], '#'+dep['activity'].replace(' ', '-'), dep['dependencyConditions'][0]))
  pipelines_file.close()
