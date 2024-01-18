#!/usr/bin/python3
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

import re

# Convert hash of params like { foo: bar, a: zero, a1: one, a2: two } to { foo: bar, a: [zero, one, two] }
# for use with es_headword
def convert_template_params(template):
    params = {}
    param_lists = {}

    if isinstance(template, dict):
        items = template.items()
    else:
        items = [(str(param.name).strip(), str(param.value).strip()) for param in template.params]

    for name, value in items:
        name = str(name)

        res = re.match(r"([^0-9]+?)[1-9]+$", name)
        if res:
            k = res.group(1)
            if k not in param_lists:
                if k in params:
                    param_lists[k] = [params[k], value]
                else:
                    param_lists[k] = [value]
            else:
                param_lists[k].append(value)
        else:
            params[name] = value

    return {**params, **param_lists}

