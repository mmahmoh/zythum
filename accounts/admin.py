from django.contrib import admin
from .models import User
from django_use_email_as_username.admin import BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'national_phone', 'is_staff']

    def get_fieldsets(self, request, obj=None):
        first, personal, *rest = self.fieldsets
        personal = (
            'Personal info', {
                'fields': (
                    'first_name', 'last_name', 'phone'
                )
            }
        )
        rest.insert(0, first)
        rest.insert(1, personal)
        self.fieldsets = tuple(rest)
        return super(UserAdmin, self).get_fieldsets(request, obj)

    # def get_list_display(self, request):
    #     display = list(self.list_display)
    #     if 'phone' not in display:
    #         display.insert(3, 'phone')
    #         self.list_display = tuple(display)
    #     return super(UserAdmin, self).get_list_display(request)

    @admin.display(description='phone', ordering='phone')
    def national_phone(self, obj: User):
        if obj.phone:
            return obj.phone.as_national
