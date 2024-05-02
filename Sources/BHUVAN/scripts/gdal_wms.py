import os
import subprocess
import timeit

from osgeo import gdal

gdal.DontUseExceptions()

path = os.getcwd() + "/Sources/BHUVAN/"

date_strings = ["cuml_2021"]  # Sample date for assam - "2023_07_07_18"

# Specify the state information to scrape data for.
state_info = {"state": "Himachal Pradesh", "code": "hp"}


for dates in date_strings:

    # Define your input and output paths
    input_xml_path = path + f"{state_info['state']}/data/inundation.xml"
    output_tiff_path = path + f"{state_info['state']}/data/tiffs/{dates}.tif"

    layer_hp = "fld_cuml_2021_hp"
    layer_assam = "flood%3Aas_2023_07_07_18"
    state_code = "hp"  # fld_cuml_2021_hp #flood%3Aas_2023_07_07_18
    url_hp = "https://bhuvan-ras2.nrsc.gov.in/mapcache"
    url_as = "https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms"

    # Download the WMS(Web Map Sevice) layer and save as XML.
    command = [
        "gdal_translate",
        "-of",
        "WMS",
        f"WMS:{url_hp}?&LAYERS={layer_hp}&TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image%2Fpng&SRS=EPSG%3A4326&BBOX=89.6922970,23.990548,96.0205936,28.1690311",
        f"{path}{state_info['state']}/data/inundation.xml",
    ]
    subprocess.run(command)

    # Specify the target resolution in the X and Y directions
    target_resolution_x = 0.0001716660336923202072
    target_resolution_y = -0.0001716684356881450775

    # Perform the warp operation using gdal.Warp()
    print("Warping Started")
    starttime = timeit.default_timer()

    gdal.Warp(
        output_tiff_path,
        input_xml_path,
        format="GTiff",
        xRes=0.0001716660336923202072,
        yRes=-0.0001716684356881450775,
        creationOptions=["COMPRESS=DEFLATE", "TILED=YES"],
        callback=gdal.TermProgress,
    )

    print("Time took to Warp: ", timeit.default_timer() - starttime)
    print(f"Warping completed. Output saved to: {output_tiff_path}")
