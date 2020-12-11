# coding=utf-8
import pytest

from dragonfly.model import Model
from dragonfly.building import Building
from dragonfly.story import Story
from dragonfly.room2d import Room2D
from dragonfly.context import ContextShade
from dragonfly.windowparameter import SimpleWindowRatio
from dragonfly.shadingparameter import Overhang

from honeybee.boundarycondition import boundary_conditions as bcs

from honeybee_energy.constructionset import ConstructionSet
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.construction.shade import ShadeConstruction
from honeybee_energy.material.opaque import EnergyMaterial
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.load.lighting import Lighting

from honeybee_energy.lib.programtypes import office_program, plenum_program
import honeybee_energy.lib.scheduletypelimits as schedule_types
from honeybee_energy.lib.materials import roof_membrane, wood, insulation

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.face import Face3D

import os
import json


def model_complete_simple(directory):
    """Generate simple Model sample."""
    pts_1 = (Point3D(0, 0, 3), Point3D(0, 10, 3), Point3D(10, 10, 3), Point3D(10, 0, 3))
    pts_2 = (Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(20, 10, 3), Point3D(20, 0, 3))
    room2d_1 = Room2D('Office1', Face3D(pts_1), 3)
    room2d_2 = Room2D('Office2', Face3D(pts_2), 3)
    story = Story('OfficeFloor', [room2d_1, room2d_2])
    story.solve_room_2d_adjacency(0.01)
    story.set_outdoor_window_parameters(SimpleWindowRatio(0.4))
    story.multiplier = 4
    for room in story.room_2ds:
        room.properties.energy.program_type = office_program
        room.properties.energy.add_default_ideal_air()
    building = Building('OfficeBuilding', [story])
    building.separate_top_bottom_floors()

    attic_program_type = plenum_program.duplicate()
    attic_program_type.identifier = 'Attic Space'
    schedule = ScheduleRuleset.from_constant_value(
        'Always Dim', 1, schedule_types.fractional)
    lighting = Lighting('Attic Lighting', 3, schedule)
    attic_program_type.lighting = lighting
    building.unique_room_2ds[-1].properties.energy.program_type = attic_program_type
    building.unique_room_2ds[-2].properties.energy.program_type = attic_program_type

    constr_set = ConstructionSet('Attic Construction Set')
    polyiso = EnergyMaterial('PolyIso', 0.2, 0.03, 43, 1210, 'MediumRough')
    roof_constr = OpaqueConstruction('Attic Roof Construction',
                                     [roof_membrane, polyiso, wood])
    floor_constr = OpaqueConstruction('Attic Floor Construction',
                                      [wood, insulation, wood])
    constr_set.floor_set.interior_construction = floor_constr
    constr_set.roof_ceiling_set.exterior_construction = roof_constr
    building.unique_room_2ds[-1].properties.energy.construction_set = constr_set
    building.unique_room_2ds[-2].properties.energy.construction_set = constr_set

    tree_canopy_geo1 = Face3D.from_regular_polygon(6, 6, Plane(o=Point3D(5, -10, 6)))
    tree_canopy_geo2 = Face3D.from_regular_polygon(6, 2, Plane(o=Point3D(-5, -10, 3)))
    tree_canopy = ContextShade('TreeCanopy', [tree_canopy_geo1, tree_canopy_geo2])
    bright_leaves = ShadeConstruction('Bright Light Leaves', 0.5, 0.5, True)
    tree_canopy.properties.energy.construction = bright_leaves
    tree_trans = ScheduleRuleset.from_constant_value(
        'Tree Transmittance', 0.5, schedule_types.fractional)
    tree_canopy.properties.energy.transmittance_schedule = tree_trans

    model = Model('NewDevelopment', [building], [tree_canopy])

    dest_file = os.path.join(directory, 'model_complete_simple.dfjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def building_simple(directory):
    """Generate simple Building sample."""
    pts_1 = (Point3D(0, 0, 0), Point3D(0, 10, 0), Point3D(10, 10, 0), Point3D(10, 0, 0))
    pts_2 = (Point3D(10, 0, 0), Point3D(10, 10, 0), Point3D(20, 10, 0), Point3D(20, 0, 0))
    pts_3 = (Point3D(0, 10, 0), Point3D(0, 20, 0), Point3D(10, 20, 0), Point3D(10, 10, 0))
    pts_4 = (Point3D(10, 10, 0), Point3D(10, 20, 0), Point3D(20, 20, 0), Point3D(20, 10, 0))
    pts_5 = (Point3D(0, 0, 3), Point3D(0, 10, 3), Point3D(10, 10, 3), Point3D(10, 0, 3))
    pts_6 = (Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(20, 10, 3), Point3D(20, 0, 3))
    pts_7 = (Point3D(0, 0, 6), Point3D(0, 10, 6), Point3D(10, 10, 6), Point3D(10, 0, 6))
    room2d_1 = Room2D('Office1', Face3D(pts_1), 3)
    room2d_2 = Room2D('Office2', Face3D(pts_2), 3)
    room2d_3 = Room2D('Office3', Face3D(pts_3), 3)
    room2d_4 = Room2D('Office4', Face3D(pts_4), 3)
    room2d_5 = Room2D('Office5', Face3D(pts_5), 3)
    room2d_6 = Room2D('Office6', Face3D(pts_6), 3)
    room2d_7 = Room2D('Office7', Face3D(pts_7), 3)
    story_1 = Story('OfficeFloor1', [room2d_1, room2d_2, room2d_3, room2d_4])
    story_2 = Story('OfficeFloor2', [room2d_5, room2d_6])
    story_3 = Story('OfficeFloor3', [room2d_7])
    story_1.solve_room_2d_adjacency(0.01)
    story_2.solve_room_2d_adjacency(0.01)
    story_1.set_outdoor_window_parameters(SimpleWindowRatio(0.3))
    story_2.set_outdoor_window_parameters(SimpleWindowRatio(0.35))
    story_3.set_outdoor_window_parameters(SimpleWindowRatio(0.6))
    building = Building('OfficeBuilding', [story_1, story_2, story_3])
    building.separate_top_bottom_floors()

    dest_file = os.path.join(directory, 'building_simple.json')
    with open(dest_file, 'w') as fp:
        json.dump(building.to_dict(True), fp, indent=4)


def story_simple(directory):
    """Generate simple Story sample."""
    mass_set = ConstructionSet('Thermal Mass Construction Set')
    pts_1 = (Point3D(0, 0, 3), Point3D(0, 10, 3), Point3D(10, 10, 3), Point3D(10, 0, 3))
    pts_2 = (Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(20, 10, 3), Point3D(20, 0, 3))
    pts_3 = (Point3D(0, 10, 3), Point3D(0, 20, 3), Point3D(10, 20, 3), Point3D(10, 10, 3))
    pts_4 = (Point3D(10, 10, 3), Point3D(10, 20, 3), Point3D(20, 20, 3), Point3D(20, 10, 3))
    room2d_1 = Room2D('Office1', Face3D(pts_1), 3)
    room2d_2 = Room2D('Office2', Face3D(pts_2), 3)
    room2d_3 = Room2D('Office3', Face3D(pts_3), 3)
    room2d_4 = Room2D('Office4', Face3D(pts_4), 3)
    story = Story('OfficeFloor', [room2d_1, room2d_2, room2d_3, room2d_4])
    story.solve_room_2d_adjacency(0.01)
    story.set_outdoor_window_parameters(SimpleWindowRatio(0.4))
    story.properties.energy.construction_set = mass_set

    dest_file = os.path.join(directory, 'story_simple.json')
    with open(dest_file, 'w') as fp:
        json.dump(story.to_dict(True), fp, indent=4)


def story_air_boundary(directory):
    """Generate a story with air boundaries."""
    pts_1 = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    pts_2 = (Point3D(10, 0, 3), Point3D(20, 0, 3), Point3D(20, 10, 3), Point3D(10, 10, 3))
    room2d_1 = Room2D('SquareShoebox1', Face3D(pts_1), 3)
    room2d_2 = Room2D('SquareShoebox2', Face3D(pts_2), 3)
    adj_info = Room2D.solve_adjacency([room2d_1, room2d_2], 0.01)
    for room_pair in adj_info:
        for room_adj in room_pair:
            room, wall_i = room_adj
            air_bnd = list(room.air_boundaries)
            air_bnd[wall_i] = True
            room.air_boundaries = air_bnd
    story = Story('OfficeFloor', [room2d_1, room2d_2])

    dest_file = os.path.join(directory, 'story_air_boundary.json')
    with open(dest_file, 'w') as fp:
        json.dump(story.to_dict(True), fp, indent=4)


def room2d_simple(directory):
    """Generate simple Room2D sample."""
    mass_set = ConstructionSet('Thermal Mass Construction Set')
    pts = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    ashrae_base = SimpleWindowRatio(0.4)
    overhang = Overhang(1)
    boundarycs = (bcs.outdoors, bcs.ground, bcs.outdoors, bcs.ground)
    window = (ashrae_base, None, ashrae_base, None)
    shading = (overhang, None, None, None)
    room = Room2D('ShoeBoxZone', Face3D(pts), 3, boundarycs, window, shading)
    room.properties.energy.construction_set = mass_set
    room.properties.energy.program_type = office_program

    dest_file = os.path.join(directory, 'room2d_simple.json')
    with open(dest_file, 'w') as fp:
        json.dump(room.to_dict(True), fp, indent=4)


def context_shade_two_tree_canopy(directory):
    """Generate the context_shade_two_tree_canopy sample."""
    tree_canopy_geo1 = Face3D.from_regular_polygon(6, 6, Plane(o=Point3D(5, -10, 6)))
    tree_canopy_geo2 = Face3D.from_regular_polygon(6, 2, Plane(o=Point3D(-5, -10, 3)))
    tree_canopy = ContextShade('TreeCanopy', [tree_canopy_geo1, tree_canopy_geo2])

    bright_leaves = ShadeConstruction('Bright Light Leaves', 0.5, 0.5, True)
    tree_trans = ScheduleRuleset.from_constant_value(
        'Tree Transmittance', 0.5, schedule_types.fractional)
    
    tree_canopy.properties.energy.construction = bright_leaves
    tree_canopy.properties.energy.transmittance_schedule = tree_trans

    dest_file = os.path.join(directory, 'context_shade_two_tree_canopy.json')
    with open(dest_file, 'w') as fp:
        json.dump(tree_canopy.to_dict(True), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples')

model_complete_simple(sample_directory)
building_simple(sample_directory)
story_simple(sample_directory)
room2d_simple(sample_directory)
context_shade_two_tree_canopy(sample_directory)
