# -*- coding: utf-8 -*-
# Author: Chmouel Boudjnah <chmouel@chmouel.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import os
import shutil

from tektonbundle import cli
from tests.fixtures import testdata  # pylint:  disable=unused-import


def test_cli(testdata, tmpdir):
    yamldir = tmpdir.mkdir("yamldir")
    shutil.copy(testdata['pipelinerun-pipeline-task'], yamldir)
    assert cli.bundler([str(yamldir)])[0] == "--- "

    copied_file = yamldir / os.path.basename(
        str(testdata['pipelinerun-pipeline-task']))
    assert cli.bundler([str(copied_file)])[0] == "--- "
