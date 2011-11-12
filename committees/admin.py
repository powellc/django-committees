from django.contrib import admin
from committees.models import *

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 5
    max_num = 15


class TermAdmin(admin.ModelAdmin):
    list_display = ('person', 'office', 'group', 'start', 'end', 'alternate','is_active',)
    search_fields = ('person','group',)
    list_filter = ( 'person','group',  )

    def is_active(self, object_):
        return object_.active
    is_active.short_description=u'Active?'
    is_active.boolean = True

admin.site.register(Term, TermAdmin)

class MinutesAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'draft', 'call_to_order', 'adjournment', 'signed', 'signed_date',)
    search_fields = ('content','members_present','meeting',)
    filter_horizontal = ('members_present', 'guests_present','members_present_new','guests_present',)
    inlines = [
        AttachmentInline,
    ]

admin.site.register(Minutes, MinutesAdmin)
    
admin.site.register(GroupType)
admin.site.register(GroupPhoto)
admin.site.register(Group)
admin.site.register(Office)
admin.site.register(Person)
admin.site.register(Meeting)
