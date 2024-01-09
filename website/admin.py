from django.contrib import admin
from website.admin_forms import *
from website.models import  *
# Register your models here.


class PageAdmin(admin.ModelAdmin):
    form = PageForm
    # inlines = [CascadeStyleInline,JavaScriptInline]
    class Meta:
        model = Page


admin.site.register(Page,PageAdmin)
admin.site.register(Widget)
admin.site.register(JsonSerializer)
admin.site.register(Website)
admin.site.register(File)

@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    form = ApiForm
