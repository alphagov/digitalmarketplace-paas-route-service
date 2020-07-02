#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from six.moves.urllib.parse import urljoin
import jinja2
from jinja2.runtime import StrictUndefined


def load_file(path):
    with open(path) as f:
        return f.read()


def _urljoin(base, url):
    """
    jinja filter to allow templates to perform a correct "url join". can also be used to conditionally add a trailing
    slash to base if not already present - particularly useful when passing an url to the proxy_pass directive which
    behaves differently depending on whether a target address has an url "path" part
    """
    return urljoin(base, url, allow_fragments=False)


def template_string(string, variables, templates_path):
    jinja_env = jinja2.Environment(
        autoescape=False,
        # the jinja templates have no user input and are used to generate config files
        # we are not confident that autoescaping will be useful here and we have therefore taken a positive decision
        # to turn it off
        trim_blocks=True,
        undefined=StrictUndefined,
        loader=jinja2.FileSystemLoader(templates_path)
    )

    jinja_env.filters["urljoin"] = _urljoin

    try:
        template = jinja_env.from_string(string)
    except jinja2.exceptions.TemplateSyntaxError as e:
        raise ValueError(u"Template error: {}".format(e))

    try:
        return template.render(variables)
    except jinja2.exceptions.UndefinedError as e:
        raise ValueError(u"Variable {} in '{}'".format(e, string))


def render_nginx_template(template_path):
    variables = {
        key.replace('DM_', '').lower(): value
        for key, value in os.environ.items()
        if key.startswith('DM_')
    }

    variables.update({
        'static_files_root': '/usr/share/nginx/html'
    })

    with open(template_path, 'r') as template_file:
        return template_string(
            template_file.read(),
            variables=variables,
            templates_path=os.path.dirname(template_path)
        )


if __name__ == "__main__":
    print(render_nginx_template(sys.argv[1]))
