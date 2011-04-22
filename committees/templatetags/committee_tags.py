import re
import logging

from django import template
from django.conf import settings
from django.db import models
from committees.models import Group, Office

register = template.Library()

@register.tag
def get_office(parser, token):
    """
    Gets an office if it exists

    Syntax::

    {% get_office [slug] as [var_name] %}

    Example usage::

    {% get_office 'president' as prez %}

    """
    args = token.split_contents()
    argc = len(args)

    try:
        assert argc == 4
    except AssertionError:
        raise template.TemplateSyntaxError('Invalid get_office syntax.')
    # determine what parameters to use
    slug = var_name = None
    if argc == 4:
        t, slug, a, var_name = args
    return GetOfficeNode(slug=slug, var_name=var_name)

class GetOfficeNode(template.Node):
    def __init__(self, slug, var_name):
        self.slug = slug
        self.var_name = var_name

    def render(self, context):
        try:
            self.office = Office.objects.get(slug=self.slug)
        except:
            self.office = None
        context[self.var_name] = self.office
        return ''

class GetGroupsNode(template.Node):
    def __init__(self, status, order, var_name):
        self.var_name = var_name
        self.status = status
        self.order = order

    def render(self, context):
        groups = '' 
        if self.order: q = models.Q(order=self.order)
        else: q = models.Q()

        if self.status == 'active': groups = Group.active_objects.filter(q)
        elif self.status == 'inactive': groups = Group.objects.filter(q).exclude(active=True)
        elif self.status == 'all': groups = Group.objects.filter(q)
        else: raise template.TemplateSyntaxError('Invalid get_committee_groups syntax where order = %s, status = %s and var_name = %s' % (self.order, self.status, self.var_name))

        if groups and len(groups)==1:
            context[self.var_name] = groups[0]
        else:
            context[self.var_name] = groups 
        return ''


@register.tag
def get_committee_groups(parser, token):
    """
    Gets any number of groups ordered by order and places them in a varable.

    Syntax::

    {% get_committee_groups (order [order]|[status]) as [var_name] %}

    Example usage::

    {% get_committee_groups order 10 as boards %}
    {% get_committee_groups inactive order 10 as boards %}
    {% get_committee_groups active as boards %}
    {% get_committee_groups inactive as committees %}
    {% get_comm_groups all as groups %}
    """
    args = token.split_contents()
    argc = len(args)

    try:
        assert argc in (4,5,6)
    except AssertionError:
        raise template.TemplateSyntaxError('Invalid get_committee_groups syntax.')
    # determine what parameters to use
    order = status = var_name = None
    if argc == 4: t, status, a, var_name = args
    elif argc == 5: t, o, order, a, var_name = args
    elif argc == 6: t, status, o, order, a, var_name = args
    return GetGroupsNode(status=status, order=order, var_name=var_name)

class GetGroupNode(template.Node):
    def __init__(self, slug, var_name):
        self.slug = slug
        self.var_name = var_name

    def render(self, context):
        try:
            group = Group.active_objects.get(slug__exact=self.slug)
            context[self.var_name] = group
        except:
            context[self.var_name] = None
        return ''


@register.tag
def get_committee_group(parser, token):
    """
    Gets a a group if it exists

    Syntax::

    {% get_group [slug] as [var_name] %}

    Example usage::

    {% get_group 'governing-board' as board %}

    """
    args = token.split_contents()
    argc = len(args)

    try:
        assert argc == 4
    except AssertionError:
        raise template.TemplateSyntaxError('Invalid get_group syntax.')
    # determine what parameters to use
    slug = var_name = None
    if argc == 4:
        t, slug, a, var_name = args
    return GetGroupNode(slug=slug, var_name=var_name)

class GetMinutesNode(template.Node):
    def __init__(self, meeting, var_name):
        self.meeting=template.Variable(meeting)
        self.var_name = var_name

    def render(self, context):
        try:
            meeting = self.meeting.resolve(context)
            try:
                context[self.var_name] = meeting.minutes_set.all()[0]
                return ''
            except:
                context[self.var_name] = None
                return ''
        except template.VariableDoesNotExist:
            return ''


@register.tag
def get_committee_minutes(parser, token):
    """
    Gets most recent minutes of a meeting if they exist

    Syntax::

    {% get_committee_minutes from [meeting object] as [var_name] %}

    """
    args = token.split_contents()
    argc = len(args)

    try:
        assert argc == 5
    except AssertionError:
        raise template.TemplateSyntaxError('Invalid get_committee_minutes syntax.')
    # determine what parameters to use
    meeting = var_name = None
    if argc == 5:
        t, f, meeting, a, var_name = args
    return GetMinutesNode(meeting=meeting, var_name=var_name)
