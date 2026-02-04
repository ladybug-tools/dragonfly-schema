from dragonfly_schema.shading_parameter import ExtrudedBorder, Overhang, \
    LouversByDistance, LouversByCount

import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples')


def test_shading_par_extruded_border():
    file_path = os.path.join(target_folder, 'shading_par_extruded_border.json')
    with open(file_path, 'r') as f:
        ExtrudedBorder.model_validate_json(f.read())


def test_shading_par_overhang():
    file_path = os.path.join(target_folder, 'shading_par_overhang.json')
    with open(file_path, 'r') as f:
        Overhang.model_validate_json(f.read())


def test_shading_par_louvers_by_distance():
    file_path = os.path.join(target_folder, 'shading_par_louvers_by_distance.json')
    with open(file_path, 'r') as f:
        LouversByDistance.model_validate_json(f.read())


def test_shading_par_louvers_by_count():
    file_path = os.path.join(target_folder, 'shading_par_louvers_by_count.json')
    with open(file_path, 'r') as f:
        LouversByCount.model_validate_json(f.read())
