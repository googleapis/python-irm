# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate dlp GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="irm",
    version="v1alpha2",
    bazel_target="//google/cloud/irm/v1alpha2:irm-v1alpha2-py",
    include_protos=True,
)

excludes = ["README.rst", "nox*.py", "setup.py", "docs/index.rst"]
s.move(library, excludes=excludes)

# Fix docstrings
s.replace("google/**/*.py", r"\\_", "_")
s.replace("google/**/incidents_service_pb2.py", r"""\\\*""", r"""*""")
s.replace("google/**/incident_service_client.py", r"""\\\*""", r"""*""")
s.replace(
    "google/**/incident_service_client.py",
    r"""        This will fail if:
           a\. there are too many \(50\) subscriptions in the incident already
           b\. a subscription using the given channel already exists""",
    r"""        This will fail if:
        a. there are too many (50) subscriptions in the incident already
        b. a subscription using the given channel already exists""",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=70)
s.move(templated_files)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

# Escape '_' in docstrings
s.replace(
   "google/cloud/**/*_pb2.py",
   """\_$""",
   """\_""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
