from datetime import datetime
from django.db.models import Manager
from django.db.models import Q

class BoardManager(Manager):
    """Returns all meetings of the type: Governing board"""

    def get_query_set(self):
        return super(BoardManager, self).get_query_set().filter(group__type__slug='board')
	
class ActiveTermManager(Manager):
    """Returns all currently active terms."""

    def get_query_set(self):
        return super(ActiveTermManager, self).get_query_set().filter(start__lte=datetime.now().date()).filter(Q(end__gte=datetime.now().date())|Q(end__isnull=True))

class ActiveGroupManager(Manager):
    """Returns all currently active groups."""

    def get_query_set(self):
        return super(ActiveGroupManager, self).get_query_set().filter(active=True)

class ApprovedManager(Manager):
    """Returns all currently active groups."""

    def get_query_set(self):
        return super(ApprovedManager, self).get_query_set().filter(draft=False)
