from django.apps import AppConfig


class ProfillerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiller'


    def ready(self):
        import profiller.signals    #import'u yukarıda degil de burada yapmamızın nedeni, profiller apini signals'da da kullanıyoruz ve orada yüklenmeden burada çekersek hata alırız.