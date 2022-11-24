from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    # GET パラメータの一部の置き換え
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    
    return url_dict.urlencode()
