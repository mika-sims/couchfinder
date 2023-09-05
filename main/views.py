from django.views.generic import TemplateView


class HomepageView(TemplateView):
    """
    View for the homepage
    """
    template_name = 'index.html'
