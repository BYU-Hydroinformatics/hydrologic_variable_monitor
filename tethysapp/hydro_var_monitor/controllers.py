from django.http.response import JsonResponse
from django.shortcuts import render
from tethys_sdk.routing import controller
import json

import ee

from .app import HydroVarMonitor as app
import ee_tools


try:
    import collections
    collections.Callable = collections.abc.Callable
    ee.Initialize(ee.ServiceAccountCredentials(None, app.get_custom_setting('ee_auth_token_path')))
    EE_IS_AUTHORIZED = True
except Exception as e:
    EE_IS_AUTHORIZED = False


@controller(name='home', url='/', login_required=True)
def ctrl_home(request):
    if not EE_IS_AUTHORIZED:
        return render(request, 'hydro_var_monitor/no_auth_error.html')
    ee_sources = {
        'air_temp': ['GLDAS', 'ERA5'],
        'ndvi': ['Landsat', ],
        'precip': ['GLDAS', 'CHIRPS', 'IMERG', 'ERA5'],
        'soil_moisture': ['GLDAS', ],
        'soil_temp': ['ERA5', ]
    }
    context = {
        'sources': json.dumps(ee_sources)
    }
    return render(request, 'hydro_var_monitor/home.html', context, status=200)


@controller(name='get-map-id', url='/ee/get-map-id', login_required=True)
def ctrl_get_map_id(request):
    if not EE_IS_AUTHORIZED:
        return JsonResponse({'error': 'Earth Engine is not authorized'}, status=500)
    args = json.loads(request.body.decode())
    ee_tools.get_map_id(variable=args.variable, source=args.source)
    return JsonResponse({'url': ''}, status=200)


@controller(name='get-plot', url='/ee/get-plot', login_required=True)
def ctrl_get_plot(request):
    if not EE_IS_AUTHORIZED:
        return JsonResponse({'error': 'Earth Engine is not authorized'}, status=500)
    args = json.loads(request.body.decode())
    return JsonResponse({'plot': ''}, status=200)
