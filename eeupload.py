import os
from datetime import datetime

import ee

ee.Initialize()


def upload(ee_dict: dict, skip_uploaded: bool = True):
    """
    Upload files to gee using earthengine util
    :param ee_dict: dictionary with upload data fields
    :param skip_uploaded: whether to skid uploaded files or not
    :return: full path of the uploaded file
    """

    fmt = '%Y-%m-%dT%H:%M:%S'
    bsn = os.path.basename(ee_dict["source"]).strip('.tif')
    ee_cmd = f'earthengine --no-use_cloud_api upload image {ee_dict["source"]} ' \
             f'--time_start {ee_dict["start_time"].strftime(fmt)} ' \
             f'--time_end {ee_dict["end_time"].strftime(fmt)} ' \
             f'--bands {ee_dict["var"]} ' \
             f'--nodata_value {ee_dict["missing_data"]} '

    ee_cmd = ''.join([ee_cmd] +
                     [f'--property {key}={val} '
                      for key, val in ee_dict["attributes"].items()] +
                     [f'--asset_id={ee_dict["asset_id"]}/{bsn} >> '
                      f'gee_uploads{datetime.today().strftime("%Y%m%d")}.txt'])

    if skip_uploaded:
        try:
            info = ee.Image(f'{ee_dict["asset_id"]}/{bsn}').getInfo()
            ext = 0
        except Exception as exc:
            print(f'EE\n{"=" * 5}\n{ee_cmd}\n')
            ext = os.system(ee_cmd)
    else:
        print(f'EE\n{"=" * 5}\n{ee_cmd}\n')
        ext = os.system(ee_cmd)
    return ext
