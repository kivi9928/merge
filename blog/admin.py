from .models import Post, User,Category,Tag,Comment
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
import csv
def download_csv(modeladmin, request, queryset):
    f = open('some.csv','w')
    writer = csv.writer(f)
    writer.writerow (['author', 'category', 'title', 'text', 'tag', 'created_date', 'published_date'])
    for s in queryset:
        writer.writerow([ s.author, s.category, s.title, s.text, s.tag, s.created_date, s.published_date])
    
    
    download_csv.short_description = "Download CSV file for selected stats."
   

class PostAdmin( admin.ModelAdmin):

    actions = [download_csv]

admin.site.register(Post,PostAdmin)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
