"""Window Parameters with instructions for generating windows."""
from pydantic import BaseModel, Field, constr


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
