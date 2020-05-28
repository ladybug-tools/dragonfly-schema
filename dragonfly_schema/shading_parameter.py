"""Window Parameters with instructions for generating windows."""
from pydantic import Field, constr
from typing import List

from honeybee_schema._base import NoExtraBaseModel


class ExtrudedBorder(NoExtraBaseModel):
    """Extruded borders over all windows in the wall."""

    type: constr(regex='^ExtrudedBorder$') = 'ExtrudedBorder'

    depth: float = Field(
        ...,
        gt=0,
        description='A number for the depth of the border.'
    )


class Overhang(NoExtraBaseModel):
    """A single overhang over an entire wall."""

    type: constr(regex='^Overhang$') = 'Overhang'

    depth: float = Field(
        ...,
        gt=0,
        description='A number for the overhang depth.'
    )

    angle: float = Field(
        0,
        ge=-90,
        le=90,
        description='A number between -90 and 90 for the for an angle to rotate the '
        'overhang in degrees. 0 indicates an overhang perpendicular to the wall. '
        'Positive values indicate a downward rotation. Negative values indicate '
        'an upward rotation.'
    )


class _LouversBase(NoExtraBaseModel):
    """Base class for for a series of louvered shades over a wall."""

    depth: float = Field(
        ...,
        gt=0,
        description='A number for the depth to extrude the louvers.'
    )

    offset: float = Field(
        0,
        ge=0,
        description='A number for the distance to louvers from the wall.'
    )

    angle: float = Field(
        0,
        ge=-90,
        le=90,
        description='A number between -90 and 90 for the for an angle to rotate the '
        'louvers in degrees. 0 indicates louvers perpendicular to the wall. '
        'Positive values indicate a downward rotation. Negative values indicate '
        'an upward rotation.'
    )

    contour_vector: List[float] = Field(
        [0, 1],
        min_items=2,
        max_items=2,
        description='A list of two float values representing the (x, y) of a 2D vector '
        'for the direction along which contours are generated. (0, 1) will generate '
        'horizontal contours, (1, 0) will generate vertical contours, and (1, 1) '
        'will generate diagonal contours.'
    )

    flip_start_side: bool = Field(
        False,
        description='Boolean to note whether the side the louvers start from should '
        'be flipped. Default is False to have contours on top or right. Setting '
        'to True will start contours on the bottom or left.'
    )


class LouversByDistance(_LouversBase):
    """A series of louvered Shades at a given distance between each louver."""

    type: constr(regex='^LouversByDistance$') = 'LouversByDistance'

    distance: float = Field(
        ...,
        gt=0,
        description='A number for the approximate distance between each louver.'
    )


class LouversByCount(_LouversBase):
    """A specific number of louvered Shades over a wall."""

    type: constr(regex='^LouversByCount$') = 'LouversByCount'

    louver_count: int = Field(
        ...,
        gt=0,
        description='A positive integer for the number of louvers to generate.'
    )
