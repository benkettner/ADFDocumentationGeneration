# ADF Documentation Generation 

## General 
This is a small tool to help you generate human-readable documentation of your Azure 
Data Factory (see [official documentation](https://docs.microsoft.com/en-us/azure/data-factory/)) solutions.
It is intended to help you generate markdown (see [e.g. here](https://www.markdownguide.org/basic-syntax/)) 
documentation for different entities in your data factory.

At the moment it contains only pipelines and datasets and pulls only limited information from 
these files, but it is intended to show the idea and grow with your needs, so if you have further needs, 
feel free to add to this solution. 

This tool is licensed under the [LGPL v3](https://www.gnu.org/licenses/lgpl-3.0.html), so use it, extend it, 
fork it and work with it. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Usage
For this tool, several parameters can be passed, the parameters are detailled below. 

| Parameter | Shorthand | Usage | Required | Default |
|---|---|---|---|---|
|`--adfpath`|`-a`| Path to the Azure data factory directory| yes | |
|`--datasets`|`-d`|Use to create documentation of datasets| no | False |
|`--datasetsfile`| |Filename of the markdown file for the datasets documentation| no | `datasets.md`|
|`--pipelines`|`-p`|Use to create documentation of pipelines| no | False |
|`--pipelinesfile`| | Filename of the markdown file for the pipelines documentation| no | `pipelines.md`|
|`--triggers`|`-t`|Use to create documentation of triggers| no | False |
|`--triggersfile`| | Filename of the markdown file for the triggers documentation | no | `triggers.md`|
|`--combine`|`-c`| Combine individual documentation into one file | no | False|
|`--outputfile`| | Filename of the markdown file for the combined documentation | no | `documentation.md`|
|`--scrubprevious`|`-s` | Removes files created in previous run | no | False |
|`--loglevel`|`-l`|Sets the verbosity of the outoput set to INFO, WARNING or ERROR | no | `warning`|


Sample call:

```python .\generate_adf_documentation.py --pipelines --datasets -a ~/ADF_dir/ -l INFO -c```
