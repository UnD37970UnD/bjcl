from django.shortcuts import render
from .forms import Searchform
from .bjcl_search import web_get
from .models import result
def index(request):
    queryset = result.objects.all()
    context = {
        'object_list': queryset
    }
    if request.method == "POST":
        form = Searchform(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            web_get(search, request)
            return render(request, 'bjcl_app/results.html', context)
    form = Searchform()
    return render(request,'bjcl_app/index.html', {"form":form})

def results(request):
    return render(request,'bjcl_app/results.html')


