from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib.localflavor.us.models import PhoneNumberField

from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from committees.managers import OfficerManager, BoardMeetingManager, ActiveManager, BoardMemberManager
from schedule.models import Event
from simple_history.models import HistoricalRecords

class Bylaws(TimeStampedModel):
    '''
    Bylaws model.

    Just keeps track of bylaws, plus any revisions.
    '''
    DRAFT  = 'D'
    ADOPTED= 'A'

    BYLAW_STATUS=(
        (DRAFT, 'Draft'),
        (ADOPTED, 'Adopted'),
    )
    title = models.CharField(max_length=30, blank=True, null=True)
    status  = models.CharField(_('Status'), choices=BYLAW_STATUS, default=DRAFT, max_length=1)
    content = models.TextField(_('Content'))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('By-laws')
        verbose_name_plural = _('By-laws')
    
    def __unicode__(self):
        return self.title

    @property
    def adopted(self): # Find the most recently adopted version
        for b in self.history.all():
            if b.status=='A':
                return b
        return None

NONE       = 0
BOARD      = 1
STANDING   = 2
ADHOC      = 3
MEMBERSHIP = 4

class GroupType(TitleSlugDescription):
    '''Group type model.

    Allows catering the group type to how orgs are organized into governing groups.
    
    e.g. Governing board, Ad-hoc committee, Congregation'''
    order = models.IntegerFIeld(_('Order'), max_length=2)

    class Meta:
        verbose_name = _('Group type')
        verbose_name_plural = _('Group types')
        ordering = ('order', 'title',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('gv-group-type-detail', None, {'slug': self.slug})


class Group(TimeStampedModel, TitleSlugDescriptionModel):
    '''Group model.

    Manages the various types of governing groups in an organization. (e.g. Governing Board, Music Committee, etc...)
    '''

    order=models.IntegerField(_('Order'), max_length=2, help_text='Used to order groups in a list. Set all ranks the same to sort by alpha.')
    type=models.ForeignKey(GroupType)
    adhoc=models.BooleanField(_('Ad-hoc'), default=False, help_text='Is this is an ad-hoc group?')

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        ordering = ('type', 'title',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('gv-group-detail', None, {'slug': self.slug})

    @property
    def members(self):
        objects=[]
        if self.type==MEMBERSHIP:
            for m in Person.objects.filter(member=True):
                objects.append(m)
        else:
            for t in Term.active_objects.all().filter(group=self):
                objects.append(t.person)
        return objects

    @property
    def past_members(self):
        objects=[]
        for t in Term.objects.all().filter(group=self):
            if not t in Term.active_objects.all().filter(group=self):
                objects.append(t.person)
        return objects

class Office(TimeStampedModel, TitleSlugDescriptionModel):
    '''
    Office model.

    Holds all the various office types, mostly just drawn from django-extension mixins. Designed to take care of pres, vp, sec, tres type positions.

    '''
    group=models.ForeignKey(Group)
    order=models.IntegerField(_('Office order'), max_length=2)
    
    class Meta:
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')
        ordering = ('order', 'group',)

    def __unicode__(self):
        return u'%s of %s' % (self.title, self.group)


class Term(TimeStampedModel):
    group = models.ForeignKey(Group)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'), blank=True, null=True)
    office = models.ForeignKey(Office, blank=True, null=True)
    alternate = models.BooleanField(_('Alternate'), default=False)
    person=models.ForeignKey('Person', blank=True, null=True)
    
    objects = models.Manager()
    board_members = BoardMemberManager()
    active_objects = ActiveManager()

    class Meta:
        verbose_name = _('Term')
        verbose_name_plural = _('Terms')
        ordering = ('-office','start_date',)
        get_latest_by = 'start_date'
   
    @property
    def active(self):
        status=False
        if self.start_date <= datetime.now().date():
            if self.end_date:
                if self.end_date >= datetime.now().date():
                    status = True
            else:
                status=True
        return status
    
    @property
    def length(self):
        if self.end_date:
            return (self.end_date.year - self.start_date.year)
        else:
            return None
    
    @property
    def officer(self):
        if self.office:
            return True
        else:
            return False

    def __unicode__(self):
        if self.officer:
            desc=self.office
        else:
            desc=u'%s member' % (self.group)
        
        if self.alternate:
            str=u'%s - alternate (%s)' % (self.person, self.start_date.year)
        else:
            str=u'%s - %s (%s)' %(self.person, desc, self.start_date.year)
        return str

    @models.permalink
    def get_absolute_url(self):
        if self.office:
            return ('gv-term-detail', None, {'office_slug': self.office.slug, })
        else:
            return None

class Person(models.Model):
    """Person model."""
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    first_name = models.CharField(_('first name'), blank=True, max_length=100)
    middle_name = models.CharField(_('middle name'), blank=True, max_length=100)
    last_name = models.CharField(_('last name'), blank=True, max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    user = models.ForeignKey(User, blank=True, null=True, help_text='If the person is an existing user of your site.')
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    member = models.BooleanField(_('Member'), default=True, help_text='Is this person a member of the organization?')
    phone = PhoneNumberField(_('Phone'), blank=True, null=True)
    email = models.EmailField(_('Email'), blank=True, null=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
        ordering = ('last_name', 'first_name',)

    def __unicode__(self):
        return u'%s' % self.full_name

    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @models.permalink
    def get_absolute_url(self):
        return ('gv-person-detail', None, {'slug': self.slug})

class Meeting(TimeStampedModel, Event):
    '''
    Meeting model.

    A general meeting model. 
    '''
    group = models.ForeignKey(Group)
    agenda = models.TextField(_('Agenda'), blank=True, null=True)
    business_arising=models.TextField(_('Business arising'), blank=True, null=True)

    board_objects = BoardMeetingManager()

    class Meta:
        verbose_name = _('Meeting')
        verbose_name_plural = _('Meetings')
        ordering = ('start',)

    def __unicode__(self):
        return u'%s meeting - %s' % (self.group, self.start)

    @models.permalink
    def get_absolute_url(self):
        return ('gv-meeting-detail', (), {'slug': self.group.slug, 'year': self.start.year, 'month': self.start.month, })

    @property
    def start_date(self):
        return self.event.start.date

    @property
    def start_time(self):
        return self.event.start.time

    @property
    def end_date(self):
        return self.event.end.date

    @property
    def end_time(self):
        return self.event.end.time

class Minutes(TimeStampedModel):
    meeting = models.ForeignKey(Meeting)
    members_present = models.ManyToManyField(Term)
    others_present= models.ManyToManyField(Person)
    content = models.TextField(_('Content'))
    signed = models.ForeignKey(Person, related_name="signed_by")
    signed_date = models.DateField(_('Signed date'), default=datetime.now())

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Minutes')
        verbose_name_plural = _('Minutes')
        ordering = ('meeting',)

    def __unicode__(self):
        return u'Minutes from %s' % (self.meeting)

    @models.permalink
    def get_absolute_url(self):
        return ('gv-minutes-detail', (), {'slug':self.meeting.meeting.group.slug, 'year': self.meeting.meeting.start.year, 'month': self.meeting.meeting.event.start.month, })
