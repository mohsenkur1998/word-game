from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('random', views.random_name, name='random'),
    path('name', views.students, name='students'),
    path('delete/<int:id_name>', views.delete_name, name='delete_name'),
    path('pick', views.pick_name, name='pick'),
    path('first', views.first_pick, name='first'),
    path('result', views.result, name='result'),
    path('delete_all', views.delete_data, name='delete_all'),
    path('timer', views.timer, name='timer'),
    # path('delete_student/<str:student>', views.name_delete, name='delete_object')
]