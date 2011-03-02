from datetime import datetime
from django.db.models import Manager
from django.db.models import Q

class OfficerManager(Manager):
    """Returns board members who are officers. """

    def get_query_set(self):
        return super(OfficerManager, self).get_query_set().filter(office__isnull=False)

class BoardMeetingManager(Manager):
    """Returns all meetings of the type: Governing board"""

    def get_query_set(self):
        return super(BoardMeetingManager, self).get_query_set().filter(group__slug='governing-board')
	
class BoardMemberManager(Manager):
    """Returns all members of the type: Governing board"""

    def get_query_set(self):
        return super(BoardMemberManager, self).get_query_set().filter(group__slug='governing-board')

class ActiveManager(Manager):
    """Returns all currently active terms."""

    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(start_date__lte=datetime.now().date()).filter(Q(end_date__gte=datetime.now().date())|Q(end_date__isnull=True))
