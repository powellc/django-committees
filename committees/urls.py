from django.conf.urls.defaults import *
from django.conf import settings

from committees import views

urlpatterns = patterns('committees.views',
    url (r'^$', view=views.index, name='cm-index', ),
    url (r'^(?P<slug>[-\w]+)/officer/(?P<office_slug>[-\w]+)/$', view=views.term_detail, name='cm-term-detail', ),
    url (r'^(?P<slug>[-\w]+)/officer/(?P<office_slug>[-\w]+)/(?P<start_year>[\d]+)/$', view=views.term_detail, name='cm-term-archive-year', ),
    url (r'^(?P<slug>[-\w]+)/$', view=views.group_detail, name='cm-group-detail', ),
    url (r'^(?P<slug>[-\w]+)/meetings/$', view=views.group_meeting_list, name='cm-group-meeting-list', ),
    url (r'^(?P<slug>[-\w]+)/meetings/(?P<year>[\d]+)/$', view=views.group_meeting_archive_year, name='cm-group-meeting-archive-year', ),
    url (r'^(?P<slug>[-\w]+)/meetings/(?P<year>[\d]+)/(?P<month>[\w]+)/$', view=views.group_meeting_detail, name='cm-meeting-detail', ),
    url (r'^(?P<slug>[-\w]+)/meetings/(?P<year>[\d]+)/(?P<month>[\w]+)/print/$', view=views.group_meeting_detail, name='cm-meeting-print', ),
    
)
