# Nomad-lab Visualizer

[![Documetation]()]()
[![Python package]()]()

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

## Development Installation

Create a dev environment:

```bash
mamba create -n nomad-lab-visualiser-dev -c conda-forge python pip jupyter jupyterlab plotly ipywidgets numpy scipy pandas scikit-learn
mamba activate nomad-lab-visualiser-dev
pip install jupyter_jsmol
```

Install the python. This will also build the TS package.

```bash
# First install the python package. This will also build the JS packages.
pip install -e ".[test]"

# Run the python tests. This should not give you a few successful example tests
py.test
```
