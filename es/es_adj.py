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

from ..get_template_params import get_template_params
from ..module.es_headword import do_adjective
import sys

def es_adj(t, title):
    args = get_template_params(t)

    form_types = {
        "masculine": "m",
        "feminine": "f",
        "plural": "pl",
        "masculine plural": "pl",
        "feminine plural": "fpl",
    }

    data = {}
    do_adjective(title, args, data)

    results = []

    for item in data.get("inflections",[]):
        for form in item.get('',[]):
            formtype = form_types.get(item["label"])
            if not formtype:
                continue

            # items can be a list of strings
            if hasattr(form, 'casefold'):
                results.append(formtype + "=" + form)

            # or a list of dicts with accelerators
            else:
                results.append(formtype + "=" + form["term"])

    return '; '.join(results)

def es_adj_sup(t, title):
    return es_adj(t, title)
