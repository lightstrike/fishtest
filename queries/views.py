from django.shortcuts import render
from rest_framework import viewsets

from .forms import AddFishQueryForm
from .models import FishQuery
from .serializers import FishQuerySerializer


def fish_queries(request):
    if request.method == "POST":
        form = AddFishQueryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'queries/add_query.html', {'form': form})
    form = AddFishQueryForm()
    queries = FishQuery.objects.all()
    return render(request, 'queries/add_query.html',
        {'form': form, 'queries': queries})


class FishQueryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows fish queries to be viewed or edited.
    """
    queryset = FishQuery.objects.all()
    serializer_class = FishQuerySerializer