from django.contrib import admin
from .models import Contexto, Nodo


class NodoInline(admin.TabularInline):
    model = Nodo
    fk_name = 'padre'
    extra = 1
    fields = ['nombre', 'orden']
    verbose_name = "Hijo"
    verbose_name_plural = "Hijos"


@admin.register(Contexto)
class ContextoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono', 'cantidad_nodos']
    search_fields = ['nombre', 'descripcion']


@admin.register(Nodo)
class NodoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contexto', 'nivel', 'orden', 'fecha_creacion']
    list_filter = ['contexto', 'nivel']
    search_fields = ['nombre', 'descripcion']
    inlines = [NodoInline]
