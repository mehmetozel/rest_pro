import os
import random
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitap_pazari.settings')

import django
django.setup()
### Modellerimize ve django içeriklerine erişmek için yukarıdaki gibi ayarlamaları yapmamız lazım
### SIRALAMA ÇOK ÖNEMLİ

from django.contrib.auth.models import User

from faker import Faker

from kitaplar.api.serializers import KitapSerializer

def set_user(fakegen=None):
    if fakegen is None:
        fakegen = Faker(['en_US'])

    f_name = fakegen.first_name()
    l_name = fakegen.last_name()
    u_name = f_name.lower() + '_' + l_name.lower()
    email = f'{u_name}@{fakegen.domain_name()}'

    user_check = User.objects.filter(username=u_name)
	##### BÖYLE BİR USERNAME VARSA HATA ALACAĞIZ BUNUN İÇİN BİR VALIDATION YAPIYORUZ
    while user_check.exists():
        print(f'Böyle bir kullanıcı var zaten: {u_name}')
        u_name = f_name + '_' + l_name + str(random.randrange(1, 999))
        user_check = User.objects.filter(username=u_name)  #Burası False dönene kadar while dönecek. burası false döndügübir algeçip yeni kullanıcı yaratacak


    user=User(
        username=u_name,
        first_name=f_name,
        last_name=l_name,
        email=email,
    )

    user.set_password('testing123')
    user.save()

    user_check = User.objects.filter(username=u_name)[0]
    print(f'Kullanici {user_check.username}, {user_check.id} id numarası ile kaydedildi. ')


from pprint import pprint
def kitap_ekle(konu):
    fake = Faker(['en_US'])
    url = 'http://openlibrary.org/search.json'
    payload = {'q': konu}
    response = requests.get(url, params=payload)

    if response.status_code != 200:
        print('Hatali istek yapildi!', response.status_code) #hatalı islem oldugunu ve yanında kodunu veriyoruz
        return

    jsn = response.json()
    kitaplar = jsn.get('docs')

    for kitap in kitaplar:
        kitap_adi = kitap.get('title')
        data = dict(
#ÖNEMLİ!!! isim, yazar, yayin_tarihi alanlarını doldurmak zorundayız, Kitap modelde var. Serializer kullanmak istiyorsak zorunlu.
            isim=kitap_adi,
            yazar=kitap.get('author_name')[0],
            yayin_tarihi = fake.date_time_between(start_date='-10y', end_date='now', tzinfo=None),

        )
####### yukarıda cektimiz datayı burada dict olarak database'e kaydediyoruz
        serializer = KitapSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('Kitap kaydedildi', kitap_adi)
        else:
            print(serializer.errors)