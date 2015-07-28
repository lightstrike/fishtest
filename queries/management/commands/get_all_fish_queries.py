import requests
from lxml import etree

from django.core.management.base import BaseCommand
from queries.models import FishQuery

# Disabling warnings related to ADFG's SSL cert
# See https://github.com/shazow/urllib3/issues/497
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


FISH_URL_BASE = 'https://www.adfg.alaska.gov/sf/FishCounts/index.cfm?ADFG='
FISH_COUNT_URL = FISH_URL_BASE + 'main.displayResults'
FISH_LOCATIONS_URL = FISH_URL_BASE + 'main.home'
FISH_OPTIONS_URL = FISH_URL_BASE + 'main.LocSelectYearSpecies'


class Command(BaseCommand):
    help = 'Crawls the Alaska Fish & Game website to find & save all unique fish count queries'

    def build_lxml_tree(self, request_content):
        parser = etree.HTMLParser(recover=True)
        return etree.fromstring(request_content, parser)

    def build_options_list(self, options_html):
        return [(o.get('value').strip(), o.text) for o in options_html if o.get('value') != '']

    def get_fish_locations(self):
        request = requests.get(FISH_LOCATIONS_URL)
        tree = self.build_lxml_tree(request.content)
        locations = tree.xpath('//select[@name="countLocationID"]/option')
        location_ids = self.build_options_list(locations)
        return location_ids

    def get_location_queries(self, location_id, location):
        location_queries = []
        request = requests.post(FISH_OPTIONS_URL,
                data={'countLocationID': location_id})
        tree = self.build_lxml_tree(request.content)
        species = tree.xpath('//select[@name="speciesID"]/option')
        species_ids = self.build_options_list(species)
        years = tree.xpath('//select[@name="year"]/option')
        year_ids = self.build_options_list(years)
        for fish_id, fish_name in species_ids:
            for year in year_ids:
                fish_query = {
                    'location': location,
                    'location_id': location_id,
                    'species_id': fish_id,
                    'species': fish_name,
                    'year': year[0],
                    }
                location_queries.append(fish_query)
        self.stdout.write("Found all fish queries for {location}".format(location=location))
        return location_queries

    def get_all_fish_queries(self):
        fish_queries = []
        locations = self.get_fish_locations()
        for location_id, location in locations:
            location_queries = self.get_location_queries(location_id, location)
            fish_queries.extend(location_queries)
        return fish_queries

    def handle(self, *args, **options):
        fish_queries = self.get_all_fish_queries()
        created_counter = 0
        for query in fish_queries:
            saved_query, created = FishQuery.objects.get_or_create(**query)
            if created:
                created_counter += 1
        total_queries = FishQuery.objects.all().count()
        command_message = "{counter} new queries created, {total} total saved queries".format(
            counter=created_counter,
            total=total_queries
            )
        self.stdout.write(command_message)
