from django import forms

from .models import FishQuery

class AddFishQueryForm(forms.ModelForm):

    class Meta:
        model = FishQuery
        fields = ('location', 'location_id', 'species', 'species_id', 'year',)