"""Geometry for specifying sloped roofs over a Story."""
from pydantic import Field
from typing import Union, List, Literal, Annotated

from honeybee_schema._base import NoExtraBaseModel
from honeybee_schema.model import Face3D, Mesh3D

from .clearstory_parameter import DetailedClearstory


class RoofSpecification(NoExtraBaseModel):
    """Geometry for specifying sloped roofs over a Story."""

    type: Literal['RoofSpecification'] = 'RoofSpecification'

    geometry: Annotated[List[Union[Face3D, Mesh3D]], Field(min_length=1)] = Field(
        ...,
        description='An array of Face3D (or Mesh3D) objects representing the '
        'geometry of the Roof. Cases where Room2Ds are only partially covered '
        'by these roof geometries will result in those portions of the Room2Ds '
        'being extruded to their floor_to_ceiling_height.'
    )

    clearstory_parameters: Union[List[DetailedClearstory], None] = Field(
        default=None,
        description='A list of ClearstoryParameter objects that dictate how to '
        'generate window geometries for any vertical walls that result from the '
        'translation of roof geometry. If None, no clearstory windows will exist '
        'over the roof.'
    )
