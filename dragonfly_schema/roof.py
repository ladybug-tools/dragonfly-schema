"""Geometry for specifying sloped roofs over a Story."""
from pydantic import Field, constr, conlist
from typing import Union

from honeybee_schema._base import NoExtraBaseModel
from honeybee_schema.model import Face3D, Mesh3D


class RoofSpecification(NoExtraBaseModel):
    """Geometry for specifying sloped roofs over a Story."""

    type: constr(regex='^RoofSpecification$') = 'RoofSpecification'

    geometry: conlist(Union[Face3D, Mesh3D], min_items=1) = Field(
        ...,
        description='An array of Face3D (or Mesh3D) objects representing the '
        'geometry of the Roof. Cases where Room2Ds are only partially covered '
        'by these roof geometries will result in those portions of the Room2Ds '
        'being extruded to their floor_to_ceiling_height.'
    )
