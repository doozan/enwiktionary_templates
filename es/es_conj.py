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
import sys
import enwiktionary_templates.module.es_verb as M
from ..get_template_params import get_template_params

def es_conj(t, title):
    #print(title, t, file=sys.stderr)
    args = get_template_params(t)
    # always generate all combined forms
    args.pop("nocomb",None)
    args[1] = args.pop('1', None)
    args["pagename"] = title

    forms = M.do_generate_forms(args, False, {}, title)
    joined = M.concat_forms(forms, {})
    joined = joined.replace("[[", "").replace("]]", "")
    items = []
    for i in joined.split("|"):
        k, _, values = i.partition("=")
        for v in values.split(","):
            items.append(f"{k}={v}")

    return "; ".join(sorted(items))
