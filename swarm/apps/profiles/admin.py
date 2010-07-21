from django.contrib import admin
from swarm.apps.profiles.models import UserProfile
admin.autodiscover()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('vanity_name',)

admin.site.register(UserProfile, UserProfileAdmin)