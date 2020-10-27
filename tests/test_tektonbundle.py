#!/usr/bin/env python
"""Tests for `tektonbundle` package."""
import glob
import logging
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
        curr = curr[k]
    return curr


FIXTURES_GOOD = [
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

FIXTURES_BAD = [
    "no-pipelinerun", "referenced-task-not-in-repo",
    "referenced-pipeline-not-in-repo"
]

FIXTURES_UGLY = [
    ("not-a-kubernetes-yaml", "Skipping this document, not a kubernetes type"),
    ("not-a-tekton-document", "Skipping not a tekton file: kind=pod")
]


@pytest.fixture(scope="session")
def testdata():
    ret = {}
    for fname in glob.glob(
            os.path.join(os.path.dirname(__file__), 'yamls/*.y*ml')):
        ret[os.path.splitext(os.path.basename(fname))[0]] = fname
    return ret


@pytest.mark.parametrize("fixture,assertions,parametre", FIXTURES_GOOD)
def test_good(testdata, fixture, assertions, parametre):
    output = yaml.safe_load(
        tektonbundle.parse([testdata[fixture]], parametre, skip_inlining=[]))
    for assertment in assertions:
        assert get_key(output, assertment[0]) == assertment[1]


@pytest.mark.parametrize("fixture", FIXTURES_BAD)
def test_bad(testdata, fixture):
    with pytest.raises(tektonbundle.TektonBundleError):
        tektonbundle.parse([testdata[fixture]], {}, skip_inlining=[])


@pytest.mark.parametrize("fixture,logtext", FIXTURES_UGLY)
def test_warnings(testdata, caplog, fixture, logtext):
    with caplog.at_level(logging.DEBUG):
        tektonbundle.parse([testdata[fixture]], {}, skip_inlining=[])
        assert logtext in caplog.text


def test_skip_inlining(testdata):
    print(testdata["pipelinerun-pipeline-task"])
    inlining_skipped = False
    output = yaml.safe_load(
        tektonbundle.parse([testdata["pipelinerun-pipeline-task"]], {},
                           skip_inlining=["task-test3"]))
    for task in output['spec']['pipelineSpec']['tasks']:
        if 'taskRef' in task and task['taskRef']['name'] == "task-test3":
            inlining_skipped = True
    assert inlining_skipped
