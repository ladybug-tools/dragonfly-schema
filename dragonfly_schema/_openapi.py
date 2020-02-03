from pkg_resources import get_distribution
from pydantic.schema import schema
from typing import Dict


# base open api dictionary for all schemas
_base_open_api = {
    "openapi": "3.0.2",
    "servers": [],
    "info": {
        "description": "",
        "version": '.'.join(get_distribution('dragonfly_schema').version.split('.')[:3]),
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
    },
    "externalDocs": {
        "description": "See how to use these schema in action.",
        "url": "https://api.pollination.cloud/"
    },
    "tags": [],
    "x-tagGroups": [
        {
            "name": "Models",
            "tags": []
        }
    ],
    "paths": {},
    "components": {"schemas": {}}
}


def get_openapi(
    base_object,
    title: str = None,
    version: str = None,
    openapi_version: str = "3.0.2",
    description: str = None,
    ) -> Dict:
    """Return Dragonfly Schema as an openapi compatible dictionary."""
    open_api = dict(_base_open_api)

    open_api['openapi'] = openapi_version

    if title:
        open_api['info']['title'] = title

    if version:
        open_api['info']['version'] = version

    if description:
        open_api['info']['description'] = description

    definitions = schema(base_object, ref_prefix='#/components/schemas/')

    # goes to tags
    tags = []
    # goes to x-tagGroups['tags']
    tag_names = []

    schemas = definitions['definitions']
    schema_names = list(schemas.keys())
    schema_names.sort()
    for name in schema_names:
        model_name = '%s_model' % name.lower()
        tag_names.append(model_name)
        tag = {
            'name': model_name,
            'x-displayName': name,
            'description': '<SchemaDefinition schemaRef=\"#/components/schemas/%s\" />\n' % name
        }
        tags.append(tag)

    tag_names.sort()
    open_api['tags'] = tags
    open_api['x-tagGroups'][0]['tags'] = tag_names

    open_api['components']['schemas'] = schemas

    return open_api


if __name__ == '__main__':
    get_openapi()
