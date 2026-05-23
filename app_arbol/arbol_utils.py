from .models import Nodo


def obtener_hijos(nodo):
    """Retorna los hijos directos de un nodo"""
    return nodo.hijos.all()


def obtener_ancestros(nodo):
    """Retorna la lista de ancestros desde la raiz hasta el nodo"""
    ancestros = []
    actual = nodo
    while actual.padre is not None:
        actual = actual.padre
        ancestros.insert(0, actual)
    return ancestros


def obtener_descendientes(nodo):
    """Retorna todos los descendientes de un nodo de forma recursiva"""
    descendientes = []
    for hijo in nodo.hijos.all():
        descendientes.append(hijo)
        descendientes.extend(obtener_descendientes(hijo))
    return descendientes


def construir_arbol(contexto):
    """Construye un arbol completo para un contexto dado"""
    raices = Nodo.objects.filter(contexto=contexto, padre__isnull=True).order_by('orden')
    return [_construir_subarbol(raiz) for raiz in raices]


def _construir_subarbol(nodo):
    """Construye un subarbol de forma recursiva"""
    return {
        'nodo': nodo,
        'hijos': [_construir_subarbol(hijo) for hijo in nodo.hijos.all().order_by('orden')]
    }


def aplanar_arbol(arbol):
    """Convierte un arbol anidado en una lista plana con niveles"""
    resultado = []
    for item in arbol:
        resultado.append((item['nodo'], item['nodo'].nivel))
        resultado.extend(aplanar_arbol(item['hijos']))
    return resultado


def es_hoja(nodo):
    """Verifica si un nodo es hoja (sin hijos)"""
    return not nodo.hijos.exists()
