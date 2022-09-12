# Nomad-lab Visualizer

[![Tests](https://github.com/nomad-coe/nomad-lab-visualizer/actions/workflows/python-package.yml/badge.svg)](https://github.com/nomad-coe/nomad-lab-visualizer/actions/workflows/python-package.yml)
[![Docs](https://github.com/nomad-coe/nomad-lab-visualizer/actions/workflows/python-mkdocs.yml/badge.svg)](https://nomad-coe.github.io/nomad-lab-visualizer/)


This is plot/visualizer widget for atomistic structures which can be used in Jupyter Notebooks.

## Installation

You can install using `pip`:

```bash
pip install nomad-lab-visualiser
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
mamba create -n nomad-lab-visualiser-dev -c conda-forge python pip jupyter jupyterlab plotly ipywidgets==7.5.1 numpy scipy pandas scikit-learn setuptools pip-tools black mypy pytest flake8 notebook==6.0.0
mamba activate nomad-lab-visualiser-dev
pip install jupyter_jsmol==2021.3.0
```
Install the python package in editable mode (i.e. setuptools "develop mode") from a local project path (`.`).
```bash
pip install -e ".[test]"
```
Run the python tests:
```bash
py.test
```
