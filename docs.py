"""generate openapi docs."""
from honeybee_schema._openapi import get_openapi, class_mapper
from dragonfly_schema.model import Model

import json
import argparse
from pkg_resources import get_distribution

parser = argparse.ArgumentParser(description='Generate OpenAPI JSON schemas')

parser.add_argument('--version',
                    help='Set the version of the new OpenAPI Schema')

args = parser.parse_args()

VERSION = None

if args.version:
    VERSION = args.version.replace('v', '')
else:
    VERSION = '.'.join(get_distribution('dragonfly_schema').version.split('.')[:3])

info = {
    "description": "",
    "version": VERSION,
    "title": "",
    "contact": {
        "name": "Ladybug Tools",
        "email": "info@ladybug.tools",
        "url": "https://github.com/ladybug-tools/dragonfly-core"
    },
    "x-logo": {
        "url": "https://www.ladybug.tools/assets/img/dragonfly-large.png",
        "altText": "Dragonfly logo"
    },
    "license": {
        "name": "MIT",
        "url": "https://github.com/ladybug-tools/dragonfly-schema/blob/master/LICENSE"
    }
}

# generate Model open api schema
print('Generating Model documentation...')

external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./model_inheritance.json"
}

openapi = get_openapi(
    [Model],
    title='Dragonfly Model Schema',
    description='This is the documentation for Dragonfly model schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
# set the version default key in the Model schema
openapi['components']['schemas']['Model']['properties']['version']['default'] = VERSION
with open('./docs/model.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# with inheritance
openapi = get_openapi(
    [Model],
    title='Dragonfly Model Schema',
    description='This is the documentation for Dragonfly model schema.',
    version=VERSION, info=info,
    inheritance=True,
    external_docs=external_docs
)
# set the version default key in the Model schema
openapi['components']['schemas']['Model']['allOf'][1]['properties']['version']['default'] = VERSION
with open('./docs/model_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# add the mapper file
with open('./docs/model_mapper.json', 'w') as out_file:
    json.dump(class_mapper([Model]), out_file, indent=2)
