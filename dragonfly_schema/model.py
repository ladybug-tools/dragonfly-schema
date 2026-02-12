"""Model schema and the 3 geometry objects that define it."""
from pydantic import BaseModel, Field, model_validator
from typing import List, Union, Literal, Annotated
from enum import Enum

from honeybee_schema._base import IDdBaseModel
from honeybee_schema.model import Room, Face3D, Mesh3D, Units
from honeybee_schema.boundarycondition import Ground, Outdoors, Surface, \
    Adiabatic, OtherSideTemperature
from honeybee_schema.altnumber import Autocalculate

from .window_parameter import SingleWindow, SimpleWindowArea, SimpleWindowRatio, \
    RepeatingWindowRatio, RectangularWindows, DetailedWindows
from .shading_parameter import ExtrudedBorder, Overhang, LouversByDistance, \
    LouversByCount
from .skylight_parameter import GriddedSkylightArea, GriddedSkylightRatio, \
    DetailedSkylights
from .roof import RoofSpecification
from .energy.properties import Room2DEnergyPropertiesAbridged, \
    StoryEnergyPropertiesAbridged, BuildingEnergyPropertiesAbridged, \
    ContextShadeEnergyPropertiesAbridged, ModelEnergyProperties
from .radiance.properties import Room2DRadiancePropertiesAbridged, \
    StoryRadiancePropertiesAbridged, BuildingRadiancePropertiesAbridged, \
    ContextShadeRadiancePropertiesAbridged, ModelRadianceProperties
from .doe2.properties import Room2DDoe2Properties, ModelDoe2Properties
from .comparison.properties import Room2DComparisonProperties, ModelComparisonProperties


class Room2DPropertiesAbridged(BaseModel):

    type: Literal['Room2DPropertiesAbridged'] = 'Room2DPropertiesAbridged'

    energy: Union[Room2DEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[Room2DRadiancePropertiesAbridged, None] = Field(
        default=None
    )

    doe2: Union[Room2DDoe2Properties, None] = Field(
        default=None
    )

    comparison: Union[Room2DComparisonProperties, None] = Field(
        default=None
    )


class Room2D(IDdBaseModel):

    type: Literal['Room2D'] = 'Room2D'

    floor_boundary: Annotated[
        List[Annotated[List[float], Field(min_length=2, max_length=2)]], Field(min_length=3)
    ] = Field(
        ...,
        description='A list of 2D points representing the outer boundary vertices of '
        'the Room2D. The list should include at least 3 points and each point '
        'should be a list of 2 (x, y) values.'
    )

    floor_holes: Union[
        List[Annotated[List[Annotated[List[float], Field(min_length=2, max_length=2)]],
                       Field(min_length=3)]], None
    ] = Field(
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

    has_floor: bool = Field(
        True,
        description='A boolean for whether the room has a Floor (True) or an '
        'AirBoundary (False). If False, this property will only be meaningful if the '
        'model is translated to Honeybee with ceiling adjacency solved and there '
        'is a Room2D below this one with a has_ceiling property set to False.'
    )

    has_ceiling: bool = Field(
        True,
        description='A boolean for whether the room has a RoofCeiling (True) or an '
        'AirBoundary (False). If False, this property will only be meaningful if the '
        'model is translated to Honeybee with ceiling adjacency solved and there '
        'is a Room2D above this one with a has_floor property set to False.'
    )

    ceiling_plenum_depth: float = Field(
        0,
        ge=0,
        description='A number for the depth that a ceiling plenum extends into '
        'the room. Setting this to a positive value will result in a separate '
        'plenum room being split off of the Room2D volume during translation '
        'from Dragonfly to Honeybee. The bottom of this ceiling plenum will '
        'always be at this Room2D ceiling height minus the value specified here. '
        'Setting this to zero indicates that the room has no ceiling plenum.'
    )

    floor_plenum_depth: float = Field(
        0,
        ge=0,
        description='A number for the depth that a floor plenum extends into '
        'the room. Setting this to a positive value will result in a separate '
        'plenum room being split off of the Room2D volume during translation '
        'from Dragonfly to Honeybee. The top of this floor plenum will always '
        'be at this Room2D floor height plus the value specified here. '
        'Setting this to zero indicates that the room has no floor plenum.'
    )

    zone: Union[str, None] = Field(
        default=None,
        description='Text string for for the zone identifier to which this Room2D '
        ' belongs. Room2Ds sharing the same zone identifier are considered part of the '
        'same zone in a Building. If the zone identifier has not been specified, it will '
        'be the same as the Room2D identifier in the destination engine. Note that this '
        'property has no character restrictions.'
    )

    boundary_conditions: Union[List[
        Union[Ground, Outdoors, Surface, Adiabatic, OtherSideTemperature]
    ], None] = Field(
        default=None,
        description='A list of boundary conditions that match the number of segments '
        'in the input floor_geometry + floor_holes. These will be used to assign '
        'boundary conditions to each of the walls of the Room in the resulting '
        'model. Their order should align with the order of segments in the '
        'floor_boundary and then with each hole segment. If None, all boundary '
        'conditions will be Outdoors or Ground depending on whether ceiling '
        'height of the room is at or below 0 (the assumed ground plane).'
    )

    window_parameters: Union[List[Union[
        None, SingleWindow, SimpleWindowArea, SimpleWindowRatio, RepeatingWindowRatio,
        RectangularWindows, DetailedWindows
    ]], None] = Field(
        default=None,
        description='A list of WindowParameter objects that dictate how the window '
        'geometries will be generated for each of the walls. If None, no windows '
        'will exist over the entire Room2D.'
    )

    shading_parameters: Union[List[Union[
        None, ExtrudedBorder, Overhang, LouversByDistance, LouversByCount
    ]], None] = Field(
        default=None,
        description='A list of ShadingParameter objects that dictate how the shade '
        'geometries will be generated for each of the walls. If None, no shades '
        'will exist over the entire Room2D.'
    )

    air_boundaries: Union[List[bool], None] = Field(
        default=None,
        description='A list of booleans for whether each wall has an air boundary type. '
        'False values indicate a standard opaque type while True values indicate '
        'an AirBoundary type. All walls will be False by default. Note that any '
        'walls with a True air boundary must have a Surface boundary condition '
        'without any windows.'
    )

    skylight_parameters: Union[
        None, GriddedSkylightArea, GriddedSkylightRatio, DetailedSkylights
    ] = Field(
        default=None,
        description='A SkylightParameter object describing how to generate skylights. '
        'If None, no skylights will exist on the Room2D.'
    )

    properties: Room2DPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )

    @model_validator(mode='after')
    def check_segment_count(self):
        "Ensure len of boundary_conditions, window par, shading par match segment count."
        floor_bound = self.floor_boundary
        floor_holes = self.floor_holes
        bcs = self.boundary_conditions
        win_par = self.window_parameters
        shd_par = self.shading_parameters
        air_bnd = self.air_boundaries

        seg_count = len(floor_bound) if floor_holes is None else \
            len(floor_bound) + sum(len(hole) for hole in floor_holes)

        if bcs is not None:
            assert len(bcs) == seg_count, 'Length of Room2D boundary_conditions ' \
                f'must match number of floor segments. {len(bcs)} != {seg_count}'
        if win_par is not None:
            assert len(win_par) == seg_count, 'Length of Room2D window_parameters ' \
                f'must match number of floor segments. {len(win_par)} != {seg_count}'
        if shd_par is not None:
            assert len(shd_par) == seg_count, 'Length of Room2D shading_parameters ' \
                f'must match number of floor segments. {len(shd_par)} != {seg_count}'
        if air_bnd is not None:
            assert len(air_bnd) == seg_count, 'Length of Room2D air_boundaries ' \
                f'must match number of floor segments. {len(air_bnd)} != {seg_count}'
        return self


class StoryType(str, Enum):
    standard = 'Standard'
    ceiling_plenum = 'CeilingPlenum'
    floor_plenum = 'FloorPlenum'


class StoryPropertiesAbridged(BaseModel):

    type: Literal['StoryPropertiesAbridged'] = 'StoryPropertiesAbridged'

    energy: Union[StoryEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[StoryRadiancePropertiesAbridged, None] = Field(
        default=None
    )


class Story(IDdBaseModel):

    type: Literal['Story'] = 'Story'

    room_2ds: List[Room2D] = Field(
        ...,
        description='An array of dragonfly Room2D objects that together form an '
        'entire story of a building.'
    )

    floor_to_floor_height: Union[Autocalculate, float] = Field(
        Autocalculate(),
        ge=0,
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

    roof: Union[RoofSpecification, None] = Field(
        default=None,
        description='An optional RoofSpecification object containing geometry '
        'for generating sloped roofs over the Story. The RoofSpecification will only '
        'affect the child Room2Ds that have a True is_top_exposed property '
        'and it will only be utilized in translation to Honeybee when the Story '
        'multiplier is 1. If None, all Room2D ceilings will be flat.'
    )

    story_type: StoryType = Field(
        StoryType.standard,
        description='Text to indicate the type of story. Stories that are plenums '
        'are translated to Honeybee with excluded floor areas.'
    )

    properties: StoryPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )


class BuildingPropertiesAbridged(BaseModel):

    type: Literal['BuildingPropertiesAbridged'] = 'BuildingPropertiesAbridged'

    energy: Union[BuildingEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[BuildingRadiancePropertiesAbridged, None] = Field(
        default=None
    )


class Building(IDdBaseModel):

    type: Literal['Building'] = 'Building'

    unique_stories: Union[List[Story], None] = Field(
        default=None,
        description='An array of unique dragonfly Story objects that together form '
        'the entire building. Stories should generally be ordered from lowest '
        'floor to highest floor, though this is not required. Note that, if a '
        'given Story is repeated several times over the height of the building '
        'and this is represented by the multiplier, the unique story included in this '
        'list should be the first (lowest) story of the repeated floors.'
    )

    room_3ds: Union[List[Room], None] = Field(
        default=None,
        description='An optional array of 3D Honeybee Room objects for additional '
        'Rooms that are a part of the Building but are not represented within '
        'the unique_stories. This is useful when there are parts of the Building '
        'geometry that cannot easily be represented with the extruded floor '
        'plate and sloped roof assumptions that underlie Dragonfly Room2Ds '
        'and RoofSpecification. Cases where this input is most useful include '
        'sloped walls and certain types of domed roofs that become tedious to '
        'implement with RoofSpecification. Matching the Honeybee Room.story '
        'property to the Dragonfly Story.display_name of an object within the '
        'unique_stories will effectively place the Honeybee Room on that Story '
        'for the purposes of floor_area, exterior_wall_area, etc. However, note '
        'that the Honeybee Room.multiplier property takes precedence over '
        'whatever multiplier is assigned to the Dragonfly Story that the '
        'Room.story may reference. (Default: None).'
    )

    roof: Union[RoofSpecification, None] = Field(
        default=None,
        description='An optional RoofSpecification object that provides an '
        'alternative way to describe roof geometry over rooms (instead of '
        'specifying roofs on each story). If trying to decide between the two, '
        'specifying geometry on each story is closer to how dragonfly natively '
        'works with roof geometry as it relates to rooms. However, when it is '
        'unknown which roof geometries correspond to which stories, this Building-level '
        'attribute may be used and each roof geometry will automatically be added '
        'to the best Story in the Building upon serialization to Python. This '
        'automatic assignment will happen by checking for overlaps between the '
        'Story Room2Ds and the Roof geometry in plan. When a given roof geometry '
        'overlaps with several Stories, the top-most Story will get the roof geometry '
        'assigned to it unless this top Story has a floor_height above the roof '
        'geometry, in which case the next highest story will be checked until a '
        'compatible one is found.'
    )

    properties: BuildingPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )


class ContextShadePropertiesAbridged(BaseModel):

    type: Literal['ContextShadePropertiesAbridged'] = 'ContextShadePropertiesAbridged'

    energy: Union[ContextShadeEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[ContextShadeRadiancePropertiesAbridged, None] = Field(
        default=None
    )


class ContextShade(IDdBaseModel):

    type: Literal['ContextShade'] = 'ContextShade'

    geometry: List[Union[Face3D, Mesh3D]] = Field(
        ...,
        description='An array of planar Face3Ds and or Mesh3Ds that together '
        'represent the context shade.'
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

    type: Literal['ModelProperties'] = 'ModelProperties'

    energy: Union[ModelEnergyProperties, None] = Field(
        default=None
    )

    radiance: Union[ModelRadianceProperties, None] = Field(
        default=None
    )

    doe2: Union[ModelDoe2Properties, None] = Field(
        default=None
    )

    comparison: Union[ModelComparisonProperties, None] = Field(
        default=None
    )


class Model(IDdBaseModel):

    type: Literal['Model'] = 'Model'

    version: str = Field(
        default='0.0.0',
        pattern=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the current version of the schema.'
    )

    buildings: Union[List[Building], None] = Field(
        None,
        description='A list of Buildings in the model.'
    )

    context_shades: Union[List[ContextShade], None] = Field(
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

    reference_vector: Union[
        Annotated[List[float], Field(min_length=3, max_length=3)], None
    ] = Field(
        None,
        description='A n optional list of 3 (x, y, z) values that describe a Vector3D '
        'relating the model to an original source coordinate system. Setting a value '
        'here is useful if the model has been moved from its original location '
        'and there may be future operations of merging geometry from the original '
        'source system.'
    )

    properties: ModelProperties = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )
