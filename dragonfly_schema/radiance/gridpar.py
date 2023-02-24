"""Grid Parameters with instructions for generating SensorGrids."""
from pydantic import Field, constr
from typing import Union, List
from enum import Enum

from honeybee_schema._base import NoExtraBaseModel
from honeybee_schema.altnumber import Autocalculate


class _GridParameterBase(NoExtraBaseModel):
    """Base object for all GridParameters."""

    dimension: float = Field(
        ...,
        gt=0,
        description='The dimension of the grid cells as a number.'
    )

    include_mesh: bool = Field(
        True,
        description='A boolean to note whether the resulting SensorGrid should '
        'include the mesh.'
    )


class RoomGridParameter(_GridParameterBase):
    """Instructions for a SensorGrid generated from a Room2D's floors."""

    type: constr(regex='^RoomGridParameter$') = 'RoomGridParameter'

    offset: float = Field(
        1.0,
        description='A number for how far to offset the grid from the Room2D floors. '
        '(Default: 1.0, suitable for Models in Meters).'
    )

    wall_offset: float = Field(
        0,
        gt=0,
        description='A number for the distance at which sensors close to walls '
        'should be removed. Note that this option has no effect unless the '
        'value is more than half of the dimension.'
    )


class RoomRadialGridParameter(RoomGridParameter):
    """Instructions for a SensorGrid of radial directions around positions from floors.

    This type of sensor grid is particularly helpful for studies of multiple
    view directions, such as imageless glare studies.
    """

    type: constr(regex='^RoomRadialGridParameter$') = 'RoomRadialGridParameter'

    offset: float = Field(
        1.2,
        description='A number for how far to offset the grid from the Room2D floors. '
        '(Default: 1.2, suitable for Models in Meters).'
    )

    dir_count: int = Field(
        8,
        gt=0,
        description='A positive integer for the number of radial directions '
        'to be generated around each position.'
    )

    start_vector: List[float] = Field(
        None,
        description='A vector as 3 (x, y, z) values to set the start direction of '
        'the generated directions. This can be used to orient the resulting sensors to '
        'specific parts of the scene. It can also change the elevation of the '
        'resulting directions since this start vector will always be rotated in '
        'the XY plane to generate the resulting directions.',
        min_items=3,
        max_items=3
    )

    mesh_radius: Union[Autocalculate, float] = Field(
        Autocalculate(),
        ge=0,
        description='An optional number to override the radius of the meshes '
        'generated around each sensor. If Autocalculate, it will be '
        'equal to 45 percent of the grid dimension.'
    )


class ExteriorFaceType(str, Enum):

    wall = 'Wall'
    roof = 'Roof'
    floor = 'Floor'
    all = 'All'


class ExteriorFaceGridParameter(_GridParameterBase):
    """Instructions for a SensorGrid generated from exterior Faces."""

    type: constr(regex='^ExteriorFaceGridParameter$') = 'ExteriorFaceGridParameter'

    offset: float = Field(
        0.1,
        description='A number for how far to offset the grid from the Faces. '
        '(Default: 0.1, suitable for Models in Meters).'
    )

    face_type: ExteriorFaceType = Field(
        ExteriorFaceType.wall,
        description='Text to specify the type of face that will be used to '
        'generate grids. Note that only Faces with Outdoors boundary '
        'conditions will be used, meaning that most Floors will typically '
        'be excluded unless they represent the underside of a cantilever.'
    )

    punched_geometry: bool = Field(
        False,
        description='A boolean to note whether the punched_geometry of the faces '
        'should be used (True) with the areas of sub-faces removed from the grid '
        'or the full geometry should be used (False).'
    )


class ExteriorApertureType(str, Enum):

    window = 'Window'
    skylight = 'Skylight'
    all = 'All'


class ExteriorApertureGridParameter(_GridParameterBase):
    """Instructions for a SensorGrid generated from exterior Aperture."""

    type: constr(regex='^ExteriorApertureGridParameter$') = \
        'ExteriorApertureGridParameter'

    offset: float = Field(
        0.1,
        description='A number for how far to offset the grid from the Apertures. '
        '(Default: 0.1, suitable for Models in Meters).'
    )

    aperture_type: ExteriorApertureType = Field(
        ExteriorApertureType.all,
        description='Text to specify the type of Aperture that will be used to '
        'generate grids. Window indicates Apertures in Walls. Skylights '
        'are in parent Roof faces.'
    )
