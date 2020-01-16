"""Model schema and the 5 geometry objects that define it."""
from pydantic import BaseModel, Field, validator, constr
from typing import List, Union
from enum import Enum

from ._base import NamedBaseModel


class ModelProperties(BaseModel):

    type: constr(regex='^ModelProperties$') = 'ModelProperties'


class Model(NamedBaseModel):

    type: constr(regex='^Model$') = 'Model'

    north_angle: float = Field(
        default=0,
        ge=0,
        lt=360,
        description='The clockwise north direction in degrees.'
    )

    properties: ModelProperties = Field(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


if __name__ == '__main__':
    print(Model.schema_json(indent=2))
