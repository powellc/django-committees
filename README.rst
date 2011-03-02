django-committees
==============
:author: Colin Powell
:date: 2011-02-19
:by: One Cardinal Web Development
:license: GPLv3

A simple pluggable django application for managing documents in a small not-for-profit organization.

At a small organization, we have a governing board, composed of variable-length termed seats, term limits, alternate members, offices: a president, vice president, secretary and treasurer. The rest of the governing is done via committees, wether standing or ad-hoc. The whole government is governed by bylaws and policies. This app should organize all these elements in one place for reference.

Models
--------

TERM_LIMIT=2

BoardOffice (Pres, vp, sec, at-large, alternate, ex-officio...)
  - title
  - slug
  - description
  - officer?
  - officer_rank (INT)

BoardTerm
  - start_date
  - end_date
  - office (Office)

BoardMember
  - Person (Profile)
  - Term (BoardTerm)

Meeting 
  - Event
  - Minutes
  - Members (BoardMember)
  - Guests (VarChar)
  - Adjourn
  
BoardMeeting (Meeting)
  - Agenda
 
Minutes
  - Meeting
  - Draft?
  - Content
  - Attachment

CommitteeMember
  - Person

Committee
  - title
  - description
  - chairs
  - members (CommitteeMember)
  - reports

CommitteeTerm
  - start_date
  - end_date
  - committee

Report
  - Date
  - Content
  - Author (Person)

URLs
-------

Just an example hook up spot:

view: index = government/ - index to show gov. board, committees, latest meetings/minutes
view: board_detail = government/board/ - detail of board make-up, past boards and minutes/meetings
view: board_meeting_detail = government/meetings/<year>/<month>/ - detail of a meeting with minutes, members, etc.
view: committee_list = government/committees/ - list of all committees and membership
view: committee_detail = government/committees/<slug> - detail of one committee
view: report_list = government/reports/<year>/<month>/<committee_slug> 
view: meeting_list = government/meetings/ - list of all meetings in the system
