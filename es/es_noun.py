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
from .module_es_headword import do_noun

def es_noun(t, title):
    args = get_template_params(t)

    fix_forms = {'p': 'pl'}

    data = {}
    do_noun(title, args, data)

    results = []

    for item in data.get("inflections",[]):
        for form in item.get('',[]):

            # items can be a list of strings
            if hasattr(form, 'casefold'):
                formtype = item["accel"]["form"]
                formtype = fix_forms.get(formtype, formtype)
                results.append(formtype + "=" + form)

            # or a list of dicts with accelerators
            else:
                formtype = form["accel"]["form"]
                formtype = fix_forms.get(formtype, formtype)
                if formtype == 'pl' and item["label"] == "feminine plural":
                    formtype = "fpl"
                if formtype == 'pl' and item["label"] == "masculine plural":
                    formtype = "mpl"
                results.append(formtype + "=" + form["term"])

    return '; '.join(results)
