import json

from django.views.generic.edit import FormView
from django.http.response import HttpResponseBadRequest, HttpResponse

from forms import GeoForm
from helpers import GeoCalculation, Price


class GeoView(FormView):
    template_name = 'welcome.html'
    form_class = GeoForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        data = form.cleaned_data

        geo = GeoCalculation()
        coordinates = geo.get_coordinates(data)
        for key, value in coordinates.iteritems():
            if value is None:
                if key.startswith('start'):
                    return HttpResponseBadRequest(
                        'origin address cannot be found')
                else:
                    return HttpResponseBadRequest(
                        'destination address cannot be found')

        result = Price(coordinates).create_result()
        result = json.dumps(result, indent=4)

        return HttpResponse('Your offer is:\n\n' + result,
                            content_type="application/json")
