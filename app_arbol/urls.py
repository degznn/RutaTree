from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_index, name='vista_index'),
    path('contextos/', views.vista_contextos, name='vista_contextos'),
    path('arbol/<int:contexto_id>/', views.vista_arbol, name='vista_arbol'),
    path('nodo/<int:nodo_id>/', views.vista_nodo, name='vista_nodo'),
    path('nodo/crear/', views.vista_crear_nodo, name='vista_crear_nodo'),
    path('nodo/<int:nodo_id>/editar/', views.vista_editar_nodo, name='vista_editar_nodo'),
    path('nodo/<int:nodo_id>/eliminar/', views.vista_eliminar_nodo, name='vista_eliminar_nodo'),
    path('buscar/', views.vista_buscar, name='vista_buscar'),
    path('acerca/', views.vista_acerca, name='vista_acerca'),
]
