from dragonfly_schema.window_parameter import SingleWindow, SimpleWindowRatio, \
    RepeatingWindowRatio, RectangularWindows, DetailedWindows
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'dragonfly_schema', 'samples')


def test_window_par_single_window():
    file_path  = os.path.join(target_folder, 'window_par_single_window.json')
    SingleWindow.parse_file(file_path)


def test_window_par_simple_window_ratio():
    file_path  = os.path.join(target_folder, 'window_par_simple_window_ratio.json')
    SimpleWindowRatio.parse_file(file_path)


def test_window_par_repeating_window_ratio():
    file_path  = os.path.join(target_folder, 'window_par_repeating_window_ratio.json')
    RepeatingWindowRatio.parse_file(file_path)


def test_window_par_detailed_rectangular_windows():
    file_path  = os.path.join(target_folder, 'window_par_detailed_rectangular_windows.json')
    RectangularWindows.parse_file(file_path)


def test_window_par_detailed_windows():
    file_path  = os.path.join(target_folder, 'window_par_detailed_windows.json')
    DetailedWindows.parse_file(file_path)
