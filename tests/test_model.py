from dragonfly_schema.model import Room2D, Story, Building, ContextShade, Model
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples')


def test_room2d_simple():
    file_path = os.path.join(target_folder, 'room2d_simple.json')
    Room2D.parse_file(file_path)


def test_story_simple():
    file_path = os.path.join(target_folder, 'story_simple.json')
    Story.parse_file(file_path)


def test_building_simple():
    file_path = os.path.join(target_folder, 'building_simple.json')
    Building.parse_file(file_path)


def test_context_shade_two_tree_canopy():
    file_path = os.path.join(target_folder, 'context_shade_two_tree_canopy.json')
    ContextShade.parse_file(file_path)


def test_model_complete_simple():
    file_path = os.path.join(target_folder, 'model_complete_simple.dfjson')
    Model.parse_file(file_path)
