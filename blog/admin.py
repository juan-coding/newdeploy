from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish', 'tag', 'status']
    list_filter = ['tag']
    search_fields = ['title', 'body']
    list_display_links = ['publish']
    list_editable = ['title', 'status', 'tag']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)