from dragonfly_schema.model import Model

import sys
import os

if __name__ == '__main__':
    # check the input arguments
    assert len(sys.argv) >= 2, 'Model JSON argument not included.'
    model_json = sys.argv[1]
    assert os.path.isfile(model_json), 'No JSON file found at {}.'.format(model_json)
    
    # validate the Model JSON
    print('Validating Model JSON ...')
    Model.parse_file(model_json)
    print('Congratulations! Model JSON is valid!')
