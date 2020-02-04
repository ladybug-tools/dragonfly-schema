from dragonfly.windowparameter import SingleWindow, SimpleWindowRatio, \
    RepeatingWindowRatio, RepeatingWindowWidthHeight, RectangularWindows, \
    DetailedWindows

from ladybug_geometry.geometry2d.pointvector import Point2D
from ladybug_geometry.geometry2d.polygon import Polygon2D

import os
import json


def window_par_single_window(directory):
    simple_window = SingleWindow(5, 2, 0.8)

    dest_file = os.path.join(directory, 'window_par_single_window.json')
    with open(dest_file, 'w') as fp:
        json.dump(simple_window.to_dict(), fp, indent=4)


def window_par_simple_window_ratio(directory):
    ashrae_base = SimpleWindowRatio(0.4)

    dest_file = os.path.join(directory, 'window_par_simple_window_ratio.json')
    with open(dest_file, 'w') as fp:
        json.dump(ashrae_base.to_dict(), fp, indent=4)


def window_par_repeating_window_ratio(directory):
    ashrae_base = RepeatingWindowRatio(0.4, 2, 0.8, 3)

    dest_file = os.path.join(directory, 'window_par_repeating_window_ratio.json')
    with open(dest_file, 'w') as fp:
        json.dump(ashrae_base.to_dict(), fp, indent=4)


def window_par_repeating_window_width_height(directory):
    bod_windows = RepeatingWindowWidthHeight(2, 1.5, 0.8, 3)

    dest_file = os.path.join(directory, 'window_par_repeating_window_width_height.json')
    with open(dest_file, 'w') as fp:
        json.dump(bod_windows.to_dict(), fp, indent=4)


def window_par_detailed_rectangular_windows(directory):
    origins = (Point2D(2, 1), Point2D(5, 0.5))
    widths = (1, 3)
    heights = (1, 2)
    detailed_window = RectangularWindows(origins, widths, heights)

    dest_file = os.path.join(directory, 'window_par_detailed_rectangular_windows.json')
    with open(dest_file, 'w') as fp:
        json.dump(detailed_window.to_dict(), fp, indent=4)


def window_par_detailed_windows(directory):
    pts_1 = (Point2D(2, 1), Point2D(3, 1), Point2D(3, 2), Point2D(2, 2))
    pts_2 = (Point2D(5, 0.5), Point2D(8, 0.5), Point2D(8, 2.5), Point2D(5, 2.5))
    detailed_window = DetailedWindows((Polygon2D(pts_1), Polygon2D(pts_2)))

    dest_file = os.path.join(directory, 'window_par_detailed_windows.json')
    with open(dest_file, 'w') as fp:
        json.dump(detailed_window.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples')

window_par_single_window(sample_directory)
window_par_simple_window_ratio(sample_directory)
window_par_repeating_window_ratio(sample_directory)
window_par_repeating_window_width_height(sample_directory)
window_par_detailed_rectangular_windows(sample_directory)
window_par_detailed_windows(sample_directory)
