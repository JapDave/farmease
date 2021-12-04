from django import template

register = template.Library()

@register.filter(name='private')
def private(obj, attribute):
    return getattr(obj, attribute)

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def define(val=None):
  return val