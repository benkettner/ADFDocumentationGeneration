"""Generates a markdown (md) documentation of an Azure Data Factory. 

The ADF-files need to be downloaded and in a folder that is available from 
the current folder. Output will be markdown files for each documented entity 
as well as a combined documentation (if not deactivated via args).

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

import pathlib
import argparse
import logging
import os.path
import json
from os import path
import read_datasets
import read_pipelines

__author__ = "Benjamin Kettner"
__copyright__ = "Copyright 2020, ML!PA Consulting GbmH"
__credits__ = ["Benjamin Kettner"]
__license__ = "LGPL v3"
__version__ = "0.0.9"
__maintainer__ = "Benjamin Kettner"
__email__ = "benjamin.kettner@ml-pa.com"
__status__ = "Development"


def document_adf(args):
  """Iterates the files of the Azure Data Factory and creates markdown files from their contents. 

  Parameters
  ----------
  args : object
    The parsed command line arguments. 
  """

  if args.scrubprevious: 
    [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]
    [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]
    [p.unlink() for p in pathlib.Path('.').rglob('*.md') if 'README.md' not in str(p)]

  if args.datasets:
    datasets_file = open(args.datasets_md_file_name, 'a')
    datasets_file.write('# Datasets \n')
    datasets_file.close()

    logging.info('Parsing datasets')
    for root, subdirs, files in os.walk(os.path.join(args.adf_path, 'dataset')):
      logging.info('processing ' + root)
      for filename in files:
        current_file_path = os.path.join(root, filename)
        read_datasets.read_dataset(dataset_file_name=current_file_path, markdown_file_name=args.datasets_md_file_name)
            
  if args.pipelines:
    pipelines_file = open(args.pipelines_md_file_name, 'w')
    pipelines_file.write('# Pipelines \n')
    pipelines_file.close()

    logging.info('Parsing pipelines')
    for root, subdirs, files in os.walk(os.path.join(args.adf_path, 'pipeline')):
      logging.info('processing ' + root)
      for filename in files:
        current_file_path = os.path.join(root, filename)
        read_pipelines.read_pipeline(pipeline_file_name=current_file_path, markdown_file_name=args.pipelines_md_file_name)

  if args.triggers:
    logging.info('Parsing triggers')
    raise NotImplementedError('not implemented yet')
  
  logging.info('done, merging output files')
  data_all = data_pipelines = data_datasets = data_triggers = "" 
  
  if args.combine: 
    logging.info("Combining output files into one document")
    if args.pipelines:
      with open(args.pipelines_md_file_name, 'r') as fp: 
        data_pipelines = fp.read() 
    # Reading data from file2 
    if args.datasets:
      with open(args.datasets_md_file_name, 'r') as fp: 
        data_datasets = fp.read() 

    if args.triggers:
      with open(args.combined_md_file_name, 'r') as fp:
        data_triggers = fp.read()

    data_all += data_pipelines
    data_all += "\n"
    data_all += data_datasets 
    data_all += "\n"
    data_all += data_triggers 
  
    with open (args.combined_md_file_name, 'w') as fp: 
      fp.write(data_all) 

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Document Azure Data Factory.')
  requiredNamed = parser.add_argument_group('required arguments')
  requiredNamed.add_argument('-a', '--adfpath', 
    dest='adf_path', 
    help='Path to the Azure data factory directory',
    required=True)

  parser.add_argument('-d', '--datasets', 
    help='Use to create documentation of datasets',
    action='store_true')

  parser.add_argument('--datasetsfile',
    help='Filename of the markdown file for the datasets documentation',
    dest='datasets_md_file_name',
    default='datasets.md')

  parser.add_argument('-p', '--pipelines', 
    help='Use to create documentation of pipelines',
    action='store_true')
  
  parser.add_argument('--pipelinesfile',
    help='Filename of the markdown file for the pipelines documentation',
    dest='pipelines_md_file_name',
    default='pipelines.md')

  parser.add_argument('-t', '--triggers', 
    help='Use to create documentation of triggers',
    action='store_true')

  parser.add_argument('--triggersfile',
    help='Filename of the markdown file for the triggers documentation',
    dest='triggers_md_file_name',
    default='triggers.md')
  
  parser.add_argument('-c', '--combine', 
    help='Combine individual documentation into one file',
    action='store_true')
  
  parser.add_argument('--outputfile',
    help='Filename of the markdown file for the combined documentation',
    dest='combined_md_file_name',
    default='documentation.md')

  parser.add_argument('-l', '--loglevel',
    help='Sets the verbosity of the outoput set to INFO, WARNING or ERROR',
    dest='loglevel', 
    default='warning')

  parser.add_argument('-s', '--scrubprevious',
    help='Removes files created in previous run',
    action='store_true')

  args = parser.parse_args()

  numeric_level = getattr(logging, args.loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % args.loglevel)
  
  if not path.exists(args.adf_path):
    raise ValueError('Path %s does not exist' % args.adf_path)

  logging.basicConfig(level=numeric_level)

  document_adf(args)
