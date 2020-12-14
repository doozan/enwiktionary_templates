#
# Copyright (c) 2020 Jeff Doozan
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Data and utilities for processing Spanish sections of enwiktionary
"""

import re
import sys

from .paradigms import paradigms
from .combined import _data as combined

from ..get_template_params import get_template_params

def es_adj(t, title):
    results = get_adjective_forms(t, title)

    sources = {
        "f": ["f", "f2", "f3"],
        "pl": ["pl", "pl2", "pl3"],
        "mpl": ["mpl", "mpl2", "mpl2"],
        "fpl": ["fpl", "fpl2", "mpl3"]
    }

    overrides = {}
    for k,params in sources.items():
        for param in params:
            if t.has(param):
                overrides[k] = overrides.get(k, []) + [str(t.get(param).value)]

    for k,v in overrides.items():
        if k in results:
            results[k] = v

    return "; ".join([f"{k}={v}" for k,vs in sorted(results.items()) for v in vs])


def es_adj_sup(t, title):
    return es_adj(t, title)

def get_adjective_forms(template, title):
    if template is None:
        return {}

    if not title:
        return {}

    params = get_template_params(template)
    for k in [ "f", "pl", "mpl", "fpl" ]:
        if isinstance(params.get(k), str):
            params[k] = [params[k]]

    if "f" in params and "fpl" not in params:
        if "pl" in params:
            params["fpl"] = [ params["pl"][0] ]
        else:
            params["fpl"] = [ params["f"][0] + "s" ]

    if "m" not in params and "mpl" in params and "pl" not in params:
        params["pl"] = params.pop("mpl")

    if "pl" not in params:
        params["pl"] = [ title + "s" ]

    return {k:params[k] for k in ["f", "pl","fpl"] if k in params}
