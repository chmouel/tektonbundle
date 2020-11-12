#!/usr/bin/env python
"""Tests for `tektonbundle` package."""
import pytest
import yaml

from tektonbundle import tektonbundle
from tests.fixtures import testdata  # pylint:  disable=unused-import


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


@pytest.mark.parametrize("fixture,assertions,parametre", FIXTURES_GOOD)
def test_good(testdata, fixture, assertions, parametre):
    ret = tektonbundle.parse([testdata[fixture]], parametre, skip_inlining=[])
    output = yaml.safe_load(ret['bundle'])
    for assertment in assertions:
        assert get_key(output, assertment[0]) == assertment[1]


@pytest.mark.parametrize("fixture", FIXTURES_BAD)
def test_bad(testdata, fixture):
    with pytest.raises(tektonbundle.TektonBundleError):
        tektonbundle.parse([testdata[fixture]], {}, skip_inlining=[])


def test_skip_not_tekton_documents(testdata):
    ret = tektonbundle.parse([testdata["not-a-kubernetes-yaml"]], {},
                             skip_inlining=[])
    assert ret['ignored_not_k8']

    ret = tektonbundle.parse([testdata["not-a-tekton-document"]], {},
                             skip_inlining=[])

    assert ret['ignored_not_tekton']


def test_skip_inlining(testdata):
    inlining_skipped = False
    ret = tektonbundle.parse([testdata["pipelinerun-pipeline-task"]], {},
                             skip_inlining=["task-test3"])
    output = yaml.safe_load(ret['bundle'])
    for task in output['spec']['pipelineSpec']['tasks']:
        if 'taskRef' in task and task['taskRef']['name'] == "task-test3":
            inlining_skipped = True
    assert inlining_skipped
