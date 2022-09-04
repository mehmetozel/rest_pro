from rest_framework.generics import GenericAPIView
from kitaplar.api.serializers import YorumSerializer, KitapSerializer
from kitaplar.models import Kitap,Yorum
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from kitaplar.api.permissions import IsAdminUserOrReadOnly, IsYorumSahibiOrReadOnly
from rest_framework.exceptions import ValidationError
from kitaplar.api.pagination import SmallPagination, LargePagination



class KitapListCreateApiView(generics.ListCreateAPIView):
    queryset = Kitap.objects.all().order_by('-id')   #ListCreateAPIView içerisinde GenericAPIView'i inherit ediyor ve o da queryset ve serializer_class atamalarının yapılmasını bekliyor. O yüzden verildiler.
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = SmallPagination


class KitapDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class YorumCreateAPIView(generics.CreateAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer

    def perform_create(self, serializer):  #?????????????????????? perform_create'i yeniden tanımlıyoruz. CreateAPIView'ün kullandığı CreateModelMixin'deki perform_create methodunun kullandığı serializeri tanımlamak için methodu tekrar tanımladık burada.
        #path('kitaplar/<int:pk>/yorum_yap', api_views.YorumCreateApiView.as_view(), name='kitap-yorumla'),
        kitap_pk = self.kwargs.get('kitap_pk')
        kitap = get_object_or_404(Kitap, pk=kitap_pk)
        kullanici = self.request.user   #yorum yapan kullanıcıyı bu şekilde cekiyoruz
        yorumlar_xx = Yorum.objects.filter(kitap=kitap, yorum_sahibi=kullanici)  ##ÖNEMLİ. (kitap ve yorum_sahibi alanları ForeignKey ile Kitap model'den çekildigi için burada karşılıkları veriliyor. ders7, 14:23)
        if yorumlar_xx.exists():
            raise ValidationError('Bir kitaba sadece bir yorum yapabilirsiniz!')
        serializer.save(kitap=kitap, yorum_sahibi=kullanici)


        
class YorumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer
    permission_classes = [IsYorumSahibiOrReadOnly]





'''class KitapListCreateApiView(CreateModelMixin, ListModelMixin, GenericAPIView):  # GenericAPIView,Base class for all other generic views.
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer


    #listelemek için
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    #Yaratabilmek için
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
'''