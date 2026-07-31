"""Clerestory Parameters with instructions for generating clerestory windows."""
from pydantic import Field
from typing import Union, List, Literal, Annotated

from honeybee_schema._base import NoExtraBaseModel


class DetailedClerestory(NoExtraBaseModel):
    """Instructions for detailed clerestory windows, defined by 2D Polygons."""

    type: Literal['DetailedClerestory'] = 'DetailedClerestory'

    base_line: List[Annotated[List[float], Field(min_length=2, max_length=2)]] = Field(
        ...,
        min_length=2,
        max_length=2,
        description='An array of two sub-arrays with each sub-array representing '
        'the start and end point of a 2D line segment in the world XY system. '
        'This establishes the plane and domain in which the clerestory geometries exist.'
    )

    elevation: float = Field(
        ...,
        description='A number for the Z-coordinate that places the base_line and '
        'the corresponding clerestory window polygons in 3D space. This elevation '
        'value should be below all of the 3D clerestory window geometries and helps '
        'set the origin of the plane in which the clerestory geometry exists.'
    )

    polygons: List[
        Annotated[List[Annotated[List[float], Field(min_length=2, max_length=2)]],
                  Field(min_length=3)]
    ] = Field(
        ...,
        description='An array of arrays with each sub-array representing a polygonal '
        'boundary of a clerestory window or door. Each sub-array should consist of '
        'arrays representing points, which contain 2 values for 2D coordinates '
        'in the plane defined by the base_line. The base_line plane is assumed to '
        'have an origin at the end point of the line segment (the second point) '
        'and an X-axis extending along the length of the segment. The Y-axis of '
        'the plane always points upwards. Therefore, both X and Y coordinates of '
        'the points in each polygon should be positive.'
    )

    are_doors: Union[List[bool], None] = Field(
        default=None,
        description='An array of booleans that align with the polygons and note '
        'whether each of the polygons represents a door out onto a roof or '
        'balcony (True) or a clerestory window (False). If None, it will be assumed '
        'that all polygons represent windows and they will be translated to Apertures '
        'in any resulting Honeybee model'
    )
