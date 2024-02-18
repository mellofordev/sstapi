from django.contrib import admin
from .models import Program,DepartmentPoints,Team
# Register your models here.'
admin.site.site_header = 'Sargam Chitram Thalam Admin'                    
admin.site.index_title = 'Sargam Chitram Thalam Admin'                
admin.site.site_title = 'Sargam Chitram Thalam Admin' 
class ProgramAdmin(admin.ModelAdmin):
        search_fields=('name',)
        filter_horizontal=('registered_users','winner_first',
                           'winner_second',
                           'winner_third'
                           )
        # readonly_fields=('name','registered_users',
        #                  'max_member_limit','program_gender_type',
        #                  'program_type','program_comes_under'
        #                  )
        def save_related(self, request, form, formsets, change):
            super().save_related(request, form, formsets, change)
            form.instance.update_score()
class TeamAdmin(admin.ModelAdmin):
        search_fields=('program__name',)
        filter_horizontal=('members',)
        readonly_fields=('team_lead','members',
                         'program','share_link',
                        )      
admin.site.register(Program,ProgramAdmin)
admin.site.register(DepartmentPoints)
admin.site.register(Team,TeamAdmin)