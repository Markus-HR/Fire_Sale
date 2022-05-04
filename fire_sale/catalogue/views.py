from django.shortcuts import render
from catalogue.models import Postings

# Create your views here.
from django.shortcuts import render


# Create your views here.
def index(request):
    context = {'postings': Postings.objects.all()}
    return render(request, 'catalogue/index.html', context)
