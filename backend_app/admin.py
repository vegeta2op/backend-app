from django.contrib import admin
from .models import Task, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass 

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)  
    list_display = ('title', 'due_date', 'status') 
    list_filter = ('status', 'due_date')  
    search_fields = ('title', 'description') 
    fieldsets = (
        ('Task Details', {
            'fields': ('title', 'description', 'due_date', 'status', 'tags')
        }),
        ('Timestamp', {
            'fields': ('timestamp',),
            'classes': ('collapse',)  
        }),
    )
