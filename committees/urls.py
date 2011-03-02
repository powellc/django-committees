from django.conf.urls.defaults import *
from django.conf import settings

from committees import views

urlpatterns = patterns('committees.views',
    url (r'^$', view=views.index, name='gv-index', ),
    url (r'^(?P<slug>[-\w]+)/$', view=views.group_detail, name='gv-group-detail', ),
    url (r'^(?P<slug>[-\w]+)/meetings/$', view=views.group_meeting_list, name='gv-group-meeting-list', ),
    url (r'^(?P<slug>[-\w]+)/meetings/(?P<year>[\d]+)/$', view=views.group_meeting_archive_year, name='gv-group-meeting-archive-year', ),
    url (r'^(?P<slug>[-\w]+)/meetings/(?P<year>[\d]+)/(?P<month>[\w]+)/$', view=views.group_meeting_detail, name='gv-meeting-detail', ),
    url (r'^(?P<slug>[-\w]+)/meetings/(?P<year>[\d]+)/(?P<month>[\w]+)/minutes/$', view=views.minutes_detail, name='gv-minutes-detail', ),
    
    url (r'^officer/(?P<office_slug>[-\w]+)/$', view=views.term_detail, name='gv-term-detail', ),
    url (r'^officer/(?P<office_slug>[-\w]+)/(?P<start_year>[\d]+)/$', view=views.term_detail, name='gv-term-archive-year', ),
)
