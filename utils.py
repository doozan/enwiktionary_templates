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

from collections import defaultdict
import re

def get_template_params(template):

    # handle overrides like {{t|one|1=foo}}, which has two parameters both named '1'
    condensed = { p.name.strip(): p.value.strip() for p in template.params }

    params = {}
    for k,v in condensed.items():
        attribs = []
        if k.isdigit():
            k = int(k)
            # handle positional params with <> attributes: |test<q:foo><t:bar>
            # This assumes that all templates using <> take a language id as the first parameter
            if v.endswith(">") and "<" in v:
                orig_v = v
                v, _, attrib_string = v.partition("<")
                for attrib_value in attrib_string.split("<"):
                    ak, _, av = attrib_value.partition(":")
                    ak = ak.strip() + str(k-1)
                    av = av.strip()
                    av = av.rstrip(" >") if av.endswith(">") else None
                    if not ak or not av:
                        v = orig_v
                        attribs = []
                        #print("Bad attributes", template, (ak, av))
                        break
                    attribs.append((ak,av))
        params[k] = v
        for ak, av in attribs:
            params[ak] = av

    return params


def params_to_str(params, sort_params=False, inline_modifiers=True):

    if not params:
        return ""

    res = []
    pos_values = []
    pos_modifiers = defaultdict(list)
    named_values = {}

    for k, v in params.items():
        if isinstance(k, int):
            pos_values.append((k,v))
        elif k[-1].isdigit():
            m = re.match(r"([^\d]+)(\d+)$", k)
            if not m:
                raise ValueError("unhandled pos modifier:", k)

            pos = int(m.group(2)) + 1
            pos_modifiers[pos].append((m.group(1), v))
        else:
            named_values[k] = v

    last_pos = 0
    for k, v in sorted(pos_values):
        for extra in range(last_pos+1, k):
            res.append("")
        last_pos = k

        modifier = ""
        if k in pos_modifiers:
            fmt = "<{}:{}>" if inline_modifiers else "|{}" + str(k-1) + "={}"
            if sort_params:
                modifier = "".join([ fmt.format(mk,mv) for mk, mv in sorted(pos_modifiers[k]) ])
            else:
                modifier = "".join([ fmt.format(mk,mv) for mk, mv in pos_modifiers[k] ])

        res.append(f"{v}{modifier}")


    if sort_params:
        res += [f"{k}={v}" for k,v in sorted(named_values.items())]
    else:
        res += [f"{k}={v}" for k,v in named_values.items()]

    return "|".join(res)
