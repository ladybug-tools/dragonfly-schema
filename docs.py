"""generate openapi docs."""
from dragonfly_schema._openapi import get_openapi
from dragonfly_schema.model import Model
from honeybee_schema.energy.simulation import SimulationParameter

import json

# generate Model open api schema
print('Generating Model documentation...')
openapi = get_openapi(
    [Model],
    title='Dragonfly Model Schema',
    description='This is the documentation for Dragonfly model schema.')
with open('./docs/model.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)
