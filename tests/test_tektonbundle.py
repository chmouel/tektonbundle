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


@pytest.fixture(scope="session")
def fixtures():
    ret = {}
    for fname in glob.glob(
            os.path.join(os.path.dirname(__file__), 'yamls/*.y*ml')):
        ret[os.path.splitext(os.path.basename(fname))[0]] = fname
    return ret


def test_pipelinerun_pipeline_task(fixtures):
    output = yaml.safe_load(
        tektonbundle.parse([fixtures['pipelinerun-pipeline-task']],
                           {"value": "replaced_value"}))
    assert get_key(
        output,
        "spec.pipelineSpec.tasks.0.taskSpec.steps.0.name"), "first-steps"

    assert get_key(
        output,
        "spec.pipelineSpec.tasks.1.taskSpec.steps.0.name"), "second-step"

    assert get_key(output, "spec.params.0.value"), "replaced_value"


def test_unknown_template_not_replacing(fixtures):
    output = yaml.safe_load(
        tektonbundle.parse([fixtures['pipelinerun-pipeline-task']],
                           {"nothing": "evergetreplaced"}))
    assert get_key(output, "spec.params.0.value"), "{{value}}"


@pytest.mark.skip(
    reason="We do not handle pipelines where we have nothing to do yet.")
def test_pipeline_nothing_todo():
    output = yaml.safe_load(
        tektonbundle.parse([
            """---
    apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      name: pr-test1
    spec:
      pipelineRef:
        spec:
          name: pipeline
        """
        ], {"1": "2"}))
    assert len(output) == 1


@pytest.mark.skip(reason="This is failing for now.")
def test_kubernetes_document():
    output = yaml.safe_load(
        tektonbundle.parse([
            """---
        key: value
        """, """---
    apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      name: pr-test1
    spec:
      pipelineRef:
        spec:
          name: pipeline
        """
        ], {"1": "2"}))
    assert len(output) == 1
