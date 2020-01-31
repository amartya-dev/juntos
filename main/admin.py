from django.contrib import admin
from main.models import Profile, News, HighlightedEvents, Donations, Causes


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'ein_number', 'organization_user')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status', 'organization')
    list_filter = ('status', 'publish', 'organization')
    search_fields = ('title', 'news_details')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    raw_id_fields = ('organization',)


@admin.register(HighlightedEvents)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_start_date', 'event_end_date', 'organization')
    list_filter = ('event_start_date', 'event_end_date', 'organization')
    search_fields = ('event_name', 'event_description')
    prepopulated_fields = {'slug': ('event_name',)}
    raw_id_fields = ('organization',)


@admin.register(Donations)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('amount', 'organization', 'success', 'donation_timestamp')
    list_filter = ('organization', 'success')
    raw_id_fields = ('organization',)


@admin.register(Causes)
class CauseAdmin(admin.ModelAdmin):
    list_display = ('cause_name', 'organization')
    list_filter = ('organization',)
    search_fields = ('cause_name', 'cause_description')
    raw_id_fields = ('organization',)
