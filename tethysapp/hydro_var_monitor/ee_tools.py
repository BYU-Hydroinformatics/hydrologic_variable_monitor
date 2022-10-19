import ee


def ERA5(band):
    ic = ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY").filterDate('1983-01-01', '2023-01-01').select(band).reduce(
        ee.Reducer.mean())
    return ic


def GLDAS(band):
    ic = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H").filterDate('2022-01-01', '2023-01-01').select(band).reduce(
        ee.Reducer.mean())
    return ic


def IMERG(band):
    ic = ee.ImageCollection("NASA/GPM_L3/IMERG_V06").filterDate('2022-07-01', '2023-01-01').select(band).reduce(
        ee.Reducer.mean())
    return ic


def CHIRPS(band):
    ic = ee.ImageCollection("UCSB-CHG/CHIRPS/PENTAD").filterDate('2022-01-01', '2023-01-01').select(band).reduce(
        ee.Reducer.mean())
    return ic


def get_tile_url(ee_image, vis_params):
    map_id_dict = ee.Image(ee_image).getMapId(vis_params)
    return map_id_dict['tile_fetcher'].url_format