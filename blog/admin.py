from .models import Post, User,Category,Tag,Comment
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
import csv
from django.http import HttpResponse


def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"
   

class PostAdmin( admin.ModelAdmin): 
    list_filter   = ("author","category","title","tag","created_date","published_date","slug")
    readonly_fields = ("slug",)
    actions = [download_csv]

class CategoeyAdmin( admin.ModelAdmin): 
    
    readonly_fields = ("slug",)
    
class TagAdmin( admin.ModelAdmin): 
    
    readonly_fields = ("slug",)
   
admin.site.register(Post,PostAdmin)
admin.site.register(User)
admin.site.register(Category,CategoeyAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Comment)
