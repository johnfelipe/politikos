from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from geopy.geocoders import Nominatim
from pci import Mapit, Popit
import tortilla


class RepresentativesSearchView(TemplateView):
    template_name = 'explorer.html'

    def post(self, request, *args, **kwargs):
        address = self.request.POST.get('search', None)

        if address:
            kwargs['search'] = address

            # for some reason, Nominatim responds 403 to this requests
            # geolocator = Nominatim()
            # location = geolocator.geocode(address)

            nominatim = tortilla.wrap('http://nominatim.openstreetmap.org')
            try:
                location = nominatim.search.get(
                    address, params={'format': 'json'}
                )[0]
            except IndexError:
                messages.warning(request, 'Location could not be found, try another one.')
                return HttpResponseRedirect('/')


            kwargs['location'] = location
            kwargs['areas'] = []
            if location:

                endpoint = settings.MAPIT_ENDPOINT
                mapit = Mapit(base_endpoint=endpoint)
                popit = Popit(instance=settings.POPIT_INSTANCE)

                kwargs['area_representatives'] = []

                for mapit_id, mapit_data in mapit.areas(point='{0},{1}'.format(location.lon, location.lat),srid='4326').get().items():
                    kwargs['areas'].append(
                        (mapit_id, mapit_data)
                    )
                    area_uri = endpoint + 'area/' + str(mapit_id)
                    area_representatives = popit.search.memberships.get(params={
                        'q': 'area.identifier:"%s"' % area_uri
                    })
                    if area_representatives['total'] > 0:
                        kwargs['area_representatives'].append(
                            (area_representatives['result'][0]['organization'], mapit_data, area_representatives['result'])
                        )

        return super(RepresentativesSearchView, self).get(request, *args, **kwargs)


class PersonDetail(TemplateView):
    template_name = 'person-detail.html'

    def get(self, request, *args, **kwargs):
        person_id = kwargs.pop('id')
        popit = Popit(instance=settings.POPIT_INSTANCE)
        return super(PersonDetail, self).get(request, person=popit.persons.get(person_id, params={'embed': 'membership.organization'})['result'], *args, **kwargs)


class InstitutionDetail(TemplateView):
    template_name = 'institution-detail.html'
    
    def get(self, request, *args, **kwargs):
        institution_id = kwargs.pop('id')
        popit = Popit(instance=settings.POPIT_INSTANCE)
        return super(InstitutionDetail, self).get(request, institution=popit.organizations.get(institution_id, params={'embed': 'membership.person'})['result'])