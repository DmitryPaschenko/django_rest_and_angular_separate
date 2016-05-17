from django.contrib import admin
from users.models import AppUser

class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'first_name', 'last_name', 'email',
                    'detailed_info', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login')

admin.site.register(AppUser, AppUserAdmin)






