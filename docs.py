"""generate openapi docs."""
import json
import argparse
from pkg_resources import get_distribution

from pydantic_openapi_helper.core import get_openapi
from pydantic_openapi_helper.inheritance import class_mapper
from dragonfly_schema.model import Model

parser = argparse.ArgumentParser(description='Generate OpenAPI JSON schemas')

parser.add_argument('--version', help='Set the version of the new OpenAPI Schema')

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

modules = [
    {'module': [Model], 'name': 'Model'}
]


def _process_name(name):
    """Process module name."""
    new_name = '-'.join(n.lower() for n in name.split())
    return new_name


for module in modules:
    # generate Recipe open api schema
    print(f'Generating {module["name"]} documentation...')

    external_docs = {
        "description": "OpenAPI Specification with Inheritance",
        "url": f"./{_process_name(module['name'])}_inheritance.json"
    }

    openapi = get_openapi(
        module['module'],
        title=f'Dragonfly {module["name"]} Schema',
        description=f'Dragonfly {_process_name(module["name"])} schema.',
        version=VERSION, info=info,
        external_docs=external_docs
    )

    # set the version default key in the Model schema
    if module['module'] is Model:
        openapi['components']['schemas']['Model']['properties']['version']['default'] = \
            VERSION
    with open(f'./docs/{_process_name(module["name"])}.json', 'w') as out_file:
        json.dump(openapi, out_file, indent=2)

    # with inheritance
    openapi = get_openapi(
        module['module'],
        title=f'Dragonfly {module["name"]} Schema',
        description=f'Documentation for Dragonfly {_process_name(module["name"])} schema',
        version=VERSION, info=info,
        inheritance=True,
        external_docs=external_docs
    )

    # set the version default key in the Recipe schema
    if module['module'] is Model:
        openapi['components']['schemas']['Model']['properties']['version']['default'] = \
            VERSION

    with open(f'./docs/{_process_name(module["name"])}_inheritance.json', 'w') \
            as out_file:
        json.dump(openapi, out_file, indent=2)

    # add the mapper file
    with open(f'./docs/{_process_name(module["name"])}_mapper.json', 'w') as out_file:
        json.dump(class_mapper(module['module']), out_file, indent=2)


# generate JSONSchema for Dragonfly model
with open('./docs/model_json_schema.json', 'w') as out_file:
    out_file.write(Model.schema_json(indent=2))

# generate schema for mode with inheritance but without descriminator
# we will use this file for generating redocly - the full model is too big, and the
# model with inheritance and discriminators is renders incorrectly
external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./model_inheritance.json"
}

openapi = get_openapi(
    [Model],
    title='Dragonfly Model Schema',
    description='Documentation for Dragonfly model schema',
    version=VERSION, info=info,
    inheritance=True,
    external_docs=external_docs,
    add_discriminator=False
)

with open('./docs/model_redoc.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)
