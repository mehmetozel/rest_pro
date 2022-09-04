from django.urls import path, include
#from profiller.api import views
from profiller.api.views import ProfilViewSet, ProfilDurumViewSet, ProfilFotoUpdateView
from rest_framework.routers import DefaultRouter

#ProfilFotoUpdateView, bir ViewSet olmadığı için router kullanamıyoruz. O yüzden klasik bir şekilde yazdık urlpatterns içinde.

router = DefaultRouter()
router.register(r'kullanici-profilleri', ProfilViewSet)
router.register(r'durum', ProfilDurumViewSet, basename='durum')   #basename vermemizin nedeni ProfilDurumViewSet'de queryset'i direkt olarak degil de
                                                                #get_queryset metodu içerisinde vermemiz. basename'i vermezsek AssertionError aliriz.

#profil_list = ProfilViewSet.as_view({'get': 'list'})    #path içerisinde de yazilabilirdi, daha kolay okunabilmesi için böyle yaptık
#profil_detay = ProfilViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('', include(router.urls)),   #router.urls bir liste yapısı old için, router'da yapılan bütün register'ları otomatik olarak ekliyor.
    path('profil_foto/', ProfilFotoUpdateView.as_view(), name='profil-foto')


#    path('kullanici-profilleri/', profil_list, name='profiller'),
#    path('kullanici-profilleri/<int:pk>', profil_detay, name='profil-detay'),

]