from django.urls import path
from . import views
app_name = 'reddead'
urlpatterns = [
     path('', views.index, name='index'),
     #need url for blob object created by js to fetch videos, not sure if this is working, for now, dont mess
     path('', views.index, name='videos'),

     
     path('characters/', views.CharacterListView.as_view(), name='characters'),
     path('characters/<int:pk>', views.CharacterDetailView.as_view(), name='character_detail'),
     #paths for create update and delete characters

     path('characters/create/', views.CharacterCreate.as_view(), name='character_create'),
     path('character/<int:pk>/update/', views.CharacterUpdate.as_view(), name='character_update'),
     path('character/<int:pk>/delete/', views.CharacterDelete.as_view(), name='character_delete'),
     #urls for group

     path('group/', views.GroupListView.as_view(), name='groups'),
     path('group/<int:pk>/', views.GroupDetailView.as_view(), name='group_detail'),

     #paths for group create, edit, delete.
     path('group/create', views.GroupCreateView.as_view(), name='group_create'),
     path('group/<int:pk>/update', views.GroupUpdateView.as_view(), name='group_update'),
     path('group/<int:pk>/delete', views.GroupDeleteView.as_view(), name='group_delete'),
     
     

     #paths for wildlife voting stuff
     path('wildlife/', views.WildlifeIndexView.as_view(), name='wildlife'),
     path('wildlife/<int:pk>/', views.WildlifeDetailView.as_view(), name='wildlife_detail'),
     path('wildlife/<int:pk>/results/', views.WildLifeResultsView.as_view(), name='results'),
     #path('<int:question_id>/vote/', views.vote, name='vote'),
     path('wildlife/<int:question_id>/vote/', views.vote, name='vote'),

   
     
     
     
     
  
    
]
