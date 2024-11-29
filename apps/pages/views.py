from django.shortcuts import render


def index(request):
    template_name = "pages/index.html"
    return render(request, template_name)
