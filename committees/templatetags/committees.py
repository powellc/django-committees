import re

from django import template
from django.conf import settings
from django.db import models

Sermon = models.get_model('sermon', 'sermon')

register = template.Library()

class LatestSermons(template.Node):
    def __init__(self, limit, var_name):
        self.limit = int(limit)
        self.var_name = var_name

    def render(self, context):
        sermons = Sermon.objects.published()[:self.limit]
        if sermons and (self.limit == 1):
            context[self.var_name] = sermons[0]
        else:
            context[self.var_name] = sermons
        return ''


@register.tag
def get_latest_sermons(parser, token):
    """
Gets any number of latest sermons and stores them in a varable.

Syntax::

{% get_latest_sermons [limit] as [var_name] %}

Example usage::

{% get_latest_sermons 10 as latest_post_list %}
"""
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return LatestSermons(format_string, var_name)