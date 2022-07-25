"""Model schema and the 3 geometry objects that define it."""
from pydantic import BaseModel, Field, root_validator, constr, conlist
from typing import List, Union

from honeybee_schema._base import IDdBaseModel
from honeybee_schema.model import Face3D, Units
from honeybee_schema.boundarycondition import Ground, Outdoors, Adiabatic, Surface
from honeybee_schema.altnumber import Autocalculate

from .window_parameter import SingleWindow, SimpleWindowRatio, RepeatingWindowRatio, \
    RectangularWindows, DetailedWindows
from .shading_parameter import ExtrudedBorder, Overhang, LouversByDistance, \
    LouversByCount
from .energy.properties import Room2DEnergyPropertiesAbridged, \
    StoryEnergyPropertiesAbridged, BuildingEnergyPropertiesAbridged, \
    ContextShadeEnergyPropertiesAbridged, ModelEnergyProperties


class Room2DPropertiesAbridged(BaseModel):

    type: constr(regex='^Room2DPropertiesAbridged$') = 'Room2DPropertiesAbridged'

    energy: Room2DEnergyPropertiesAbridged = Field(
        default=None
    )


class Room2D(IDdBaseModel):

    type: constr(regex='^Room2D$') = 'Room2D'

    floor_boundary: List[conlist(float, min_items=2, max_items=2)] = Field(
        ...,
        min_items=3,
        description='A list of 2D points representing the outer boundary vertices of '
        'the Room2D. The list should include at least 3 points and each point '
        'should be a list of 2 (x, y) values.'
    )

    floor_holes: List[conlist(conlist(float, min_items=2, max_items=2), min_items=3)] \
        = Field(
        None,
        description='Optional list of lists with one list for each hole in the floor '
        'plate. Each hole should be a list of at least 2 points and each point a list '
        'of 2 (x, y) values. If None, it will be assumed that there are no '
        'holes in the floor plate.'
    )

    floor_height: float = Field(
        ...,
        description='A number to indicate the height of the floor plane in the Z axis.'
    )

    floor_to_ceiling_height: float = Field(
        ...,
        description='A number for the distance between the floor and the ceiling.'
    )

    is_ground_contact: bool = Field(
        False,
        description='A boolean noting whether this Room2D has its floor in contact '
        'with the ground.'
    )

    is_top_exposed: bool = Field(
        False,
        description='A boolean noting whether this Room2D has its ceiling exposed '
        'to the outdoors.'
    )

    boundary_conditions: List[Union[Ground, Outdoors, Adiabatic, Surface]] = Field(
        default=None,
        description='A list of boundary conditions that match the number of segments '
        'in the input floor_geometry + floor_holes. These will be used to assign '
        'boundary conditions to each of the walls of the Room in the resulting '
        'model. Their order should align with the order of segments in the '
        'floor_boundary and then with each hole segment. If None, all boundary '
        'conditions will be Outdoors or Ground depending on whether ceiling '
        'height of the room is at or below 0 (the assumed ground plane).'
    )

    window_parameters: List[Union[None, SingleWindow, SimpleWindowRatio,
                                  RepeatingWindowRatio, RectangularWindows,
                                  DetailedWindows]] = Field(
        default=None,
        description='A list of WindowParameter objects that dictate how the window '
        'geometries will be generated for each of the walls. If None, no windows '
        'will exist over the entire Room2D.'
    )

    shading_parameters: List[Union[None, ExtrudedBorder, Overhang, LouversByDistance,
                                   LouversByCount]] = Field(
        default=None,
        description='A list of ShadingParameter objects that dictate how the shade '
        'geometries will be generated for each of the walls. If None, no shades '
        'will exist over the entire Room2D.'
    )

    air_boundaries: List[bool] = Field(
        default=None,
        description='A list of booleans for whether each wall has an air boundary type. '
        'False values indicate a standard opaque type while True values indicate '
        'an AirBoundary type. All walls will be False by default. Note that any '
        'walls with a True air boundary must have a Surface boundary condition '
        'without any windows.'
    )

    properties: Room2DPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )

    @root_validator
    def check_segment_count(cls, values):
        "Ensure len of boundary_conditions, window par, shading par match segment count."
        floor_bound = values.get('floor_boundary')
        floor_holes = values.get('floor_holes')
        bcs = values.get('boundary_conditions')
        win_par = values.get('window_parameters')
        shd_par = values.get('shading_parameters')
        air_bnd = values.get('air_boundaries')

        seg_count = len(floor_bound) if floor_holes is None\
            else len(floor_bound) + sum(len(hole) for hole in floor_holes)

        if bcs is not None:
            assert len(bcs) == seg_count, 'Length of Room2D boundary_conditions ' \
                'must match number of floor segments. {} != {}'.format(
                    len(bcs), seg_count)
        if win_par is not None:
            assert len(win_par) == seg_count, 'Length of Room2D window_parameters ' \
                'must match number of floor segments. {} != {}'.format(
                    len(win_par), seg_count)
        if shd_par is not None:
            assert len(shd_par) == seg_count, 'Length of Room2D shading_parameters ' \
                'must match number of floor segments. {} != {}'.format(
                    len(shd_par), seg_count)
        if air_bnd is not None:
            assert len(air_bnd) == seg_count, 'Length of Room2D air_boundaries ' \
                'must match number of floor segments. {} != {}'.format(
                    len(air_bnd), seg_count)
        return values


class StoryPropertiesAbridged(BaseModel):

    type: constr(regex='^StoryPropertiesAbridged$') = 'StoryPropertiesAbridged'

    energy: StoryEnergyPropertiesAbridged = Field(
        default=None
    )


class Story(IDdBaseModel):

    type: constr(regex='^Story$') = 'Story'

    room_2ds: List[Room2D] = Field(
        ...,
        description='An array of dragonfly Room2D objects that together form an '
        'entire story of a building.'
    )

    floor_to_floor_height: Union[Autocalculate, float] = Field(
        Autocalculate(),
        description='A number for the distance from the floor plate of this story '
        'to the floor of the story above this one (if it exists). If Autocalculate, '
        'this value will be the maximum floor_to_ceiling_height of the input room_2ds.'
    )

    floor_height: Union[Autocalculate, float] = Field(
        Autocalculate(),
        description='A number to indicate the height of the floor plane in the Z axis.'
        'If Autocalculate, this will be the minimum floor height of all the room_2ds, '
        'which is suitable for cases where there are no floor plenums.'
    )

    multiplier: int = Field(
        1,
        ge=1,
        description='An integer that denotes the number of times that this Story is '
        'repeated over the height of the building.'
    )

    properties: StoryPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )


class BuildingPropertiesAbridged(BaseModel):

    type: constr(regex='^BuildingPropertiesAbridged$') = 'BuildingPropertiesAbridged'

    energy: BuildingEnergyPropertiesAbridged = Field(
        default=None
    )


class Building(IDdBaseModel):

    type: constr(regex='^Building$') = 'Building'

    unique_stories: List[Story] = Field(
        ...,
        description='An array of unique dragonfly Story objects that together form '
        'the entire building. Stories should generally be ordered from lowest '
        'floor to highest floor. Note that, if a given Story is repeated several '
        'times over the height of the building, the unique story included in this '
        'list should be the first (lowest) story of the repeated floors.'
    )

    properties: BuildingPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )


class ContextShadePropertiesAbridged(BaseModel):

    type: constr(regex='^ContextShadePropertiesAbridged$') = \
        'ContextShadePropertiesAbridged'

    energy: ContextShadeEnergyPropertiesAbridged = Field(
        default=None
    )


class ContextShade(IDdBaseModel):

    type: constr(regex='^ContextShade$') = 'ContextShade'

    geometry: List[Face3D] = Field(
        ...,
        description='An array of planar Face3Ds that together represent the '
        'context shade.'
    )

    is_detached: bool = Field(
        True,
        description='Boolean to note whether this shade is detached from any of '
        'the other geometry in the model. Cases where this should be True include '
        'shade representing surrounding buildings or context.'
    )

    properties: ContextShadePropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )


class ModelProperties(BaseModel):

    type: constr(regex='^ModelProperties$') = 'ModelProperties'

    energy: ModelEnergyProperties = Field(
        default=None
    )


class Model(IDdBaseModel):

    type: constr(regex='^Model$') = 'Model'

    version: str = Field(
        default='0.0.0',
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the current version of the schema.'
    )

    buildings: List[Building] = Field(
        ...,
        description='A list of Buildings in the model.'
    )

    context_shades: List[ContextShade] = Field(
        None,
        description='A list of ContextShades in the model.'
    )

    units: Units = Field(
        default=Units.meters,
        description='Text indicating the units in which the model geometry exists. '
        'This is used to scale the geometry to the correct units for simulation '
        'engines like EnergyPlus, which requires all geometry be in meters.'
    )

    tolerance: float = Field(
        default=0.01,
        ge=0,
        description='The maximum difference between x, y, and z values at which '
        'vertices are considered equivalent. This value should be in the Model '
        'units and is used in a variety of checks and operations. A value of 0 '
        'will result in bypassing all checks so it is recommended that this always '
        'be a positive number when checks have not already been performed '
        'on a Model. The default of 0.01 is suitable for models in meters.'
    )

    angle_tolerance: float = Field(
        default=1.0,
        ge=0,
        description='The max angle difference in degrees that vertices are '
        'allowed to differ from one another in order to consider them colinear. '
        'This value is used in a variety of checks and operations that can be '
        'performed on geometry. A value of 0 will result in no checks and '
        'an inability to perform certain operations so it is recommended that '
        'this always be a positive number when checks have not already '
        'been performed on a given Model.'
    )

    properties: ModelProperties = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )
