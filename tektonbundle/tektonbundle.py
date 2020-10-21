"""Main module."""

import copy
import io
import logging
import re
from typing import Dict, List

import yaml

log = logging.getLogger(__name__)

TEKTON_TYPE = ("pipeline", "pipelinerun", "task", "taskrun", "condition")


class TektonBundleError(Exception):
    pass


def tpl_apply(yaml_obj, parameters):
    def _apply(param):
        if param in parameters:
            return parameters[param]
        return "{{%s}}" % (param)

    return io.StringIO(
        re.sub(
            r"\{\{([_a-zA-Z0-9\.]*)\}\}",
            lambda m: _apply(m.group(1)),
            open(yaml_obj).read(),
        ))


def resolve_task(mpipe, name, yaml_documents):
    if 'pipelineSpec' in mpipe['spec']:
        tasks = mpipe['spec']['pipelineSpec']['tasks']
    else:
        tasks = mpipe['spec']['tasks']

    for task in tasks:
        if 'taskRef' in task:
            reftask = task['taskRef']['name']
            if 'task' not in yaml_documents or reftask not in yaml_documents[
                    'task']:
                raise TektonBundleError(
                    f"Pipeline: {name} reference a Task: {reftask} not in repository"
                )

            del task['taskRef']
            task['taskSpec'] = yaml_documents['task'][reftask]['spec']

    return mpipe


def parse(yamlfiles: List[str], parameters: Dict[str, str]) -> str:
    """parse a bunch of yaml files"""
    yaml_documents = {}  # type: Dict[str, Dict]
    results = []
    for yaml_file in yamlfiles:
        for document in yaml.load_all(tpl_apply(yaml_file, parameters),
                                      Loader=yaml.Loader):
            if 'apiVersion' not in document or 'kind' not in document:
                log.debug("Skipping this document, not a kubernetes type")
                continue

            name = (document['metadata']['generateName']
                    if 'generateName' in document['metadata'].keys() else
                    document['metadata']['name'])
            kind = document['kind'].lower()

            if kind not in TEKTON_TYPE:
                log.debug("Skipping not a tekton file: kind=%s", kind)
                continue

            yaml_documents.setdefault(kind, {})
            yaml_documents[kind][name] = document

    if 'pipelinerun' not in yaml_documents:
        raise TektonBundleError("We need at least a PipelineRun")

    # if we have pipeline (i.e: not embedded) then expand all tasksRef insides.
    if 'pipeline' in yaml_documents:
        for pipeline in yaml_documents['pipeline']:
            mpipe = copy.deepcopy(yaml_documents['pipeline'][pipeline])
            resolved = resolve_task(mpipe, pipeline, yaml_documents)
            yaml_documents['pipeline'][pipeline] = copy.deepcopy(resolved)

    # For all pipelinerun expands the pipelineRef, keep it as is if it's a
    # pipelineSpec.
    for pipeline_run in yaml_documents['pipelinerun']:
        mpr = copy.deepcopy(yaml_documents['pipelinerun'][pipeline_run])
        if 'pipelineSpec' in mpr['spec']:
            mpr = resolve_task(mpr, pipeline_run, yaml_documents)
        elif 'pipelineRef' in mpr['spec']:
            refpipeline = mpr['spec']['pipelineRef']['name']
            if 'pipeline' not in yaml_documents or refpipeline not in yaml_documents[
                    'pipeline']:
                raise TektonBundleError(
                    f"PR: {pipeline_run} reference a Pipeline: {refpipeline} not in repository"
                )
            del mpr['spec']['pipelineRef']
            mpr['spec']['pipelineSpec'] = yaml_documents['pipeline'][
                refpipeline]['spec']

        # Adjust names with generateName if needed
        # TODO(chmou): make it optional, we maybe don't want to do this sometime
        if 'name' in mpr['metadata']:
            name = mpr['metadata']['name']
            mpr['metadata']['generateName'] = name + "-"
            del mpr['metadata']['name']

        results.append(mpr)

    return (yaml.dump_all(results,
                          Dumper=yaml.Dumper,
                          default_flow_style=False,
                          allow_unicode=True))
