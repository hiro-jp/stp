from django import template

register = template.Library()

# ２つのリストを１つのforループで並列で回すため、
# python の zip を実装する。
# ただし、リストは２つまで。
# 参考 https://stackoverflow.com/questions/2415865/iterating-through-two-lists-in-django-templates
@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)
