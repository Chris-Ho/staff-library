from django import template

register = template.Library()

#decorator registers function as custom template filter
@register.filter
def getItem(myDict, key): #used for accessing dictionary items
    return myDict.get(key, None)