from django.contrib import admin
from .models import Category, Blog, About, SocialMediaLink, Comment
from django.contrib.auth.models import User

# Register your models here.
class BlogAdmin(admin.ModelAdmin) :
    prepopulated_fields = {'slug' : ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'author__username', 'category__category_name', 'status')
    list_editable = ('is_featured', 'status', 'author')

class AboutAdmin(admin.ModelAdmin) :
    def has_add_permission(self, request):
        count = About.objects.all().count()
        if count == 0 :
            return True
        return False


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(SocialMediaLink)
admin.site.register(Comment)