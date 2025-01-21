from django.contrib import admin
from apps.events.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status', 'seats_available', 'created_at')
    list_filter = ('status', 'date', 'hall')
    search_fields = ('title', 'description')
    ordering = ('-date',)
    readonly_fields = ('seats_available', 'created_at', 'updated_at')
    fieldsets = (
        ('Event details', {
            'fields': ('title', 'description', 'date', 'end_date', 'status')
        }),
        ('place and Event', {
            'fields': ('hall', 'capacity', 'seats_available')
        }),
        ('Price and Image', {
            'fields': ('price', 'image')
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at')
        }),
    )
