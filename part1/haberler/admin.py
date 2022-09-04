from django.contrib import admin

# Register your models here.


from haberler.models import Makale, Gazeteci


admin.site.register(Makale),
admin.site.register(Gazeteci),
