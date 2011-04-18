from django.contrib import admin
from committees.models import *

class TermAdmin(admin.ModelAdmin):
    list_display = ('person', 'office', 'group', 'start', 'end', 'alternate','is_active',)
    search_fields = ('person','group',)
    list_filter = ( 'person','group',  )

    def is_active(self, object_):
        return object_.active
    is_active.short_description=u'Active?'
    is_active.boolean = True

admin.site.register(Term, TermAdmin)
    
admin.site.register(GroupType)
admin.site.register(GroupPhoto)
admin.site.register(Group)
admin.site.register(Office)
admin.site.register(Person)
admin.site.register(Meeting)
admin.site.register(Minutes)
