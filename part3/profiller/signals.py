from django.contrib.auth.models import User
from profiller.models import Profil, ProfilDurum
from django.db.models.signals import post_save
from django.dispatch import receiver


#user yaratıldıktan hemen sonra otomatik olarak profil yaratılmasını istedigimiz için post_save kullanıyoruz.
@receiver(post_save, sender=User)
def create_profil(sender, instance,created, **kwargs):

    print(instance.username,'__created:  ', created)   #created adi öylesine verilmemiş, başka isim verince hata veriyor.
    if created:
        Profil.objects.create(user=instance) #user, Profil modeldeli ilk attribute



@receiver(post_save, sender=Profil)
def create_durum_mesaji(sender, instance,created, **kwargs):

    if created:
        ProfilDurum.objects.create(user_profil=instance, durum_mesaji=f'{instance.user.username} Klübe katildi') #yine instance olma sebebi yukarıdaki gibi yeni user yaratıldıgında mesaj verilecek.
        #user_profil ve durum mesaji, ProfilDurumu modeldeki zorunlu datalar