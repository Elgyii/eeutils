import json


def write(asset_dict: dict, disp: bool = False):
    """
    Writes earth engine manifest file for data upload 
    :param asset_dict: dictionary with data to write
    :param disp: whether to print the dictionary 
    :return: manifest file name
    """
    # The enclosing object for the asset.
    asset = {
        'name': asset_dict['asset_id'],
        'tilesets': [
            {'sources': [
                {"uris": [asset_dict['source']]}]}],
        'bands': [
            {'id': asset_dict['var'],
             'missing_data': {'values': [int(asset_dict['missing_data'])]}}],
        "start_time": {"seconds": asset_dict['start_time']},
        "end_time": {"seconds": asset_dict['end_time']},
        "properties": asset_dict['attributes']
    }
    if disp:
        print(json.dumps(asset, indent=2))

    json_manifest = 'temp_manifest.json'
    with open(json_manifest, 'w') as f:
        json.dump(asset, f, indent=2)
    return json_manifest
