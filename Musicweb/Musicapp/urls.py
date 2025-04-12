from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'), 
    path('add_song/', views.add_song, name='add_song'),
    path('playsong/<int:song_id>/', views.playsong, name='playsong'),
    path('search/', views.search_view, name='search'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist'),
    path('add_to_playlist/<int:song_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('delete_song_by_name/', views.delete_song_by_name, name='delete_song_by_name'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('rename_playlist/<int:playlist_id>/', views.rename_playlist, name='rename_playlist'),
    path('delete_playlist/<int:playlist_id>/', views.delete_playlist, name='delete_playlist'),
    path('remove_from_playlist/<int:playlist_id>/<int:song_id>/', views.remove_from_playlist, name='remove_from_playlist'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)