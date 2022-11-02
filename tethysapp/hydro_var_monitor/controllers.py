from django.http.response import JsonResponse
from datetime import date
from datetime import datetime
from django.shortcuts import render
from tethys_sdk.permissions import login_required
from .ee_auth import *
import json
from django.http import JsonResponse, HttpResponseNotAllowed
from tethys_sdk.workspaces import app_workspace
from . import ee_auth
import logging
import os
from .ee_tools import ERA5, get_tile_url, GLDAS, CHIRPS, IMERG, GLDAS_evapo
from .plots import plot_ERA5, plot_GLDAS, plot_IMERG, plot_CHIRPS
from .compare import air_temp_compare, precip_compare


# @controller(name='home', url='/', login_required=
# @login_required()
def home(request):
    if not EE_IS_AUTHORIZED:
        return render(request, 'hydro_var_monitor/no_auth_error.html')
    ee_sources = {
        'air_temp': ['GLDAS', 'ERA5'],
        'precip': ['GLDAS', 'CHIRPS', 'IMERG', 'ERA5'],
        'soil_moisture': ['GLDAS', ],
        'evapo': ['GLDAS']
    }
    context = {
        'sources': json.dumps(ee_sources)
    }
    return render(request, 'hydro_var_monitor/home.html', context)


def compare(request):
    response_data = {'success': False}
    try:
        region = request.GET.get('region', None)
        definedRegion = request.GET.get('definedRegion', None)
        if definedRegion == "true":
            province = region + ".json"
            ROOT_DIR = os.path.abspath(os.curdir)
            json_url = os.path.join(ROOT_DIR, "hydrologic_variable_monitor", "tethysapp", "hydro_var_monitor",
                                    "workspaces",
                                    "app_workspace", "preconfigured_geojsons", "ecuador", province)
            f = open(json_url)
            region = json.load(f)

        var = request.GET.get('variable', None)
        isPoint = request.GET.get('isPoint', None)

        if var == "air_temp":
            if definedRegion == "true":
                values = air_temp_compare(region, json.loads(isPoint))
            else:
                values = air_temp_compare(json.loads(region), json.loads(isPoint))

        if var == "precip":
            if definedRegion == "true":
                values = precip_compare(region, json.loads(isPoint))
            else:
                values = precip_compare(json.loads(region), json.loads(isPoint))

        response_data.update({
            'success': True,
        })

    except Exception as e:
        response_data['error'] = f'Error Processing Request: {e}'

    return JsonResponse(json.loads(json.dumps(values)))


# @controller(name='get-map-id', url='/ee/get-map-id', login_required=True)
def get_map_id(request):
    response_data = {'success': False}

    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        sensor = request.GET.get('source', None)
        var = request.GET.get('variable', None)

        if sensor == "ERA5":
            if var == "air_temp":
                band = "temperature_2m"
                vis_params = {"min": 250, "max": 300,
                              "palette": ['009392', '72aaa1', 'b1c7b3', 'f1eac8', 'e5b9ad', 'd98994', 'd0587e']}
            if var == "precip":
                band = "total_precipitation"
                vis_params = {"min": 0, "max": 0.008, "palette": ['00FFFF', '0000FF']}
            if var == "soil_temperature":
                band = "skin_temperature"
                vis_params = {"min": 250, "max": 300,
                              "palette": ['009392', '72aaa1', 'b1c7b3', 'f1eac8', 'e5b9ad', 'd98994', 'd0587e']}

            imgs = ERA5(band)

        if sensor == "GLDAS":
            if var == "precip":
                band = "Rainf_tavg"
                vis_params = {"min": 0, "max": 0.00006, "palette": ['00FFFF', '0000FF']}
                imgs = GLDAS(band)
            if var == "air_temp":
                band = "Tair_f_inst"
                vis_params = {"min": 235, "max": 320,
                              "palette": ['009392', '72aaa1', 'b1c7b3', 'f1eac8', 'e5b9ad', 'd98994', 'd0587e']}
                imgs = GLDAS(band)
            if var == "soil_moisture":
                band = "RootMoist_inst"
                vis_params = {"min": 100, "max": 400}
                imgs = GLDAS(band)
            if var == "evapo":
                band = "Evap_tavg"
                vis_params = {"min":0, "max":0.00005}
                imgs = GLDAS_evapo(band)

        if sensor == "IMERG":
            band = "HQprecipitation"
            vis_params = {"min": 0, "max": 0.4, "palette": ['00FFFF', '0000FF']}
            imgs = IMERG(band)

        if sensor == "CHIRPS":
            band = "precipitation"
            vis_params = {"min": 0, "max": 40, "palette": ['00FFFF', '0000FF']}
            imgs = CHIRPS(band)

        # get the url from specified image and then return it in json
        wurl = get_tile_url(imgs, vis_params)
        response_data.update({
            'success': True,
            'water_url': wurl,
        })

    except Exception as e:
        response_data['error'] = f'Error Processing Request: {e}'

    return JsonResponse(response_data)


def get_date():
    now = date.today().strftime("%Y-%m-%d")
    y2d_start = date(date.today().year, 1, 1).strftime("%Y-%m-%d")
    return now, y2d_start


# @controller(name='get-plot', url='/ee/get-plot', login_required=True)
def get_plot(request):
    response_data = {'success': False}

    try:
        sensor = request.GET.get('source', None)
        var = request.GET.get('variable', None)
        region = request.GET.get('region', None)
        isPoint = request.GET.get('isPoint', None)
        year = request.GET.get('year', None)

        if year == "" or year == "2022" or year == "y2d":
            endDate, startDate = get_date()
        elif year == "last12":
            endDate = date.today().strftime("%Y-%m-%d")
            startDate = "last12"
        else:
            startDate = datetime(int(year), 1, 1).strftime("%Y-%m-%d")
            endDate = datetime(int(year), 12, 31).strftime("%Y-%m-%d")

        if sensor == "ERA5":
            if var == "air_temp":
                band = "temperature_2m"
                title = "Temperatura del Aire - ERA5"
                yaxis = "Temperature en Celsius"
            if var == "precip":
                band = "total_precipitation"
                title = "Acumulados de Precipitación - ERA5"
                yaxis = "mm of precipitación"
            if var == "soil_temperature":
                band = "skin_temperature"
                title = "Temperatura del Suelo- ERA5"
                yaxis = "Temperatura en Celsius"
            plot_data = plot_ERA5(json.loads(region), band, title, yaxis, json.loads(isPoint), startDate, endDate)

        if sensor == "GLDAS":
            if var == "precip":
                band = "Rainf_tavg"
                title = "Acumulados de Precipitación- GLDAS"
                yaxis = "mm of precipitación"
            if var == "air_temp":
                band = "Tair_f_inst"
                title = "Temperatura del Aire- GLDAS"
                yaxis = "Temperatura en Celsius"
            if var == "soil_moisture":
                band = "RootMoist_inst"
                title = "Humedad del Suelo - GLDAS (root zone)"
                yaxis = "kg/m^2"
            if var == "evapo":
                band = "Evap_tavg"
                title = "Evapotranspiración- GLDAS"
                yaxis = "Evapotranspiración en kg/M^2/s"
            plot_data = plot_GLDAS(json.loads(region), band, title, yaxis, json.loads(isPoint), startDate, endDate)

        if sensor == "IMERG":
            plot_data = plot_IMERG(json.loads(region), json.loads(isPoint), startDate, endDate)

        if sensor == "CHIRPS":
            plot_data = plot_CHIRPS(json.loads(region), json.loads(isPoint), startDate, endDate)

        response_data.update({
            'success': True,
        })

    except Exception as e:
        response_data['error'] = f'Error Processing Request: {e}'
    return JsonResponse(json.loads(json.dumps(plot_data)))


def compare_precip(request):
    response_data = {'success': False}

    try:
        region = request.GET.get('region', None)
        isPoint = request.GET.get('isPoint', None)
        plot_data = compare_precip_moist(json.loads(region), isPoint)

        response_data.update({
            'success': True,
        })

    except Exception as e:
        response_data['error'] = f'Error Processing Request: {e}'
    return JsonResponse(json.loads(json.dumps(plot_data)))


def get_predefined(request):
    # read in values to variables
    name_of_area = request.GET.get("region", None)
    isPoint = request.GET.get('isPoint', None)
    sensor = request.GET.get('source', None)
    var = request.GET.get('variable', None)
    year = request.GET.get('year', None)
    # get json simplified version from app workspace for earth engine
    province = name_of_area + ".json"
    ROOT_DIR = os.path.abspath(os.curdir)
    json_url = os.path.join(ROOT_DIR, "hydrologic_variable_monitor", "tethysapp", "hydro_var_monitor", "workspaces",
                            "app_workspace", "preconfigured_geojsons", "ecuador", province)
    f = open(json_url)
    region = json.load(f)

    if year == "" or year == "y2d":
        endDate, startDate = get_date()
    elif year == "last12":
        endDate = date.today().strftime("%Y-%m-%d")
        startDate = "last12"
    else:
        startDate = datetime(int(year), 1, 1).strftime("%Y-%m-%d")
        endDate = datetime(int(year), 12, 31).strftime("%Y-%m-%d")

    if sensor == "ERA5":
        if var == "air_temp":
            band = "temperature_2m"
            title = "Temperatura del Aire - ERA5"
            yaxis = "Temperature en Celsius"
        if var == "precip":
            band = "total_precipitation"
            title = "Acumulados de Precipitación - ERA5"
            yaxis = "mm of precipitación"
        if var == "soil_temperature":
            band = "skin_temperature"
            title = "Temperatura del Suelo- ERA5"
            yaxis = "Temperatura en Celsius"
        plot_data = plot_ERA5(region, band, title, yaxis, json.loads(isPoint), startDate, endDate)

    if sensor == "GLDAS":
        if var == "precip":
            band = "Rainf_tavg"
            title = "Acumulados de Precipitación- GLDAS"
            yaxis = "mm of precipitación"
        if var == "air_temp":
            band = "Tair_f_inst"
            title = "Temperatura del Aire- GLDAS"
            yaxis = "Temperatura en Celsius"
        if var == "soil_moisture":
            band = "RootMoist_inst"
            title = "Humedad del Suelo - GLDAS (root zone)"
            yaxis = "kg/m^2"
        if var == "evapo":
            band = "Evap_tavg"
            title = "Evapotranspiración- GLDAS"
            yaxis = "Evapotranspiración en kg/M^2/s"
        plot_data = plot_GLDAS(region, band, title, yaxis, json.loads(isPoint), startDate, endDate)

    if sensor == "IMERG":
        plot_data = plot_IMERG(region, json.loads(isPoint), startDate, endDate)

    if sensor == "CHIRPS":
        plot_data = plot_CHIRPS(region, json.loads(isPoint), startDate, endDate)

    return JsonResponse(json.loads(json.dumps(plot_data)))
