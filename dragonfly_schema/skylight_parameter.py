"""Window Parameters with instructions for generating windows."""
from pydantic import Field, constr, conlist, confloat
from typing import Union
from typing import List

from honeybee_schema._base import NoExtraBaseModel
from honeybee_schema.altnumber import Autocalculate


class GriddedSkylightRatio(NoExtraBaseModel):
    """Gridded skylights derived from an area ratio with the roof."""

    type: constr(regex='^GriddedSkylightRatio$') = 'GriddedSkylightRatio'

    window_ratio: float = Field(
        ...,
        gt=0,
        lt=0.75,
        description='A number between 0 and 0.75 for the ratio between the skylight '
        'area and the total Roof face area.'
    )

    spacing: Union[Autocalculate, float] = Field(
        Autocalculate(),
        gt=0,
        description='A number for the spacing between the centers of each grid cell. '
        'This should be less than half of the dimension of the Roof geometry '
        'if multiple, evenly-spaced skylights are desired. If Autocalculate, a spacing '
        'of one half the smaller dimension of the parent Roof will be automatically '
        'assumed.'
    )


class DetailedSkylights(NoExtraBaseModel):
    """Several detailed skylights defined by 2D Polygons (lists of 2D vertices)."""

    type: constr(regex='^DetailedSkylights$') = 'DetailedSkylights'

    polygons: List[
        conlist(conlist(confloat(gt=0), min_items=2, max_items=3), min_items=3)
    ] = Field(
        ...,
        description='An array of arrays with each sub-array representing a polygonal '
            'boundary of a skylight. Each sub-array should consist of arrays '
            'representing points, which contain 2 values for 2D coordinates in '
            'the world XY system. These coordinate values should lie within the '
            'parent Room2D Polygon.'
    )

    are_doors: List[bool] = Field(
        default=None,
        description='An array of booleans that align with the polygons and note '
        'whether each of the polygons represents an overhead door (True) or a '
        'skylight (False). If None, it will be assumed that all polygons represent '
        'skylights and they will be translated to Apertures in any resulting '
        'Honeybee model.'
    )
