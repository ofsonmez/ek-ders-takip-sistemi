from django.urls import path
from . import views

app_name = 'sistem'

urlpatterns = [
	path('', views.login_view, name='login'),
    path('index', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('donem', views.donem_excel, name='donem'),
    path('profil', views.profile, name='profile'),
    path('logout', views.logout_view, name ='logout'),
    path('dersler', views.dersler_view, name='dersler'),
    path('dersler/<int:id>', views.ders_update_view, name='update'),
    path('dersler/create', views.ders_create_view, name='create'),
    path('dersler/<int:id>/delete', views.ders_delete_view, name='delete')
]
