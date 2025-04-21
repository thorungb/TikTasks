from django.contrib import admin
from .models import TodoItem

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    """
    Admin interface for TodoItem model.
    """
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status', 'user')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    list_editable = ('status',)
    actions = ['mark_as_completed', 'mark_as_incomplete']
