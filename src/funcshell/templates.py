# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, TemplateSyntaxError

def render(name, data):
  try:
    templates_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
    environment = Environment(loader=FileSystemLoader(templates_path))
    template = environment.get_template('%s.tmpl' % name)
    content = template.render(data=data).strip()
  except TemplateNotFound:
    content = 'Template not found.'
  except TemplateSyntaxError:
    content = 'Template syntax error.'
  return content
