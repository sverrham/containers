#!/usr/bin/env python3

# Authors:
#   Unai Martinez-Corral
#
# Copyright 2021 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from run import _exec


def BuildImage(
    image: str,
    registry: str = "ghcr.io/hdl",
    collection: str = "debian-buster",
    dockerfile: str = None,
    target: str = None,
    argimg: str = None,
    pkg: str = False,
    dry: bool = False,
):
    if dockerfile is None:
        dockerfile = image

    if pkg is True:
        image = f"pkg:{image}"
        if target is None:
            target = "pkg"

    _imageName = f"{registry}/{collection}/{image}"

    cmd = ["docker", "build"]
    cmd += ["--progress=plain", "--build-arg", "BUILDKIT_INLINE_CACHE=1"]
    cmd += ["-t", _imageName]

    if target is not None:
        cmd += [f"--target={target}"]

    if argimg is not None:
        cmd += ["--build-arg", f"IMAGE={argimg}"]

    cmd += ["-f", f"./{collection}/{dockerfile}.dockerfile"]

    cmd += ["."]

    _exec(args=cmd, dry=dry, collapse=f"Build {_imageName}")