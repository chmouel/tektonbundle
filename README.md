# Tekton resources Bundle

[![Codecov](https://img.shields.io/codecov/c/github/chmouel/tektonbundle/master.svg?style=flat-square)](https://codecov.io/gh/chmouel/tektonbundle)  [![License](https://img.shields.io/pypi/l/tektonbundle.svg?style=flat-square)](https://pypi.python.org/pypi/tektonbundle) [![PYPI](https://img.shields.io/pypi/v/tektonbundle.svg?style=flat-square)](https://pypi.python.org/pypi/tektonbundle)

A CLI to go over a bunch of Tekton yaml resources and bundle them as one in a `Pipelinerun` and `pipelineSpec`/`taskSpec`.
It optionally can get argument to replace in tempalates.

## Install

```shell
pip3 install tektonbundle
```

and you are good to go!

`pyyaml` is really the external depencences here.

## Usage

You only need to point the tool to a directory and it will collect every `.yaml`
or `.yml` in there and analyze them. It will then output the 'bundled' yaml file which you can pipe to
`kubectl create`, i.e:

```shell
tektonbundle "/path/to/directory"|kubectl create -f-
```

Full help of the CLI is :

```
usage: tektonbundle [-h] directory [parameters [parameters ...]]

positional arguments:
  directory   Directory where to get all the yaml files.
  parameters  Add parameters to pass to templates.

optional arguments:
  -h, --help  show this help message and exit
```

## Description

If you have a Pipelinerun that looks like this :

```yaml
---
apiVersion: tekton.dev/v1beta1
kind: Pipelinerun
metadata:
    name: pipeline-run
spec:
    pipelineRef:
        name: pipeline
```

and a `Pipeline` named pipeline1 that looks like this :

```yaml
---
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
    name: pipeline
spec:
    tasks:
    - name: task
      taskRef:
        name: task
```

and finally a task that looks like this :

```yaml
---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: task
spec:
  steps:
    - name: step
      image: scratch
```

It will 'bundle' everything as one, using `pipelineSpec` and `taskSpec`:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  generateName: pipeline-run-
spec:
  pipelineSpec:
    tasks:
    - name: task
      taskSpec:
        steps:
        - image: scratch
          name: step
```

It will change the `name` as `generateName` to be unique.

## Substition support via parameters.

`tektonbundle` support simple template substitions if you need to specify some value before applying.

If you have the string `key: {{value}}` in your template (no spaces in between).

And you launch the CLI with this arguments :

```shell
tektonbundle /path/to/dir value="hello"
```

The value of the template would be substited with the value your provided.

If no value has been provided, it will be kept as is (you will end up with a `key: {{value}}` in your template).
