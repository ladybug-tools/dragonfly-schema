"""Geometry for specifying sloped roofs over a Story."""
from pydantic import Field, constr
from typing import List

from honeybee_schema._base import NoExtraBaseModel
from honeybee_schema.model import Face3D


class RoofSpecification(NoExtraBaseModel):
    """Geometry for specifying sloped roofs over a Story."""

    type: constr(regex='^RoofSpecification$') = 'RoofSpecification'

    geometry: List[Face3D] = Field(
        ...,
        description='An array of Face3D objects representing the geometry of the '
        'Roof. None of these geometries should overlap in plan and, together, these '
        'Face3D should either completely cover or skip each Room2D of the Story '
        'to which the RoofSpecification is assigned.'
    )
