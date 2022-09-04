from rest_framework import permissions
#from rest_framework.permissions import SAFE_METHODS


#SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsAdminUserOrReadOnly(permissions.IsAdminUser):  #sadece görüntüleme izni için
    def has_permission(self, request, view):
       is_admin = super().has_permission(request, view)
       return request.method in permissions.SAFE_METHODS or is_admin
      # return request.method in permissions.SAFE_METHODS or bool(request.user and request.user.is_staff) #üstteki super() metdodlu satır olmasaydı bu satır yeterli olurdu.

class IsYorumSahibiOrReadOnly(permissions.BasePermission):   #baskasının profilinin biosu vs degistirmeyi engellemek için
    def has_object_permission(self, request, view, obj):
       if request.method in permissions.SAFE_METHODS:
           return True

       return request.user == obj.yorum_sahibi
