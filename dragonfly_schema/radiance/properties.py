"""Model radiance properties."""
from pydantic import Field, constr
from typing import List, Union

from honeybee_schema._base import NoExtraBaseModel
from honeybee_schema.radiance.modifier import _REFERENCE_UNION_MODIFIERS
from honeybee_schema.radiance.modifierset import ModifierSet, ModifierSetAbridged
from honeybee_schema.radiance.global_modifierset import GlobalModifierSet

from .gridpar import RoomGridParameter, RoomRadialGridParameter, \
    ExteriorFaceGridParameter, ExteriorApertureGridParameter


class Room2DRadiancePropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^Room2DRadiancePropertiesAbridged$') = \
        'Room2DRadiancePropertiesAbridged'

    modifier_set: str = Field(
        default=None,
        description='Identifier of a ModifierSet to specify all modifiers for '
        'the Room2D. If None, the Room2D will use the Story or Building '
        'modifier_set or the Model global_modifier_set. Any ModifierSet '
        'assigned here will override those assigned to the parent objects.'
    )

    grid_parameters: List[
        Union[RoomGridParameter, RoomRadialGridParameter,
              ExteriorFaceGridParameter, ExteriorApertureGridParameter]
    ] = Field(
        default=None,
        description='An optional list of GridParameter objects to describe '
        'how sensor grids should be generated for the Room2D.'
    )


class StoryRadiancePropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^StoryRadiancePropertiesAbridged$') = \
        'StoryRadiancePropertiesAbridged'

    modifier_set: str = Field(
        default=None,
        description='Name of a ModifierSet to specify all modifiers for '
        'the Story. If None, the Story will use the Building modifier_set '
        'or the Model global_modifier_set. Any ModifierSet '
        'assigned here will override those assigned to the parent objects.'
    )


class BuildingRadiancePropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^BuildingRadiancePropertiesAbridged$') = \
        'BuildingRadiancePropertiesAbridged'

    modifier_set: str = Field(
        default=None,
        description='Name of a ModifierSet to specify all modifiers for '
        'the Building. If None, the Model global_modifier_set will be used.'
    )


class ContextShadeRadiancePropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^ContextShadeRadiancePropertiesAbridged$') = \
        'ContextShadeRadiancePropertiesAbridged'

    modifier: str = Field(
        default=None,
        description='Name of a Modifier to set the reflectance and '
        'specularity of the ContextShade. If None, the the default '
        'of 0.2 diffuse reflectance will be used.'
    )


class ModelRadianceProperties(NoExtraBaseModel):

    type: constr(regex='^ModelRadianceProperties$') = 'ModelRadianceProperties'

    global_modifier_set: GlobalModifierSet = Field(
        default=GlobalModifierSet(),
        description='Global Radiance modifier set.',
        readOnly=True
    )

    modifier_sets: List[Union[ModifierSetAbridged, ModifierSet]] = Field(
        default=None,
        description='List of all ModifierSets in the Model.'
    )

    modifiers: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=None,
        description='A list of all unique modifiers in the model. This includes '
        'modifiers across all the Model modifier_sets.'
    )
