#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import jinja2
from jinja2.runtime import StrictUndefined


def load_file(path):
    with open(path) as f:
        return f.read()


def ensure_trailing_slash(value):
    """
    jinja filter to add a trailing slash to value if not already present - particularly useful when passing an url
    to the proxy_pass directive which behaves differently depending on whether a target address has an url "path" part
    """
    value = str(value)
    return value if value.endswith("/") else value + "/"


def template_string(string, variables, templates_path):
    jinja_env = jinja2.Environment(
        trim_blocks=True,
        undefined=StrictUndefined,
        loader=jinja2.FileSystemLoader(templates_path)
    )

    jinja_env.filters["ensure_trailing_slash"] = ensure_trailing_slash

    try:
        template = jinja_env.from_string(string)
    except jinja2.exceptions.TemplateSyntaxError as e:
        raise ValueError(u"Template error: {}".format(e))

    try:
        return template.render(variables)
    except jinja2.exceptions.UndefinedError as e:
        raise ValueError(u"Variable {} in '{}'".format(e, string))


def main(template_name):
    variables = {
        key.replace('DM_', '').lower(): value
        for key, value in os.environ.items()
        if key.startswith('DM_')
    }

    variables.update({
        'static_files_root': '/usr/share/nginx/html'
    })

    with open(template_name, 'r') as template_file:
        return template_string(
            template_file.read(),
            variables=variables,
            templates_path=os.path.dirname(template_name)
        )


if __name__ == "__main__":
    print(main(sys.argv[1]))
