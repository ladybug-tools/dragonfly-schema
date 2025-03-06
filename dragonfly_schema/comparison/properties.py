"""Model comparison properties."""
from pydantic import Field, constr, conlist
from typing import List, Union

from honeybee_schema._base import NoExtraBaseModel

from ..window_parameter import SingleWindow, SimpleWindowArea, SimpleWindowRatio, \
    RepeatingWindowRatio, RectangularWindows, DetailedWindows
from ..skylight_parameter import GriddedSkylightArea, GriddedSkylightRatio, \
    DetailedSkylights


class Room2DComparisonProperties(NoExtraBaseModel):

    type: constr(regex='^Room2DComparisonProperties$') = \
        'Room2DComparisonProperties'

    floor_boundary: List[conlist(float, min_items=2, max_items=2)] = Field(
        None,
        min_items=3,
        description='A list of 2D points representing the outer boundary vertices of '
        'the Room2D to which the host Room2D is being compared. The list should '
        'include at least 3 points and each point should be a list of 2 (x, y) values.'
    )

    floor_holes: List[conlist(conlist(float, min_items=2, max_items=2), min_items=3)] \
        = Field(
        None,
        description='Optional list of lists with one list for each hole in the floor '
        'plate of the Room2D to which the host Room2D is being compared. Each hole '
        'should be a list of at least 2 points and each point a list '
        'of 2 (x, y) values. If None, it will be assumed that there are no '
        'holes in the floor plate.'
    )

    comparison_windows: List[Union[
        None, SingleWindow, SimpleWindowArea, SimpleWindowRatio, RepeatingWindowRatio,
        RectangularWindows, DetailedWindows
    ]] = Field(
        default=None,
        description='A list of WindowParameter objects that dictate the window '
        'geometries of the Room2D to which the host Room2D is being compared.'
    )

    comparison_skylight: Union[
        None, GriddedSkylightArea, GriddedSkylightRatio, DetailedSkylights
    ] = Field(
        default=None,
        description='A SkylightParameter object for the Room2D to which the host '
        'Room2D is being compared.'
    )


class ModelComparisonProperties(NoExtraBaseModel):

    type: constr(regex='^ModelComparisonProperties$') = 'ModelComparisonProperties'
