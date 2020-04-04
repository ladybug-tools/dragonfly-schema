"""Model energy properties."""
from pydantic import Field, constr
from typing import List, Union
from enum import Enum

from honeybee_schema._base import NoExtraBaseModel
from honeybee_schema.energy.constructionset import ConstructionSetAbridged, \
    ConstructionSet
from honeybee_schema.energy.programtype import ProgramTypeAbridged, ProgramType
from honeybee_schema.energy.hvac import IdealAirSystemAbridged

from honeybee_schema.energy.properties import TerrianTypes
from honeybee_schema.energy.construction import OpaqueConstructionAbridged, \
    WindowConstructionAbridged, ShadeConstruction, AirBoundaryConstructionAbridged, \
    OpaqueConstruction, WindowConstruction, AirBoundaryConstruction
from honeybee_schema.energy.material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialGlazing, EnergyWindowMaterialShade
from honeybee_schema.energy.schedule import ScheduleTypeLimit, ScheduleRulesetAbridged, \
    ScheduleFixedIntervalAbridged, ScheduleRuleset, ScheduleFixedInterval


class Room2DEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^Room2DEnergyPropertiesAbridged$') = \
        'Room2DEnergyPropertiesAbridged'

    construction_set: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ConstructionSet to specify all constructions for '
            'the Room2D. If None, the Room2D will use the Story or Building '
            'construction_set or the Model global_construction_set. Any ConstructionSet '
            'assigned here will override those assigned to these objects.'
    )

    program_type: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ProgramType to specify all schedules and loads '
            'for the Room2D. If None, the Room2D will have no loads or setpoints.'
    )

    hvac: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='An optional identifier of a HVAC system (such as an IdealAirSystem) '
            'that specifies how the Room2D is conditioned. If None, it will be assumed '
            'that the Room2D is not conditioned.'
    )


class StoryEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^StoryEnergyPropertiesAbridged$') = \
        'StoryEnergyPropertiesAbridged'

    construction_set: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ConstructionSet to specify all constructions for '
            'the Story. If None, the Story will use the Building construction_set '
            'or the Model global_construction_set. Any ConstructionSet '
            'assigned here will override those assigned to these objects.'
    )


class BuildingEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^BuildingEnergyPropertiesAbridged$') = \
        'BuildingEnergyPropertiesAbridged'

    construction_set: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ConstructionSet to specify all constructions for '
            'the Building. If None, the Model global_construction_set will be used.'
    )


class ContextShadeEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^ContextShadeEnergyPropertiesAbridged$') = \
        'ContextShadeEnergyPropertiesAbridged'

    construction:  str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ShadeConstruction to set the reflectance and '
            'specularity of the ContextShade. If None, the the EnergyPlus default '
            'of 0.2 diffuse reflectance will be used.'
    )

    transmittance_schedule: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a schedule to set the transmittance of the ContextShade, '
            'which can vary throughout the simulation. If None, the ContextShade will '
            'be completely opauqe.'
    )


class ModelEnergyProperties(NoExtraBaseModel):

    type: constr(regex='^ModelEnergyProperties$') = 'ModelEnergyProperties'

    terrain_type: TerrianTypes = Field(
        default=TerrianTypes.city,
        description='Text for the terrain in which the model sits. This is used '
            'to determine the wind profile over the height of the buildings.'
    )

    global_construction_set: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for the ConstructionSet to be used for all objects lacking '
            'their own construction or a parent construction_set. This '
            'ConstructionSet must appear under the Model construction_sets.'
    )

    construction_sets: List[Union[ConstructionSetAbridged, ConstructionSet]] = Field(
        default=None,
        description='List of all ConstructionSets in the Model.'
    )

    constructions: List[Union[
        OpaqueConstructionAbridged, WindowConstructionAbridged,
        ShadeConstruction, AirBoundaryConstructionAbridged,
        OpaqueConstruction, WindowConstruction, AirBoundaryConstruction]] = Field(
        ...,
        description='A list of all unique constructions in the model. This includes '
            'constructions across all the Model construction_sets.'
    )

    materials: List[Union[EnergyMaterial, EnergyMaterialNoMass, EnergyWindowMaterialGas,
                          EnergyWindowMaterialGasCustom, EnergyWindowMaterialGasMixture,
                          EnergyWindowMaterialSimpleGlazSys, EnergyWindowMaterialBlind,
                          EnergyWindowMaterialGlazing,
                          EnergyWindowMaterialShade]] = Field(
        ...,
        description='A list of all unique materials in the model. This includes '
            'materials needed to make the Model constructions.'
    )

    hvacs: List[Union[IdealAirSystemAbridged]] = Field(
        default=None,
        description='List of all HVAC systems in the Model.'
    )

    program_types: List[Union[ProgramTypeAbridged, ProgramType]] = Field(
        default=None,
        description='List of all ProgramTypes in the Model.'
    )

    schedules: List[Union[ScheduleRulesetAbridged, ScheduleFixedIntervalAbridged,
                          ScheduleRuleset, ScheduleFixedInterval]] = Field(
        default=None,
        description='A list of all unique schedules in the model. This includes '
            'schedules across all HVAC systems, ProgramTypes and ContextShades.'
    )

    schedule_type_limits: List[ScheduleTypeLimit] = Field(
        default=None,
        description='A list of all unique ScheduleTypeLimits in the model. This '
            'all ScheduleTypeLimits needed to make the Model schedules.'
    )
