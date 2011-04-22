from datetime import datetime

from django.template.context import RequestContext
from django.views.generic import list_detail
from django.shortcuts import render_to_response, get_object_or_404

from committees.models import Group, Meeting, Minutes, Term

def index(request):
    objects = Group.active_objects.all().order_by('order')
    past_meetings = Meeting.objects.filter(start__lte=datetime.now())
    return render_to_response('committees/index.html', locals(),
                              context_instance=RequestContext(request))

def group_detail(request, slug):
    object=Group.objects.get(slug=slug)
    members=object.term_set.filter(start__lte=datetime.now(), end__gte=datetime.now())
    return render_to_response('committees/group_detail.html', locals(),
                              context_instance=RequestContext(request))

def group_meeting_list(request, slug):
    group = Group.objects.get(slug=slug)
    objects = Meeting.objects.filter(group=group)
    return render_to_response('committees/meeting_list.html', locals(),
                  context_instance=RequestContext(request))

def group_meeting_archive_year(request, slug, year):
    group = Group.objects.get(slug=slug)
    objects = Meeting.objects.filter(group=group, start__year=year)
    return render_to_response('committees/meeting_list.html', locals(),
                  context_instance=RequestContext(request))

def group_meeting_detail(request, slug, year, month):
    object = Meeting.objects.get(group__slug=slug, start__year=year, start__month=month)
    return render_to_response('committees/meeting_detail.html', locals(),
                  context_instance=RequestContext(request))
    
def minutes_detail(request, slug, year, month):
    meeting = Meeting.objects.get(meeting__group__slug=slug, start__year=year, start__month=month)
    object = Minutes.objects.get(meeting=meeting)
    return render_to_response('committees/minutes_detail.html', locals(),
                  context_instance=RequestContext(request))

def term_detail(request, slug, office_slug, start_year=None):
    if start_year:
        term = Term.objects.get(office__slug=office_slug, group__slug=slug,  start__year=start_year)
    else:
        terms = Term.objects.filter(office__slug=office_slug, group__slug=slug )
        if len(terms) == 1:
            term = terms[0]
    return render_to_response('committees/term_detail.html', locals(),
                  context_instance=RequestContext(request))
