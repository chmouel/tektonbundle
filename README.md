# Tekton resources Bundle

<!---
.. image:: https://img.shields.io/pypi/v/tektonbundle.svg
        :target: https://pypi.python.org/pypi/tektonbundle

.. image:: https://readthedocs.org/projects/tektonbundle/badge/?version=latest
        :target: https://tektonbundle.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
-->

A CLI to go over a bunch of Tekton yaml resources and bundle them as one in a `Pipelinerun` and `pipelineSpec`/`taskSpec`. 
It optionally can get argument to replace in tempalates.

## USAGE

```
usage: tektonbundle [-h] directory [parameters [parameters ...]]

positional arguments:
  directory   Directory where to get all the yaml files.
  parameters  Add parameters to pass to templates.

optional arguments:
  -h, --help  show this help message and exit
```

* Free software: MIT license
* Documentation: https://tektonbundle.readthedocs.io.


### Features

* TODO

