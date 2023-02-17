import zipfile
import tempfile
import json
import os
import glob
from zipfile import ZipFile
import shutil

import pandas as pd
import datetime
from django.http import JsonResponse
from .app import HydroVarMonitor as App



def unzip_and_read_files(request):
    print("Checking")
    # extract the file from the request object and save it to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        for chunk in request.FILES['exact-json'].chunks():
            f.write(chunk)

    # extract the contents of the ZIP file to the './json-files/' directory
    with zipfile.ZipFile(f.name, 'r') as zip_ref:
        zip_ref.extractall('./json-files/')
    print("Extracted")
    # process each JSON file in the './json-files/' directory
    for filename in os.listdir('./json-files/'):
        if filename.endswith('.json'):
            with open(f'./json-files/{filename}') as json_file:
                json_data = json.load(json_file)
                print(json_data)
    print ("SUCCESS")

    # delete the temporary file
    os.unlink(f.name)
    return


def list_uploaded_observations():
    workspace_path = App.get_app_workspace().path
    uploaded_observations = glob.glob(os.path.join(workspace_path, 'observations', '*.csv'))
    list_of_observations = []
    for uploaded_observation in uploaded_observations:
        file_name = os.path.basename(uploaded_observation)
        presentation_name = file_name.replace('_', ' ').replace('.csv', '')
        list_of_observations.append((presentation_name, file_name))
    return tuple(sorted(list_of_observations))


def upload_new_observations(request):
    workspace_path = App.get_app_workspace().path
    files = request.FILES
    for file in files:
        new_observation_path = os.path.join(workspace_path, 'observations', files[file].name)
        with open(new_observation_path, 'wb') as dst:
            for chunk in files[file].chunks():
                dst.write(chunk)
        try:
            df = pd.read_csv(new_observation_path, index_col=0)
            df.dropna(inplace=True)
        except Exception as e:
            JsonResponse(dict(error='Cannot read the csv provided. It may not be a valid csv file.'))
        df.to_csv(new_observation_path)

    return JsonResponse(dict(new_file_list=list_uploaded_observations()))


def get_project_directory(project):
    workspace_path = App.get_app_workspace().path
    project = str(project).replace(' ', '_')
    return os.path.join(workspace_path, 'projects', project)


def geoprocess_zip_shapefiles(request):
    project = request.GET.get('project', False)
    proj_dir = get_project_directory(project)

    catchment_zip = os.path.join(proj_dir, 'catchment_shapefile.zip')
    drainageline_zip = os.path.join(proj_dir, 'drainageline_shapefile.zip')
    project = str.lower(project)
    try:
        with ZipFile(catchment_zip, 'w') as zipped:
            for component in glob.glob(os.path.join(proj_dir, 'catchment_shapefile', project + '_catchments.*')):
                zipped.write(component, arcname=os.path.basename(component))
        shutil.rmtree(os.path.join(proj_dir, 'catchment_shapefile'))

        with ZipFile(drainageline_zip, 'w') as zipped:
            for component in glob.glob(os.path.join(proj_dir, 'drainageline_shapefile', project + '_drainagelines.*')):
                zipped.write(component, arcname=os.path.basename(component))
            shutil.rmtree(os.path.join(proj_dir, 'drainageline_shapefile'))

        return JsonResponse({'status': 'success'})

    except FileNotFoundError as e:
        if os.path.isdir(os.path.join(proj_dir, 'drainageline_shapefile')):
            shutil.rmtree(os.path.join(proj_dir, 'drainageline_shapefile'))
        if os.path.isdir(os.path.join(proj_dir, 'catchment_shapefile')):
            shutil.rmtree(os.path.join(proj_dir, 'catchment_shapefile'))
        if os.path.exists(catchment_zip):
            os.remove(catchment_zip)
        if os.path.exists(drainageline_zip):
            os.remove(drainageline_zip)
        raise e

    except Exception as e:
        raise e
