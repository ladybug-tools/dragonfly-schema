# coding=utf-8
from dragonfly.shadingparameter import ExtrudedBorder, Overhang, LouversByDistance, \
    LouversByCount

import os
import json


def shading_par_extruded_border(directory):
    simple_border = ExtrudedBorder(0.3)

    dest_file = os.path.join(directory, 'shading_par_extruded_border.json')
    with open(dest_file, 'w') as fp:
        json.dump(simple_border.to_dict(), fp, indent=4)


def shading_par_overhang(directory):
    simple_awning = Overhang(2, 10)

    dest_file = os.path.join(directory, 'shading_par_overhang.json')
    with open(dest_file, 'w') as fp:
        json.dump(simple_awning.to_dict(), fp, indent=4)


def shading_par_louvers_by_distance(directory):
    louvers = LouversByDistance(0.5, 0.3, 1, 30)

    dest_file = os.path.join(directory, 'shading_par_louvers_by_distance.json')
    with open(dest_file, 'w') as fp:
        json.dump(louvers.to_dict(), fp, indent=4)


def shading_par_louvers_by_count(directory):
    louvers = LouversByCount(3, 0.3, 1, 30)

    dest_file = os.path.join(directory, 'shading_par_louvers_by_count.json')
    with open(dest_file, 'w') as fp:
        json.dump(louvers.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples')

shading_par_extruded_border(sample_directory)
shading_par_overhang(sample_directory)
shading_par_louvers_by_distance(sample_directory)
shading_par_louvers_by_count(sample_directory)
