#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '.')

from script_helpers.render_template_helpers import render_nginx_template

if __name__ == "__main__":
    print(render_nginx_template(sys.argv[1]))
