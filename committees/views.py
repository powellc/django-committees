from datetime import datetime

from django.template.context import RequestContext
from django.views.generic import list_detail
from django.shortcuts import render_to_response, get_object_or_404

from committees.models import *

def index(request):
    board = Term.active_objects.filter(group__slug='governing-board')
    past_meetings = Meeting.objects.filter(start__lte=datetime.now(), calendar__slug='governance')[:5]
    return render_to_response('gov/index.html', locals(),
                              context_instance=RequestContext(request))

def group_detail(request, slug):
    object=Group.objects.get(slug=slug)
    members=object.term_set.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now())
    return render_to_response('gov/group_detail.html', locals(),
                              context_instance=RequestContext(request))

def group_meeting_list(request, slug):
    group = Group.objects.get(slug=slug)
    objects = Meeting.objects.filter(group=group)
    return render_to_response('gov/meeting_list.html', locals(),
                  context_instance=RequestContext(request))

def group_meeting_archive_year(request, slug, year):
    group = Group.objects.get(slug=slug)
    objects = Meeting.objects.filter(group=group, start__year=year)
    return render_to_response('gov/meeting_list.html', locals(),
                  context_instance=RequestContext(request))

def group_meeting_detail(request, slug, year, month):
    object = Meeting.objects.get(meeting__group__slug=slug, start__year=year, start__month=month)
    return render_to_response('gov/meeting_detail.html', locals(),
                  context_instance=RequestContext(request))
    
def minutes_detail(request, slug, year, month):
    meeting = Meeting.objects.get(meeting__group__slug=slug, start__year=year, start__month=month)
    object = Minutes.objects.get(meeting=meeting)
    return render_to_response('gov/minutes_detail.html', locals(),
                  context_instance=RequestContext(request))

def term_detail(request, office_slug, start_year=None):
    if start_year:
        term = Term.objects.get(office__slug=office_slug, start_date__year=start_year)
    else:
        term = Term.objects.filter(office__slug=office_slug).latest()
    return render_to_response('gov/term_detail.html', locals(),
                  context_instance=RequestContext(request))
