from django.db import models
from django.utils import timezone


"""
class Location(models.Model):
    title = models.CharField(max_length=200)
    akfg_id = models.IntegerField()

    def __str__(self):
        return "{title}: {id}".format(
            title=self.title,
            id=akfg_id)
"""

SALMON_COUNT_URL = 'https://www.adfg.alaska.gov/sf/FishCounts/index.cfm?ADFG=main.displayResults'


class FishQuery(models.Model):
    location = models.CharField(max_length=200)
    location_id = models.IntegerField()
    species = models.CharField(max_length=200)
    species_id = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        verbose_name_plural = "Fish Queries"

    @property
    def akfg_url(self):
        """
        Returns Alaska (AK) Fish & Game URL to look up fish count data
        using a POST request
        """
        akfg_url = "{base_url}&countLocationID={location_id}&speciesID={species_id}&year={year}".format(
            base_url=SALMON_COUNT_URL,
            location_id=self.location_id,
            species_id=self.species_id,
            year=self.year
            )
        return akfg_url

    def __str__(self):
        return "{location}-{species}-{year}".format(
            location=self.location,
            species=self.species,
            year=self.year
            )