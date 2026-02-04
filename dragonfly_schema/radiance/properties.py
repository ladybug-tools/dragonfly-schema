"""Model radiance properties."""
from pydantic import Field
from typing import List, Union, Literal

from honeybee_schema._base import NoExtraBaseModel
from honeybee_schema.radiance.modifier import _REFERENCE_UNION_MODIFIERS
from honeybee_schema.radiance.modifierset import ModifierSet, ModifierSetAbridged
from honeybee_schema.radiance.global_modifierset import GlobalModifierSet

from .gridpar import RoomGridParameter, RoomRadialGridParameter, \
    ExteriorFaceGridParameter, ExteriorApertureGridParameter


class Room2DRadiancePropertiesAbridged(NoExtraBaseModel):

    type: Literal['Room2DRadiancePropertiesAbridged'] = 'Room2DRadiancePropertiesAbridged'

    modifier_set: Union[str, None] = Field(
        default=None,
        description='Identifier of a ModifierSet to specify all modifiers for '
        'the Room2D. If None, the Room2D will use the Story or Building '
        'modifier_set or the Model global_modifier_set. Any ModifierSet '
        'assigned here will override those assigned to the parent objects.'
    )

    grid_parameters: Union[List[
        Union[RoomGridParameter, RoomRadialGridParameter,
              ExteriorFaceGridParameter, ExteriorApertureGridParameter]
    ], None] = Field(
        default=None,
        description='An optional list of GridParameter objects to describe '
        'how sensor grids should be generated for the Room2D.'
    )


class StoryRadiancePropertiesAbridged(NoExtraBaseModel):

    type: Literal['StoryRadiancePropertiesAbridged'] = 'StoryRadiancePropertiesAbridged'

    modifier_set: Union[str, None] = Field(
        default=None,
        description='Name of a ModifierSet to specify all modifiers for '
        'the Story. If None, the Story will use the Building modifier_set '
        'or the Model global_modifier_set. Any ModifierSet '
        'assigned here will override those assigned to the parent objects.'
    )


class BuildingRadiancePropertiesAbridged(NoExtraBaseModel):

    type: Literal['BuildingRadiancePropertiesAbridged'] = 'BuildingRadiancePropertiesAbridged'

    modifier_set: Union[str, None] = Field(
        default=None,
        description='Name of a ModifierSet to specify all modifiers for '
        'the Building. If None, the Model global_modifier_set will be used.'
    )


class ContextShadeRadiancePropertiesAbridged(NoExtraBaseModel):

    type: Literal['ContextShadeRadiancePropertiesAbridged'] = 'ContextShadeRadiancePropertiesAbridged'

    modifier: Union[str, None] = Field(
        default=None,
        description='Name of a Modifier to set the reflectance and '
        'specularity of the ContextShade. If None, the the default '
        'of 0.2 diffuse reflectance will be used.'
    )


class ModelRadianceProperties(NoExtraBaseModel):

    type: Literal['ModelRadianceProperties'] = 'ModelRadianceProperties'

    global_modifier_set: GlobalModifierSet = Field(
        default=GlobalModifierSet(),
        description='Global Radiance modifier set.',
        json_schema_extra={'readOnly': True}
    )

    modifier_sets: Union[List[Union[ModifierSetAbridged, ModifierSet]], None] = Field(
        default=None,
        description='List of all ModifierSets in the Model.'
    )

    modifiers: Union[List[_REFERENCE_UNION_MODIFIERS], None] = Field(
        default=None,
        description='A list of all unique modifiers in the model. This includes '
        'modifiers across all the Model modifier_sets.'
    )
