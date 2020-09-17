import logging
import os

import ee
import logger_config

from .filerm import rm_file

ee.Initialize()

file = f'{os.path.dirname(__file__)}'
logger = logger_config.logger(log=logging.getLogger(__name__), log_name=file)


def gsee_rm(asset_id: str, bucket: str):
    """
    Removes GC files that have been uploaded to the EE Asset
    :param asset_id: EE Asset ID
    :param bucket: GC bucket where files are stored
    :return: list of removed files
    """
    gs_file = 'gs_files.txt'
    gs_cmd = f'gsutil ls {bucket}/*.tif > {gs_file}'
    os.system(gs_cmd)
    rm_files = []
    append = rm_files.append

    with open(gs_file, 'r') as txt:
        for line in txt.readlines():
            bsn = os.path.basename(line.strip('.tif\n'))
            try:
                info = ee.Image(f'{asset_id}/{bsn}').getInfo()
            except Exception as exc:
                logger.exception(f'{bsn} not in {asset_id}\n', exc_info=exc)
                continue
            os.system(f'gsutil rm {bucket}/{bsn}.tif')
            append(line.strip('\n'))
    ext = rm_file(file=gs_file)
    return rm_files
