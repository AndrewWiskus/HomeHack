from django.urls import path     
from . import views

urlpatterns=[
    path('', views.index),
    path('register', views.register),
    path('about', views.about),
    path('create_user', views.register_user),
    path('login', views.login),
    path('dash', views.dash),
    path('logout', views.logout),
    path('create_project', views.create_project),
    path('like/<int:user_id>/<int:project_id>', views.like),
    path('delete/<int:project_id>',views.delete_project),
    path('user_projects/<int:user_id>', views.user_projects),
    path('edit_account/<int:user_id>',views.edit_account),
    path('update_user/<int:user_id>', views.update),
    path('project_page/<int:project_id>', views.project_page),
    path('edit_project/<int:project_id>', views.edit_project),
    path('update_project/<int:project_id>', views.update_project),
    path('create_comment/<int:project_id>', views.create_comm),
    path('comm_delete/<int:comm_id>/<int:project_id>', views.delete_comm),
    path('search_projects', views.search_projects),
    path('get_project_queryset', views.get_project_queryset)
]
