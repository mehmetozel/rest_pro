from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator


class Kitap(models.Model):
    isim = models.CharField(max_length=250)
    yazar = models.CharField(max_length=250)
    aciklama = models.TextField(blank=True, null=True)
    yaratilma_tarihi = models.DateTimeField(auto_now_add=True) #yaratildigi anki tarih için
    guncellenme_tarihi = models.DateTimeField(auto_now=True) #her güncellendigi anki tarihi alir
    yayin_tarihi = models.DateTimeField()

    def __str__(self):
        return f'{self.isim} - {self.yazar}'


class Yorum(models.Model):
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, related_name='yorumlar')  #on_delete ile kitap silindiginde yorumlar da silinsin
                                                                                            #related_name, Kitap objesini çektiğimizde Yorum querysini de yapmak için
    #yorum_sahibi = models.CharField(max_length=250)
    yorum_sahibi = models.ForeignKey(User,on_delete=models.CASCADE, related_name='kullanici_yorumlari')
    yorum = models.TextField(blank=True, null=True)
    yaratilma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    degerlendirme = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],)  #yorumları değerlendirirken 1 ve 5 arası puanlama için
    
    def __str__(self):
        return str(self.degerlendirme)