#!/usr/bin/env python
"""Tests for `tektonbundle` package."""
import glob
import os

import pytest
import yaml

from tektonbundle import tektonbundle


def get_key(dico, key):
    curr = dico
    for k in key.split("."):
        if k.isdigit() and isinstance(curr, list):
            curr = curr[int(k)]
            continue
        if k not in curr:
            return ""
        curr = curr[k]

    if not isinstance(curr, str):
        curr = str(curr)
    return curr


PARAM_FIXTURES = [
    (
        "pipelinerun-pipeline-task",
        [("spec.pipelineSpec.tasks.0.taskSpec.steps.0.name", "first-step")],
        {},
    ),
    (
        "pipelinerun-pipeline-task",
        [("spec.params.0.value", "thatizzevalue")],
        {
            "value": "thatizzevalue"
        },
    ),
    (
        "pipelinerun-pipeline-task",
        [("spec.params.0.value", "{{value}}")],
        {},
    ),
    (
        "pipelinerun-pipelinespec-taskspec",
        [("spec.pipelineSpec.tasks.0.taskSpec.steps.0.name", "hello-moto")],
        {},
    ),
    (
        "pipelinerun-pipelinespec-taskref",
        [("spec.pipelineSpec.tasks.0.taskSpec.steps.0.name", "task1")],
        {},
    ),
    (
        "pipelinerun-pipelineref-taskspec",
        [("spec.pipelineSpec.tasks.0.taskSpec.steps.0.name", "first-step")],
        {},
    ),
]


@pytest.fixture(scope="session")
def fixtures():
    ret = {}
    for fname in glob.glob(
            os.path.join(os.path.dirname(__file__), 'yamls/*.y*ml')):
        ret[os.path.splitext(os.path.basename(fname))[0]] = fname
    return ret


@pytest.mark.parametrize("fixture,assertions,parametre", PARAM_FIXTURES)
def test_tektonbundle_parsing(fixtures, fixture, assertions, parametre):
    output = yaml.safe_load(tektonbundle.parse([fixtures[fixture]], parametre))
    for assertment in assertions:
        assert get_key(output, assertment[0]) == assertment[1]
