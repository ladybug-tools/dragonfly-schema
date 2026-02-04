from dragonfly_schema.window_parameter import SingleWindow, SimpleWindowRatio, \
    RepeatingWindowRatio, RepeatingWindowWidthHeight, RectangularWindows, \
    DetailedWindows
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples')


def test_window_par_single_window():
    file_path = os.path.join(target_folder, 'window_par_single_window.json')
    with open(file_path, 'r') as f:
        SingleWindow.model_validate_json(f.read())


def test_window_par_simple_window_ratio():
    file_path = os.path.join(target_folder, 'window_par_simple_window_ratio.json')
    with open(file_path, 'r') as f:
        SimpleWindowRatio.model_validate_json(f.read())


def test_window_par_repeating_window_ratio():
    file_path = os.path.join(target_folder, 'window_par_repeating_window_ratio.json')
    with open(file_path, 'r') as f:
        RepeatingWindowRatio.model_validate_json(f.read())


def test_window_par_repeating_window_width_height():
    file_path = os.path.join(target_folder, 'window_par_repeating_window_width_height.json')
    with open(file_path, 'r') as f:
        RepeatingWindowWidthHeight.model_validate_json(f.read())


def test_window_par_detailed_rectangular_windows():
    file_path = os.path.join(target_folder, 'window_par_detailed_rectangular_windows.json')
    with open(file_path, 'r') as f:
        RectangularWindows.model_validate_json(f.read())


def test_window_par_detailed_windows():
    file_path = os.path.join(target_folder, 'window_par_detailed_windows.json')
    with open(file_path, 'r') as f:
        DetailedWindows.model_validate_json(f.read())
