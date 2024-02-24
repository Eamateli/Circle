from django.contrib import admin
from django.contrib.auth.models import Group, User
# Undergister Groups
admin.site.unregister(Group)

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    
# Unregister initial User
admin.site.unregister(User)
# Reregister User
admin.site.register(User, UserAdmin)