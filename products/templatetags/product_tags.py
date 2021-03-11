from django import template

register = template.Library()


# filtro personalisado para disposição dos produtos
@register.filter()
def remainder(n):
    return n % 3
