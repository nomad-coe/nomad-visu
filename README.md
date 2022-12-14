# NOMAD-visu:

[![Tests](https://github.com/nomad-coe/nomad-visu/actions/workflows/python-package.yml/badge.svg)](https://github.com/nomad-coe/nomad-visu/actions/workflows/python-package.yml)
[![Docs](https://github.com/nomad-coe/nomad-visu/actions/workflows/python-mkdocs.yml/badge.svg)](https://nomad-coe.github.io/nomad-visu/)

A Python package for atomistic data visualisation

## Installation

You can install using `pip`:

```bash
pip install nomad-visu
```

## Quick start

Visualize octet binaries:

```python
import pandas as pd
from nomad_lab_visualizer import Visualizer
```

Load the data:

```python
df = pd.read_pickle('examples/octet_binaries/df')

regr_line_coefs = [0.11425013108281612, -1.48249992475763]
intercept = -0.1447151781886926
```

Define the features for the plots:

```python
features = ['((|IP_B  - EA_B |) / (r_p_A^2))', '((|r_s_A - r_p_B|) / exp(r_s_A))']
```

Finally display the visualizer:

```python
visualizer = Visualizer(
    df,
    features,
    features,
    target="Classification",
    #   path_to_structures='./octet_binaries/structures',
    regr_line_coefs=[regr_line_coefs, intercept],
    smart_fract=True,
    convex_hull=True,
)
visualizer.show()
```

## Development installation

Create a python environment for development:
```bash
mamba create -n nomad-visu-dev -c conda-forge python pip jupyter jupyterlab plotly ipywidgets py3dmol numpy scipy pandas scikit-learn setuptools pip-tools black mypy pytest flake8
mamba activate nomad-visu-dev
```

Install the python package in editable mode (i.e. setuptools "develop mode") from a local project path (`.`).
```bash
pip install -e ".[dev,test,docs]"
```
Run the python tests:
```bash
py.test
```
