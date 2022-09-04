from rest_framework import serializers
from haberler.models import Makale, Gazeteci

from datetime import datetime
from datetime import date
from django.utils.timesince import timesince




class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    #yazar = serializers.StringRelatedField() #Bunu yazsaydik 'yazar = Edward Norton' gibi ismini alırdik. Bu olmazsa yazar id'sini aliyoruz.
    #yazar = GazeteciSerializer()   #yazarin ayrintilari alinir bu sekilde. önceden sadece id'si yazarken simdi adi,soyadi,biyografisi de yazi

    class Meta:
        model = Makale
        fields = '__all__'
        #fields = ['yazar', 'baslik', 'metin']
        #exclude = ['metin']
        read_only_fields = ['id', 'yaratilma_tarihi', 'guncellenme_tarihi']

    def get_time_since_pub(self, obj):  #time_since_pub için yazılıyor ve basına olustururken get_ koymak gerekiyor instance'ın, yoksa attribute error verir. #obj, Makale modelden data çekmek için gerekli olan instance
        now = datetime.now()
        pub_date = obj.yayimlanma_tarihi
        if obj.aktif == True:        #makale aktifte degilse yayimlanma tarihini güncellememek için
            time_delta = timesince(pub_date, now)   #yayimlanma tarihinden şimdiyi çıkarıyor, farkı veriyor
            return time_delta
        else:
            return 'Aktif degil!'



    def validate_yayimlanma_tarihi(self, tarihdegeri):
        today = date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError('Yayimlanma tarihi hatalı')
        return tarihdegeri

#### STANDART SERIALIZER
class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  #Makale model'ı yaratılırken yani db'de bir satır yaratılırken otomatikman id numarası da yaratılıyor. O yüzden bunu olusturuyoruz.
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayimlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True) #bir sey yapmana gerek yok diyoruz cünkü yaratılan tarih degismiyor.
    guncelleneme_tarihi = serializers.DateTimeField(read_only=True)


#json post requesti gelirse obje de create edebilmeyi sağlar bu metod.
    def create(self, validated_data): #serializer otomatik olarak validasyon yapıyor ve bu datayı kullanıyoruz.
        print(validated_data)
        return Makale.objects.create(**validated_data) #validated_data dict olarak geldiği için kwargs olarak giriliyor


#json put requesti ile güncellenmek istenirse diye update metodu.
    def update(self, instance, validated_data):  #update ederken zaten elimizde olan bir datayı gönderiyoruz bu yüzden instance ekliyoruz.
        instance.yazar = validated_data.get('yazar', instance.yazar)   #validated_data'da yazar'ında karsısında bir değer varsa bunu get et yani al, eğer yoksa yani yazaranlamında bir güncelleme yapılmadıysa instance'daki yazar'ı al bunu kullan, demek ki bir degisiklik olmamıs demektir.
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayimlanma_tarihi = validated_data.get('yayimlanma_tarihi', instance.yayimlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance

    def validate(self, data): #object level  #To do any other validation that requires access to multiple fields, add a method called .validate() to your Serializer subclass.
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Baslik ve Aciklama alanlari olamaz.')
        return data

    def validate_baslik(self, value):  #field level  ....#kontrol edilmek istenen field 'validate_...' üc nokta olarak belirtilen yere yazilmali
        if len(value) < 20:
            raise serializers.ValidationError(f'Baslik alanı min 20 karakter olmalı. Siz {len(value)} girdiniz.')
        return value




class GazeteciSerializer(serializers.ModelSerializer):


    #makaleler = MakaleSerializer(many=True, read_only=True)   #makale vermeden gazeteci yani yazar yaratabilmek için read_only=True olarak verildi.
                                                            #makaleler, Makale modul- yazar'dan related_name ile ilişkili.
    makaleler = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='makele-detay')


    class Meta:
        model = Gazeteci
        fields = '__all__'
