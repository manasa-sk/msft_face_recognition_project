from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('registerU/', views.registerU, name='registerUser'),
    path('loginU/', views.loginU, name='loginUser'),
    path('scanR/', views.scanR, name='scanR'),
    path('cam_feed_R/', views.cam_feed, name='cam_feed_R'),
    path('cam_feed_L/', views.check_face, name='cam_feed_L'),
    path('scanL/', views.scanL, name='scanL'),
    path('dash/', views.dashboard, name='dash'),
    path('profile/', views.profile, name='profile'),
    path('showProfile/', views.showProfile, name='showProfile'),
    path('showPost/', views.showPost, name='showPost'),
    path('editProfile/', views.editForm, name='editProfile'),
    path('edit/', views.edit, name='edit'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('logout/', views.logout, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('likePost/', views.likePost, name='likePost'),
    path('deleteP/', views.delete_post, name='deleteP'),
    path('create/', views.create, name='create'),
    path('delete/', views.delete_acct, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

