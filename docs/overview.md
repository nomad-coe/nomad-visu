# Overview


Goals and principles



## Quick example

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



## Details of the features

- fractional data

- convex hull

- molecular visualiser



## Citation


