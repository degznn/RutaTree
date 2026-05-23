from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Contexto, Nodo
from .arbol_utils import construir_arbol, obtener_ancestros, obtener_descendientes, aplanar_arbol


def vista_index(request):
    contextos = Contexto.objects.all()
    total_nodos = Nodo.objects.count()
    total_raices = Nodo.objects.filter(padre__isnull=True).count()
    return render(request, 'app_arbol/index.html', {
        'contextos': contextos,
        'total_nodos': total_nodos,
        'total_raices': total_raices,
    })


def vista_contextos(request):
    contextos = Contexto.objects.all()
    return render(request, 'app_arbol/contextos.html', {'contextos': contextos})


def vista_arbol(request, contexto_id):
    contexto = get_object_or_404(Contexto, id=contexto_id)
    arbol = construir_arbol(contexto)
    arbol_plano = aplanar_arbol(arbol)
    return render(request, 'app_arbol/arbol.html', {
        'contexto': contexto,
        'arbol': arbol,
        'arbol_plano': arbol_plano,
    })


def vista_nodo(request, nodo_id):
    nodo = get_object_or_404(Nodo, id=nodo_id)
    ancestros = obtener_ancestros(nodo)
    hijos = nodo.hijos.all()
    return render(request, 'app_arbol/nodo.html', {
        'nodo': nodo,
        'ancestros': ancestros,
        'hijos': hijos,
    })


def vista_crear_nodo(request):
    contextos = Contexto.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        contexto_id = request.POST.get('contexto')
        padre_id = request.POST.get('padre') or None
        orden = request.POST.get('orden', 0)

        contexto = get_object_or_404(Contexto, id=contexto_id)
        padre = Nodo.objects.filter(id=padre_id).first() if padre_id else None
        nivel = (padre.nivel + 1) if padre else 0

        Nodo.objects.create(
            nombre=nombre, descripcion=descripcion,
            contexto=contexto, padre=padre,
            nivel=nivel, orden=orden
        )
        return redirect('vista_arbol', contexto_id=contexto.id)

    contexto_id = request.GET.get('contexto')
    padre_id = request.GET.get('padre')
    contexto_seleccionado = None
    padre_seleccionado = None
    nodos_disponibles = []

    if contexto_id:
        contexto_seleccionado = get_object_or_404(Contexto, id=contexto_id)
        nodos_disponibles = Nodo.objects.filter(contexto=contexto_seleccionado)
    if padre_id:
        padre_seleccionado = get_object_or_404(Nodo, id=padre_id)

    return render(request, 'app_arbol/crear_nodo.html', {
        'contextos': contextos,
        'contexto_seleccionado': contexto_seleccionado,
        'padre_seleccionado': padre_seleccionado,
        'nodos_disponibles': nodos_disponibles,
    })


def vista_editar_nodo(request, nodo_id):
    nodo = get_object_or_404(Nodo, id=nodo_id)
    contextos = Contexto.objects.all()
    nodos_mismo_contexto = Nodo.objects.filter(contexto=nodo.contexto).exclude(id=nodo.id)

    if request.method == 'POST':
        nodo.nombre = request.POST.get('nombre')
        nodo.descripcion = request.POST.get('descripcion', '')
        nuevo_padre_id = request.POST.get('padre') or None
        nodo.orden = request.POST.get('orden', 0)

        if nuevo_padre_id:
            nuevo_padre = get_object_or_404(Nodo, id=nuevo_padre_id)
            nodo.padre = nuevo_padre
            nodo.nivel = nuevo_padre.nivel + 1
        else:
            nodo.padre = None
            nodo.nivel = 0

        nodo.save()
        return redirect('vista_nodo', nodo_id=nodo.id)

    return render(request, 'app_arbol/editar_nodo.html', {
        'nodo': nodo,
        'contextos': contextos,
        'nodos_mismo_contexto': nodos_mismo_contexto,
    })


def vista_eliminar_nodo(request, nodo_id):
    nodo = get_object_or_404(Nodo, id=nodo_id)
    if request.method == 'POST':
        contexto_id = nodo.contexto.id
        nodo.delete()
        return redirect('vista_arbol', contexto_id=contexto_id)
    descendientes = obtener_descendientes(nodo)
    return render(request, 'app_arbol/eliminar_nodo.html', {
        'nodo': nodo,
        'descendientes': descendientes,
    })


def vista_buscar(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        resultados = Nodo.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    return render(request, 'app_arbol/buscar.html', {
        'query': query,
        'resultados': resultados,
    })


def vista_acerca(request):
    return render(request, 'app_arbol/acerca.html')
