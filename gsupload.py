import os
import time

from .filerm import rm_file


def upload(file: str, bucket: str, skip_uploaded: bool = True):
    """
    Upload files to gc using gsutil
    :param file: file to upload
    :param bucket: bucket where to upload
    :param skip_uploaded: whether to skid uploaded files or not
    :return: full path of the uploaded file
    """

    basename = os.path.basename(file)
    gc_file = f'{bucket}/{basename}'
    ext = 0

    if skip_uploaded is True:
        gs_cmd = f'gsutil cp {file} {gc_file}'
    else:
        gs_cmd = f'gsutil -m cp -n {file} {gc_file}'
    n = len(gs_cmd)
    print(f'\tGSUTIL\n{gs_cmd}\n{"=" * n}')
    ext = os.system(gs_cmd)
    return gc_file, ext
