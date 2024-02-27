from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Noise


# Undergister Groups
admin.site.unregister(Group)

# Mix Profile info into User info 

class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]
    
# Unregister initial User
admin.site.unregister(User)
# Reregister User
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Register Noises
admin.site.register(Noise)


