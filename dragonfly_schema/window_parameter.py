"""Window Parameters with instructions for generating windows."""
from pydantic import Field, root_validator, constr, conlist, confloat
from typing import List

from honeybee_schema._base import NoExtraBaseModel


class SingleWindow(NoExtraBaseModel):
    """A single window in the wall center defined by a width * height."""

    type: constr(regex='^SingleWindow$') = 'SingleWindow'

    width: float = Field(
        ...,
        gt=0,
        description='A number for the window width. Note that, if this width is '
        'applied to a wall that is too narrow for this width, the generated '
        'window will automatically be shortened when it is applied to the wall. '
        'In this way, setting the width to be `float("inf")` will create '
        'parameters that always generate a ribbon window.'
    )

    height: float = Field(
        ...,
        gt=0,
        description='A number for the window height. Note that, if this height is '
        'applied to a wall that is too short for this height, the generated '
        'window will automatically be shortened when it is applied to the wall.'
    )

    sill_height: float = Field(
        1.0,
        gt=0,
        description='A number for the window sill height.'
    )


class SimpleWindowRatio(NoExtraBaseModel):
    """A single window defined by an area ratio with the base surface."""

    type: constr(regex='^SimpleWindowRatio$') = 'SimpleWindowRatio'

    window_ratio: float = Field(
        ...,
        gt=0,
        lt=1,
        description='A number between 0 and 1 for the ratio between the window '
        'area and the parent wall surface area.'
    )


class RepeatingWindowRatio(NoExtraBaseModel):
    """Repeating windows derived from an area ratio with the base wall."""

    type: constr(regex='^RepeatingWindowRatio$') = 'RepeatingWindowRatio'

    window_ratio: float = Field(
        ...,
        gt=0,
        lt=1,
        description='A number between 0 and 1 for the ratio between the window '
        'area and the parent wall surface area.'
    )

    window_height: float = Field(
        ...,
        gt=0,
        description='A number for the target height of the windows. Note that, '
        'if the window ratio is too large for the height, the ratio will take '
        'precedence and the actual window_height will be larger than this value.'
    )

    sill_height: float = Field(
        ...,
        gt=0,
        description='A number for the target height above the bottom edge of the '
        'wall to start the windows. Note that, if the ratio is too large '
        'for the height, the ratio will take precedence and the sill_height '
        'will be smaller than this value.'
    )

    horizontal_separation: float = Field(
        ...,
        ge=0,
        description='A number for the target separation between individual window '
        'centerlines.  If this number is larger than the parent rectangle base, '
        'only one window will be produced.'
    )

    vertical_separation: float = Field(
        0,
        ge=0,
        description='An optional number to create a single vertical separation '
        'between top and bottom windows.'
    )


class RepeatingWindowWidthHeight(NoExtraBaseModel):
    """Repeating rectangular windows of a fixed width and height."""

    type: constr(regex='^RepeatingWindowWidthHeight$') = 'RepeatingWindowWidthHeight'

    window_height: float = Field(
        ...,
        gt=0,
        description='A number for the target height of the windows. Note that, '
        'if the window_height is larger than the height of the wall, '
        'the generated windows will have a height equal to the wall height '
        'in order to avoid having windows extend outside the wall face.'
    )

    window_width: float = Field(
        ...,
        gt=0,
        description='A number for the target width of the windows. '
        'Note that, if the window_width is larger than the width of the wall, '
        'the generated windows will have a width equal to the wall width '
        'in order to avoid having windows extend outside the wall face.'
    )

    sill_height: float = Field(
        ...,
        gt=0,
        description='A number for the target height above the bottom edge of the '
        'wall to start the windows. If the window_height is too large for the '
        'sill_height to fit within the rectangle, the window_height will take '
        'precedence.'
    )

    horizontal_separation: float = Field(
        ...,
        ge=0,
        description='A number for the target separation between individual window '
        'centerlines.  If this number is larger than the parent rectangle base, '
        'only one window will be produced.'
    )


class RectangularWindows(NoExtraBaseModel):
    """Several rectangular windows, defined by origin, width and height."""

    type: constr(regex='^RectangularWindows$') = 'RectangularWindows'

    origins: List[conlist(confloat(gt=0), min_items=2, max_items=2)] = Field(
        ...,
        min_items=1,
        description='An array of 2D points within the plane of the wall for the origin '
        'of each window. Each point should be a list of 2 (x, y) values. The '
        'wall plane is assumed to have an origin at the first point of the wall '
        'segment and an X-axis extending along the length of the segment. The '
        'wall plane Y-axis always points upwards. Therefore, both X and Y '
        'values of each origin point should be positive.'
    )

    widths: List[confloat(gt=0)] = Field(
        ...,
        min_items=1,
        description='An array of positive numbers for the window widths. '
        'The length of this list must match the length of the origins.'
    )

    heights: List[confloat(gt=0)] = Field(
        ...,
        min_items=1,
        description='An array of positive numbers for the window heights. '
        'The length of this list must match the length of the origins.'
    )

    @root_validator
    def check_aligned_lists(cls, values):
        "Ensure length of origins, widths and heights match."
        origins = values.get('origins')
        widths = values.get('widths')
        heights = values.get('heights')

        assert len(origins) == len(widths) == len(heights), 'Length of ' \
            'RectangularWindows origins, widths, and heights ' \
            'must match. origins: {}, widths: {}, heights: {}'.format(
                len(origins), len(widths), len(heights))

        return values


class DetailedWindows(NoExtraBaseModel):
    """Several detailed windows defined by 2D Polygons (lists of 2D vertices)."""

    type: constr(regex='^DetailedWindows$') = 'DetailedWindows'

    polygons: List[conlist(conlist(confloat(gt=0), min_items=2, max_items=2), min_items=3)] = \
        Field(
        ...,
        description='An array of arrays with each sub-array representing a polygonal '
            'boundary of a window within the plane of the wall. Each sub-array should '
            'consist of at least three 2D points and each point should be a list of '
            '2 (x, y) values. The wall plane is assumed to have an origin at the '
            'first point of the wall segment and an X-axis extending along the '
            'length of the segment. The wall plane Y-axis always points upwards. '
            'Therefore, both X and Y values of each point in the polygon should '
            'always be positive. Note that, if you are starting from 3D vertices '
            'of windows, you can use these window parameters to represent them. '
            'Some sample code to convert from 2D vertices to 2D vertices in the '
            'plane of the wall can be found here: '
            'https://www.ladybug.tools/dragonfly-core/docs/dragonfly.windowparameter.html#dragonfly.windowparameter.DetailedWindows'
    )
