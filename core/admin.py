from django.contrib import admin
from .models import User, Profile


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)

admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
