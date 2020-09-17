import os
from .filerm import rm_file

def translate(src_file: str, trg_file: str, srs, fill_value: float, rm_src: bool = True):
    """
    The gdal_translate utility can be used to convert raster data between different formats,
    potentially performing some operations like subsettings, resampling, and rescaling pixels
    in the process.

    :param src_file: source tif file to perform the operation
    :param trg_file: source output tif file to save on
    :param srs: Spatial Reference System. Override the projection for the output file.
                The<srs_def> may be any of the usual GDAL/OGR forms, complete WKT, PROJ.4,
                EPSG:n or a file containing the WKT. No reprojection is done.
    :param fill_value: mask value for empty pixels
    :param rm_src: whether to delete the source file or not
    :return: system exit
    """

    cmd = f'gdal_translate -a_nodata {fill_value} -a_srs {srs} {src_file} {trg_file}'
    ext = os.system(cmd)
    if rm_src:
        rm_file(file=rm_src)
    return ext
