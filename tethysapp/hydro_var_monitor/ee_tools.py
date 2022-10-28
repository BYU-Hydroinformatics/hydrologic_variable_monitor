import ee


def ERA5(band):
    ic = ee.ImageCollection(
        [f'users/rachelshaylahuber55/era5_monthly_avg/era5_monthly_{i:02}' for i in range(1, 13)]).select(band).reduce(
        ee.Reducer.mean())
    return ic


def GLDAS(band):
    ic = ee.ImageCollection(
        [f'users/rachelshaylahuber55/gldas_monthly/gldas_monthly_avg_{i:02}' for i in range(1, 13)]).select(band).reduce(
        ee.Reducer.mean())
    return ic


def IMERG(band):
    ic = ee.ImageCollection(
        [f'users/rachelshaylahuber55/imerg_monthly_avg/imerg_monthly_avg_{i:02}' for i in range(1, 13)]).select(band).reduce(
        ee.Reducer.mean())
    return ic


def CHIRPS(band):
    ic = ee.ImageCollection(
        [f'users/rachelshaylahuber55/chirps_monthly_avg/chirps_monthly_avg_{i:02}' for i in range(1, 13)]).select(band).reduce(
        ee.Reducer.mean())
    return ic


def get_tile_url(ee_image, vis_params):
    map_id_dict = ee.Image(ee_image).getMapId(vis_params)
    return map_id_dict['tile_fetcher'].url_format