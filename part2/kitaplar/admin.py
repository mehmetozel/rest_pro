from django.contrib import admin

# Register your models here.


from kitaplar.models import Kitap, Yorum

admin.site.register(Kitap)
admin.site.register(Yorum)