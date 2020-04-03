from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from profiles.models import Developer, Provider


class DeveloperInline(admin.StackedInline):
    model = Developer
    can_delete = False
    verbose_name_plural = 'Developer'
    fk_name = 'user'


class ProviderInline(admin.StackedInline):
    model = Provider
    can_delete = False
    verbose_name_plural = 'Provider'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (DeveloperInline, ProviderInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)