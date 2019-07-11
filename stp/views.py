from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'stp/index_view.html'
