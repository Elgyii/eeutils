import os
from .filerm import rm_file

def create(asset_id: str):
    """
    Create EE Asset if is not created already
    :param asset_id: Asset ID
    :return: system exit 
    """
    tmp_file = 'ee_asset.txt'
    os.system(f'earthengine --no-use_cloud_api ls -m 1 {asset_id} > {tmp_file}')
    with open(tmp_file, 'r') as txt:
        res = ''.join([line.strip('\n') for line in txt.readlines()])
    # rm_file(file=tmp_file)

    ext = 0
    if ('not found.' in res) or ('No such folder or collection:' in res):
        ee_cmd = f'earthengine --no-use_cloud_api create collection -p {asset_id}'
        print(f'CreateAsset\n{ee_cmd}')
        ext = os.system(ee_cmd)
    return ext