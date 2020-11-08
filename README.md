[![Build Status](https://travis-ci.com/ladybug-tools/dragonfly-schema.svg?branch=master)](https://travis-ci.com/ladybug-tools/dragonfly-schema)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/dragonfly-schema/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/dragonfly-schema)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

# dragonfly-schema

Dragonfly Data-Model Objects

## Installation

```console
pip install dragonfly-schema
```

## QuickStart

```python
import dragonfly_schema

```

## API Documentation

[Model Schema](https://ladybug-tools.github.io/dragonfly-schema/model.html)

[Energy Simulation Parameter Schema](https://ladybug-tools-in2.github.io/honeybee-schema/simulation-parameter.html)

## Local Development

1. Clone this repo locally

```console
git clone git@github.com:ladybug-tools/dragonfly-schema

# or

git clone https://github.com/ladybug-tools/dragonfly-schema
```

2. Install dependencies:

```console
cd dragonfly-schema
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:

```console
python -m pytest tests/
```

4. Generate Documentation:

```python
python ./docs.py
```

5. Generate Sample Files:

```python
python ./scripts/export_samples.py
```
