from django.contrib import admin
from .models import Program,DepartmentPoints
# Register your models here.
class ProgramAdmin(admin.ModelAdmin):
        filter_horizontal=('registered_users','winners','winners_position')
        def save_related(self, request, form, formsets, change):
            super().save_related(request, form, formsets, change)
            form.instance.update_score()
admin.site.register(Program,ProgramAdmin)
admin.site.register(DepartmentPoints)