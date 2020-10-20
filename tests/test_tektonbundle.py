#!/usr/bin/env python
import pytest
import yaml

from tektonbundle import tektonbundle
"""Tests for `tektonbundle` package."""


def test_with_taskspec():
    """Expands pipeline but keep the taskSpec"""
    output = yaml.safe_load(
        tektonbundle.parse([
            """---
    apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      name: pr-test1
    spec:
      pipelineRef:
        name: pipeline-test1
      params:
        - name: key
          value: {{value}}
        - name: revision
          value: "bar"
    """, """---
    apiVersion: tekton.dev/v1beta1
    kind: Pipeline
    metadata:
      name: pipeline-test1
    spec:
      params:
        - name: repo_url
        - name: revision
      tasks:
        - name: task-of-pipeline-test1
          taskSpec:
            steps:
            - name: first-step
              image: image1
        - name: task-of-pipeline-test2
          taskRef:
            name: task-test2
      steps:
        - name: first-step
          image: image
    """, """---
    apiVersion: tekton.dev/v1beta1
    kind: Task
    metadata:
      name: task-test2
    spec:
      steps:
        - name: second-step
          image: image
"""
        ], {"value": "hello"}))

    assert output['spec']['pipelineSpec']['tasks'][0]['taskSpec']['steps'][0][
        'name'] == "first-step"
    assert output['spec']['pipelineSpec']['tasks'][1]['taskSpec']['steps'][0][
        'name'] == "second-step"


def test_simple():
    output = yaml.safe_load(
        tektonbundle.parse([
            """---
    apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      name: pr-test1
    spec:
      pipelineRef:
        name: pipeline-test1
      params:
        - name: key
          value: {{value}}
        - name: revision
          value: "bar"
    """, """---
    apiVersion: tekton.dev/v1beta1
    kind: Pipeline
    metadata:
      name: pipeline-test1
    spec:
      params:
        - name: repo_url
        - name: revision
      tasks:
        - name: task-of-pipeline-test1
          taskRef:
            name: task1
    """, """---
    apiVersion: tekton.dev/v1beta1
    kind: Task
    metadata:
      name: task1
    spec:
      steps:
        - name: first-step
          image: image
    """
        ], {"value": "hello"}))

    assert 'pipelineSpec' in output['spec']
    assert 'taskSpec' in output['spec']['pipelineSpec']['tasks'][0]
    assert output['spec']['pipelineSpec']['tasks'][0][
        'name'] == 'task-of-pipeline-test1'


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
