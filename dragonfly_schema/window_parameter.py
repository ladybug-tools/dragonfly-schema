"""Window Parameters with instructions for generating windows."""
from pydantic import BaseModel, Field, validator, root_validator, constr
from typing import List


class SingleWindow(BaseModel):
    """A single window in the wall center defined by a width * height."""

    type: constr(regex='^SingleWindow$') = 'SingleWindow'

    width: float = Field(
        ...,
        gt=0,
        description='A number for the window width. Note that, if this width is '
            'applied to a wall that is too narrow for this width, the generated '
            'window will automatically be shortened when it is applied to the wall. '
            'In this way, setting the width to be `float("inf")` will create '
            'parameters that always generate a ribboin window.'
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


class SimpleWindowRatio(BaseModel):
    """A single window defined by an area ratio with the base surface."""

    type: constr(regex='^SimpleWindowRatio$') = 'SimpleWindowRatio'

    window_ratio: float = Field(
        ...,
        gt=0,
        lt=1,
        description='A number between 0 and 1 for the ratio between the window '
            'area and the parent wall surface area.'
    )


class RepeatingWindowRatio(BaseModel):
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
            'rectangle to start the windows. Note that, if the ratio is too large '
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


class RectangularWindows(BaseModel):
    """Several rectangular windows, defined by origin, width and height."""

    type: constr(regex='^RectangularWindows$') = 'RectangularWindows'

    origins: List[List[float]] = Field(
        ...,
        description='An array of 2D points within the plane of the wall for the origin '
            'of each window. Each point should be a list of 2 (x, y) values. The '
            'wall plane is assumed to have an origin at the first point of the wall '
            'segment and an X-axis extending along the length of the segment. The '
            'wall plane Y-axis always points upwards. Therefore, both X and Y '
            'values of each origin point should be positive.'
    )

    widths: List[float] = Field(
        ...,
        description='An array of postive numbers for the window widths. '
            'The length of this list must match the length of the origins.'
    )

    heights: List[float] = Field(
        ...,
        description='An array of postive numbers for the window heights. '
            'The length of this list must match the length of the origins.'
    )

    @validator('origins')
    def check_num_items(cls, v):
        for i in v:
            assert len(i) == 2, 'Number of floats must be 2 for (x, y).'
            assert i[0] > 0, 'X value for WindowParameter origin must be positive.'
            assert i[1] > 0, 'Y value for WindowParameter origin must be positive.'
        return v

    @validator('widths')
    def check_positive_widths(cls, v):
        for i in v:
            assert i > 0, 'Window width must be positive.'
        return v

    @validator('heights')
    def check_positive_heights(cls, v):
        for i in v:
            assert i > 0, 'Window height must be positive.'
        return v

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


class DetailedWindows(BaseModel):
    """Several detailed windows defined by 2D Polygons (lists of 2D vertices)."""

    type: constr(regex='^DetailedWindows$') = 'DetailedWindows'

    polygons: List[List[List[float]]] = Field(
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

    @validator('polygons')
    def check_num_items(cls, v):
        for pt_list in v:
            assert len(pt_list) >= 3, \
                'DetailedWindows must have windows with at least 3 vertices.'
            for pt in pt_list:
                assert len(pt) == 2, 'Number of floats must be 2 for (x, y).'
                assert pt[0] > 0, 'X value for WindowParameter vertex must be positive.'
                assert pt[1] > 0, 'Y value for WindowParameter vertex must be positive.'
        return v
