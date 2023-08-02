import urllib.request
from netCDF4 import Dataset
import numpy as np
from numpy import asarray
import PIL
import glob
import natsort

import xarray as xr
import rioxarray

from PIL import Image
PIL.Image.MAX_IMAGE_PIXELS = 933120000
import os
from pathlib import Path
import shutil

from joblib import Parallel, delayed
import time
import multiprocessing as mp

path = os.getcwd()+'/Sources/BHUVAN/'

def get_image_from_tile(BBOX,date_string):
    '''
    Downloads the image from the WMS tile and returns the path of downloaded image.
    Input parameters:
    BBOX: Bounding box coordinates(ln_w, lt_s, ln_e, lt_n)
    date_string: "yyyy_dd_mm_hh" hh is optional

    '''
    floods_url =  "https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms?LAYERS=flood%3Aas_"+date_string+"&TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image%2Fpng&SRS=EPSG%3A4326&BBOX="+BBOX+"&WIDTH=256&HEIGHT=256"

    #print(floods_url)
    try:
        urllib.request.urlretrieve(floods_url, path+r"/data/Tiles/"+date_string+"xx"+BBOX+".image")
        return None
    except:
        urllib.request.urlretrieve(floods_url, path+r"/data/Tiles/" + date_string + "xx" + BBOX + ".image")
        return print(floods_url) #r"Tiles/"+date_string+"xx"+BBOX+".image"


def merge_images(file1, file2, horizontal):
    """Merge two images into one
    Input parameters
    file1: path to first image file
    file2: path to second image file
    horizontal: True if the images are to be stitched horizontally

    returns the merged Image object
    """
    if type(file1) == PIL.Image.Image:
        image1 = file1
    else:
        image1 = Image.open(file1)
        # Removing BHUVAN watermark
        try:
            image1_ar = np.asarray(image1).copy()
            #image1_ar[:,:,3][(image1_ar[:,:,3]<255.0)] = 0
            image1_ar[:, :, :3][
                (image1_ar[:, :, 0] == image1_ar[:, :, 1]) & ((image1_ar[:, :, 1] == image1_ar[:, :, 2]))] = 255.0
            image1 = Image.fromarray(image1_ar)
        except:
            pass

    image2 = Image.open(file2)
    # Removing BHUVAN watermark
    try:
        image2_ar = np.asarray(image2).copy()
        #image2_ar[:,:,3][(image2_ar[:,:,3]<255.0)] = 0
        image2_ar[:, :, :3][
            (image2_ar[:, :, 0] == image2_ar[:, :, 1]) & ((image2_ar[:, :, 1] == image2_ar[:, :, 2]))] = 255.0
        image2 = Image.fromarray(image2_ar)
    except:
        pass

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    if horizontal == True:
        result_width = width1 + width2
        result_height = max(height1, height2)
        result = Image.new('L', (result_width, result_height))
        result.paste(im=image1, box=(0, 0))
        result.paste(im=image2, box=(width1, 0))
    else:
        result_height = height1 + height2
        result_width = max(width1, width2)
        result = Image.new('L', (result_width, result_height))
        result.paste(im=image1, box=(0, 0))
        result.paste(im=image2, box=(0, height1))

    # result.save('result.image')

    return result


def create_nc_from_images(lt_s, lt_n, ln_w, ln_e, image_path, image_name):
    '''
    Creates NetCDF4 files from the grayscale image using the BBOX coordinates.

    Input parameters:
    BBOX coordindates (lt_s, lt_n, ln_w, ln_e)
    image_path: filepath of the image to be converted.
    image_name: output file name

    Returns the filepath of the NetCDF4 file created.
    '''
    image = Image.open(image_path)
    grayscale_array = np.asarray(image)

    lt_array = np.linspace(lt_n, lt_s, grayscale_array.shape[0])
    ln_array = np.linspace(ln_w, ln_e, grayscale_array.shape[1])

    my_file = Dataset(path+r"/data/NCs/" + image_name + '.nc', 'w', format='NETCDF4')
    lat_dim = my_file.createDimension('lat', grayscale_array.shape[0])
    lon_dim = my_file.createDimension('lon', grayscale_array.shape[1])
    time_dim = my_file.createDimension('time', None)

    latitudes = my_file.createVariable("lat", 'f4', ('lat',))
    longitudes = my_file.createVariable("lon", 'f4', ('lon',))
    time = my_file.createVariable('time', np.float32, ('time',))

    new_nc_variable = my_file.createVariable("Inundation", np.uint8, ('time', 'lat', 'lon'))
    latitudes[:] = lt_array
    longitudes[:] = ln_array
    new_nc_variable[0, :, :] = grayscale_array

    my_file.close()

    return path+r"/data/NCs/" + image_name + '.nc'


def create_tiffs_from_ncs(nc_path, image_name):
    '''
    Creates GeoTIFF files from the NetCDF4 files.

    Input parameters:
    nc_path: filepath of the NetCDF4 file.
    image_name: Output name of the GeoTIFF
    '''

    nc_file = xr.open_dataset(nc_path)
    var = nc_file['Inundation']

    var = var.rio.set_spatial_dims('lon', 'lat')
    var.rio.set_crs("epsg:4326")
    var.rio.to_raster(path+r"/data/tiffs/" + image_name + r".tif")
    nc_file.close()


#date_strings = ['2023_16_18_06']
date_strings = ['2023_09_07_18', '2023_07_07_18', '2023_29_06_18', '2023_27_06_18', '2023_26_06_18', '2023_26_06_06', '2023_25_06_18', '2023_23_06_18', '2023_22_06_18', '2023_21_06_18', '2023_20_06_18', '2023_19_06_18', '2023_16_18_06', '2023_18_06', '2023_17_06', '2023_16_06']

delta = 0.0439453125

print(len(date_strings))

for date_string in date_strings:
    print("Date: ",date_string)
    starting_point_lat = 23.994140625
    lt_s = starting_point_lat
    starting_point_lon = 90 - 7 * delta
    ln_w = starting_point_lon
    BBOXs = []

    # Scraping the tile longitudinally first and then latitudinally.
    tic = time.perf_counter()
    no_images_vertically = 0
    while lt_s <= 28.125:
        lt_n = lt_s + delta

        no_images_horizontally = 0
        while ln_w <= 96:
            ln_e = ln_w + delta
            BBOX = "{},{},{},{}".format(ln_w, lt_s, ln_e, lt_n)
            ## Download the tile image
            BBOXs.append(BBOX)
            no_images_horizontally = no_images_horizontally + 1

            ln_w = ln_e

        if no_images_vertically == 0:
            print("Number of images horizontally: ", no_images_horizontally)

        lt_s = lt_n
        ln_w = starting_point_lon

        no_images_vertically = no_images_vertically + 1

    print("Number of vertical images: ", no_images_vertically)
    Parallel(n_jobs=mp.cpu_count())(delayed(get_image_from_tile)(BBOX, date_string) for BBOX in BBOXs)

    ## All tile images are downloaded -- these have to be stitched.
    # 144 tiles horizontally.
    toc = time.perf_counter()
    print("All tiles downloaded - Time Taken: {} seconds".format(toc - tic))

    extension = 'image'
    result = glob.glob(path+r'/data/Tiles/*.{}'.format(extension))

    lats = []
    lons = []
    
    for file in result:
        lats.append(float(file.split(',')[-1].split('.image')[0]))
        lons.append(float(file.split(',')[-2]))
    print(len(result))
    if len(result)!=13680:
        break
    result = sorted(result)

    tic = time.perf_counter()
    c = 0
    count = 1
    # We will first stitch images vertically (latitudinally) and then stitch them horizontally(longitudinally)
    # There are 95 images per a vertical stretch
    while c + no_images_vertically <= len(result):
        #print(count)
        vert_images = result[c:c + no_images_vertically]
        vert_images.reverse()
        #print(len(vert_images))
        merged_image = vert_images[0]
        for image in vert_images[1:]:
            merged_image = merge_images(merged_image, image, horizontal=False)
        c = c + no_images_vertically

        merged_image.save(path+r'/data/vert/' + str(count) + '.png')
        count = count + 1

    shutil.rmtree(path+'/data/Tiles')
    os.makedirs(path+'/data/Tiles')
    
    toc = time.perf_counter()
    print("Vertical Images created - Time Taken: {} seconds".format(toc - tic))

    #Stitch images horizontall
    tic = time.perf_counter()

    extension = 'png'
    vert_imgs = glob.glob(path+'/data/vert/*.{}'.format(extension))
    vert_imgs = natsort.natsorted(vert_imgs,reverse=False)

    merged_image = vert_imgs[0]
    #print(vert_imgs[0])
    for image in vert_imgs[1:]:
     #   print(image)
        merged_image = merge_images(merged_image, image,horizontal=True)
        
    toc = time.perf_counter()
    print("Horizontal stitch - Time Taken: {} seconds".format(toc-tic))
    
    tic = time.perf_counter()
    merged_image_ar = np.asarray(merged_image).copy()
    #merged_image_ar[:,:][(merged_image_ar[:,:]<255)] = 179
    merged_image_ar[:,:][(merged_image_ar[:,:]<255)] = 1
    merged_image_ar[:,:][(merged_image_ar[:,:]==255)] = 0
    merged_image = Image.fromarray(merged_image_ar)
    merged_image.save(path+r'/data/PNGs/'+date_string+'.png')
    shutil.rmtree(path+r'/data/'+'vert')
    os.makedirs(path+r'/data/'+'vert')
    toc = time.perf_counter()
    print("PNG save - Time Taken: {} seconds".format(toc-tic))
    
    tic = time.perf_counter()
    nc_path = create_nc_from_images(starting_point_lat, max(lats),
                                    starting_point_lon, max(lons),
                                    path+r'/data/PNGs/'+date_string+'.png',
                                    date_string)
    toc = time.perf_counter()
    print("NC save - Time Taken: {} seconds".format(toc-tic))
    
    tic = time.perf_counter()
    create_tiffs_from_ncs(nc_path, date_string)
    os.remove(nc_path)
    toc = time.perf_counter()
    print("Tiff save - Time Taken: {} seconds".format(toc-tic))
    
    print("--------------------")