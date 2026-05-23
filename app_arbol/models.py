from django.db import models


class Contexto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    icono = models.CharField(max_length=10, default="📁", verbose_name="Icono")

    class Meta:
        verbose_name = "Contexto"
        verbose_name_plural = "Contextos"

    def __str__(self):
        return self.nombre

    def cantidad_nodos(self):
        return self.nodo_set.count()


class Nodo(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    padre = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='hijos', verbose_name="Padre"
    )
    contexto = models.ForeignKey(
        Contexto, on_delete=models.CASCADE, verbose_name="Contexto"
    )
    nivel = models.IntegerField(default=0, verbose_name="Nivel")
    orden = models.IntegerField(default=0, verbose_name="Orden")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Nodo"
        verbose_name_plural = "Nodos"
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

    def es_raiz(self):
        return self.padre is None

    def es_hoja(self):
        return not self.hijos.exists()
