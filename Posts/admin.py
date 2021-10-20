from django.contrib import admin

# Register your models here.
from .models import Post, SavedPost, PostImage, PostQuestion, Order, Reserve
admin.site.register(Post)
admin.site.register(SavedPost)
admin.site.register(PostImage)
admin.site.register(PostQuestion)
admin.site.register(Order)
admin.site.register(Reserve)