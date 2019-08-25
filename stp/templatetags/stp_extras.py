from django import template

register = template.Library()

# ２つのリストを１つのforループで並列で回すため、
# python の zip を実装する。
# ただし、リストは２つまで。
# 参考 https://stackoverflow.com/questions/2415865/iterating-through-two-lists-in-django-templates
@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)


@register.filter(name='verbose_name_filter')
def verbose_name_filter(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()
