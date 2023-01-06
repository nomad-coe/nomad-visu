
# Development

The `nomad-vis` package is meant to be used in a jupyter `notebook` environment. This package using `ipywidgets` for creating the interactive elements and `plotly` and `py3Dmol` for the visualisaton of graphs and structures respectively.

## Creating python environment for development

You can use `conda`/`mamba` or `venv` to create the Python 3.10 environment. For example,
you can use the following command to create a `mamba` environment for development:

```bash
mamba create -n nomad-visu-dev python=3.10
```

Activate the environment:

```bash
mamba activate nomad-visu-dev
```

Install the  all teh requirements:

```bash
pip install -r requirements-all.txt
```

Finally install the package itself:

```bash
pip install -e .
```

## Update the development environment


Update the requirements using the following command:

```bash
pip-compile pip-compile --annotation-style=line --extra=dev --extra=docs --extra=test --output-file=requirements-all.txt pyproject.toml
```

To update the development environment, you can use the following command:

```bash
pip-sync requirements-all.txt
```

## Building the documentation

From the root of the repository, you can build the documentation using the following command:

```bash
mkdocs build
```
or having a real-time preview of the documentation using the following command:

```bash
mkdocs serve
```

<!--
## Running the tests

You can run the tests using the following command:

```bash
pytest
```
-->
