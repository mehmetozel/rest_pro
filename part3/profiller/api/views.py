from profiller.api.serializers import ProfilSerializer, ProfilDurumSerializer, ProfilFotoSerializer
from profiller.models import Profil, ProfilDurum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
#from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from profiller.api.permissions import KendiProfiliOrReadOnly, DurumSahibiOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

#ÖNEMLİ: Tek bir view ile tüm işlemleri halledebiliyoruz.Fonsiyonel ayrıntılandırmasını urls'de yapıyoruz.

class ProfilViewSet(
        GenericViewSet,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,):

    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated, KendiProfiliOrReadOnly]
    filter_backends = [SearchFilter]  #liste yapısı, yani birden fazla seçenek ekleyebiliriz.
    search_fields = ['sehir']   #birden fazla alan ekleyebilirizi profil modelimizden.



class ProfilDurumViewSet(ModelViewSet):

    queryset = ProfilDurum.objects.all()
    serializer_class = ProfilDurumSerializer
    permission_classes = [IsAuthenticated,DurumSahibiOrReadOnly]

    def perform_create(self, serializer):   #bu methodu vermezsek yani user_profil verilmezse durum olusturmak istedigimizde integrity error aliriz
        user_profil = self.request.user.profil
        serializer.save(user_profil=user_profil)

    def get_queryset(self):
        queryset = ProfilDurum.objects.all()
        username = self.request.query_params.get('username', None)  #gelen request içerisinde username ile ilgili parametre var mı bakacak yoksa hata çevirme None çevir diyoruz burada.
        if username is not None:
            queryset = queryset.filter(user_profil__user__username=username)
        return queryset


class ProfilFotoUpdateView(generics.UpdateAPIView):

    serializer_class = ProfilFotoSerializer
    permission_classes = [IsAuthenticated]  #IsAuthenticated dısında baska permission class yazmamamızın sebebi get_object'te zaten login olmus kullanıcı olması yeterli.
                                            #Ayrıca UpdateAPIView ile, sadece Put requeste izin vermiş oluyoruz.

    #Neden queryset vermedik? Cünkü biz tek bir profil nesnesi ile ilgileniyoruz tüm querysetle degil. Ve bizim
    #alacagımız profil nesnesinin login olmus kullanıcının profili olması lazım. Ve biz bu işlemi, GenericAPIView ile
    #gelen get_object() methodu içerisinde cözüyoruz. Bu sebeple hem queryset vermemize hem de ekstra permission
    #yazmamıza gerek kalmadı.

    def get_object(self):
        profil_nesnesi = self.request.user.profil
        return profil_nesnesi

#ProfilFotoSerializer'da field olarak sadece 'foto' verildiği için sadece bu view'da foto update eder.



'''
class ProfilList(generics.ListAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAuthenticated]
'''