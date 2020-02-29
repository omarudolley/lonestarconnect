from django.contrib import admin
from .models import Forum,Thread,Post
# Register your models here.

admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Post)
