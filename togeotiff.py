import pyproj
from osgeo import gdal, gdal_array, osr
from pyresample import geometry


def toGeotiff(output_file:str, data, proj_id: str, extent: list, fill_value):
    """
    Creates geotif file
    :param output_file: filename for the output geotif
    :param data: data to write into the geotif
    :param proj_id: projection ID of the data
    :param extent: area extent of the data
    :param fill_value: missing value fill
    :return: geotif filename and SRS
    """
    print(output_file)
    datum = 'WGS84'
    if proj_id == 'sinu':
        a = 6378.137
        g = pyproj.Geod(a=a)
    else:
        g = pyproj.Geod(ellps=datum)
    area_id = proj_id
    proj_id = proj_id
    lat_0, lon_0 = 0, 0

    proj = dict(proj=proj_id, lat_0=lat_0, lon_0=lon_0, a=g.a, b=g.b, units='m')
    prj = pyproj.Proj(proj)

    adef = geometry.AreaDefinition.from_extent(
        area_id=area_id, projection=proj,
        shape=data.shape, area_extent=extent)

    # -----------------------
    # create and set output projection
    # -----------------------
    srs = osr.SpatialReference()
    srs.ImportFromProj4(prj.srs)
    srs.SetProjCS(proj_id)
    srs = srs.ExportToWkt()

    data[data.mask] = fill_value

    # -----------------------
    # define and set output geotransform
    # -----------------------
    sgt = [adef.area_extent[0], adef.pixel_size_x, 0,
           adef.area_extent[3], 0, -adef.pixel_size_y]

    # -----------------------
    # begin to create geotiff
    # -----------------------
    driver = gdal.GetDriverByName('GTiff')                              # Select GDAL GeoTIFF driver
    dtype = gdal_array.NumericTypeCodeToGDALTypeCode(data.dtype)        # Define output data type
    height, width = data.shape                                          # Define rows/cols from array size
    dst = driver.Create(output_file, width, height, 1, dtype)           # Specify parameters of the GeoTIFF

    band = dst.GetRasterBand(1)                                         # Get band 1
    band.WriteArray(data)                                               # Write data array to band 1
    band.FlushCache()                                                   # Export data
    band.SetNoDataValue(float(fill_value))                              # Set fill value
    dst.SetGeoTransform(sgt)                                            # Set Geotransform
    dst.SetProjection(srs)                                              # Set projection

    dst = None                                                          # Close file
    print('Processing: {}'.format(output_file))                         # Print the progress
    return sgt, srs
