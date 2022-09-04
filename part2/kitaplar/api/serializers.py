from rest_framework import serializers
from kitaplar.models import Kitap, Yorum



class YorumSerializer(serializers.ModelSerializer):
    yorum_sahibi = serializers.StringRelatedField(read_only=True)  #yarımcunun id olarak degil de ismen görünmesi için
                                                                    #read_only=True dememizin nedeni, yorum_sahibi views'de yaratılıyor.
    class Meta:
        model = Yorum
        exclude = ['kitap']


class KitapSerializer(serializers.ModelSerializer):
    yorumlar = YorumSerializer(many=True, read_only=True)  #read_only amacı, yeni bir kitap yaratıldıgında yorum girmeden de yaratabilsin diye
    class Meta:
        model = Kitap
        fields = '__all__'

