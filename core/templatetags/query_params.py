from django import template

register = template.Library()


@register.simple_tag
def add_query_params(request, key, value):
    """Добавляет или обновляет параметры запроса, возвращает строку запроса"""
    qd = request.GET.copy()
    qd[key] = value
    return qd.urlencode()
