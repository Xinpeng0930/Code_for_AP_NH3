
# import necessary packages
import math
import geopandas as gpd
from shapely.geometry import mapping
from osgeo import gdal,osr,ogr # gdal package used to process rasters
from collections import Counter
import numpy as np
import matplotlib as mpl #plot package
from matplotlib.colors import ListedColormap
mpl.use('TkAgg')  # !IMPORTANT to fix plt bug
import matplotlib.pyplot as plt #plt visualization function
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader #read shapefile properties
import glob #read file names in a directory
import rasterio #procdess rasters
from rasterstats import zonal_stats  #(conduct zonal statistic)
from rasterio.mask import mask
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.features import rasterize
from rasterio.merge import merge
from rasterio.plot import show
from rasterio.transform import from_origin
from scipy.interpolate import griddata
import pandas as pd
from copy import deepcopy
import glob
import os
import xarray as xr
import pickle

#%%
# define necessary functions
def output_ras(outpath,exampath,CRS,input_array):
    '''
    :param outpath: the outpath of newly calculated map
    :param exampath: the inputpath of referred map
    :param input_array: newly calculated array
    :return:
    '''
    with rasterio.open(exampath) as src:  # (obtain a referred coordinate system from a certain former well-orgnized tif file)
        # transform for input raster
        src_transform = src.transform  # (get the coordinate system of the source data)

        # calculate the transform matrix for the output
        dst_transform, width, height = calculate_default_transform(
            src.crs,  # source CRS
            src.crs,  # destination CRS is equel to source CRS because of no transform
            src.width,  # column count
            src.height,  # row count
            *src.bounds,  # unpacks outer boundaries (left, bottom, right, top)
        )
    with rasterio.open(
            outpath,
            mode="w",  # writing mode
            driver="GTiff",  # format is geotif
            height=src.shape[0],  # height of the map
            width=src.shape[1],  # width of the map
            count=1,  # a count of the dataset bands
            dtype=input_array.dtype,  # data type of the value
            crs=CRS,
            # also called the equidistant cylindrical projection, which is widely used to plot global maps
            transform=dst_transform,  # execute the affine transformation
    ) as new_dataset:
        new_dataset.write(input_array, 1)
    return

def output_ras_filtered (outpath,exampath,CRS,input_array):
    '''
     Save a newly calculated map as a GeoTIFF file, filtering out invalid data based on a reference map.
    :param outpath: the outpath of newly calculated map
    :param exampath: the inputpath of referred map
    :param input_array: newly calculated array
    :return:
    '''
    with rasterio.open(exampath) as src:  # (obtain a referred coordinate system from a certain former well-orgnized tif file)
        # transform for input raster
        src_transform = src.transform  # (get the coordinate system of the source data)

        # calculate the transform matrix for the output
        dst_transform, width, height = calculate_default_transform(
            src.crs,  # source CRS
            src.crs,  # destination CRS is equel to source CRS because of no transform
            src.width,  # column count
            src.height,  # row count
            *src.bounds,  # unpacks outer boundaries (left, bottom, right, top)
        )
    Data_example = rasterio.open(exampath).read(1)
    input_filtered = np.where ((Data_example == -999),-999,input_array)
    with rasterio.open(
            outpath,
            mode="w",  # writing mode
            driver="GTiff",  # format is geotif
            height=src.shape[0],  # height of the map
            width=src.shape[1],  # width of the map
            count=1,  # a count of the dataset bands
            dtype=input_array.dtype,  # data type of the value
            crs=CRS,
            # also called the equidistant cylindrical projection, which is widely used to plot global maps
            transform=dst_transform,  # execute the affine transformation
            nodata=-999  # set NoData value
    ) as new_dataset:
        new_dataset.write(input_filtered, 1)
    return


def add_field(input_shp,input_table,start_column,end_column):
    '''
    :param input_shp: pathways of input shapefiles
    :param input_table: pathways of tables consist of joined fields (should be a dataframe)
    :param start_column: the start number of column corresponds to the joined fields
    :param end_column:  the end number of column corresponds to the joined fields
    :return:
    '''
    driver2 = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver2.Open(input_shp, 1)
    for i in input_table.columns[start_column:end_column]:    
        fldDef2 = ogr.FieldDefn(i, ogr.OFTReal)
        fldDef2.SetWidth(30)  # total 16 numbers
        fldDef2.SetPrecision(10)  # 10 digits after dicimou
        layer = dataSource.GetLayer()
        # layer.CreateField(fldDef)
        layer.CreateField(fldDef2)
        for features in layer:
            fid = features.GetFID()
            features.SetField(i, input_table[i][fid])
            layer.SetFeature(features)  # added in order to save field value
    return
#(Generally needs to be run twice)



def tidy_zero(inputpath):
    '''
    :param inputpath: the raster needed to be tidied
    :return: the newly revised raster array
    '''
    raster_array = rasterio.open(inputpath).read(1)
    raster_array[np.isnan(raster_array)] = 0
    raster_array[np.where(raster_array <0)] = 0
    return (raster_array)

def clip_map(outpath, inputpath, cutline):
    '''
    :param outpath: newly clipped raster data output directory
    :param inputpath: initial raster data input directory
    :param cutline: boudary vector data input directory
    :return: the newly clipped raster data
    '''
    info = gdal.Open(inputpath)
    return (gdal.Warp(outpath,info,cutlineDSName=cutline,cropToCutline=True, dstNodata = -999))


def zonal_summary(crop_or_animal_type_list,crop_or_animal_map_list,summary_map_path,summary_map_feature_number,summary_type,nodata_value, output_path):
    Zonal_cali = dict.fromkeys(crop_or_animal_type_list)
    Zonal_output = dict.fromkeys(crop_or_animal_type_list)
    for i in Zonal_output:
        Zonal_output[i] = [None] * summary_map_feature_number
    crop_or_animal_map_wddt = dict(zip(crop_or_animal_type_list,crop_or_animal_map_list))
    for i in crop_or_animal_map_wddt:
        Zonal_cali[i] = zonal_stats(summary_map_path,crop_or_animal_map_wddt[i],stats=[summary_type],nodata=nodata_value)
        for j in range(0,summary_map_feature_number):
            Zonal_output[i][j]=Zonal_cali[i][j][summary_type]
    df_Zonal_cali = pd.DataFrame(Zonal_output)
    df_Zonal_cali.to_excel(output_path,\
                        index=False)
    return

def split_raster(outpath,inpath, sizex, sizey):
    '''
    para: outpath is the output pathway of newly generated pathways. e.g. r'K:/基础数据/A.数据/LUCAS_tile_folder/tile_'. Note this is not full name, only the pathway plus a part of file names. The rest part of the names will be filled by raster positions and sizes
    para: inpath is the input pathway of the original raster. e.g. r'F:/基础数据/A.数据/LUCAS_dataset/LUCAS_tile_folder/LUCAS.tif'. We can just input the full name of the original raster here
    para: sizex, the number of columns
    para: sizey, the number of rows 
    '''
    ##set the size of each tile（# the numbers of rows and columns)
    tile_size_x = sizex
    tile_size_y = sizey
    
    ds = gdal.Open(inpath)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize
    
    for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
            com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(inpath) + " " + str(outpath) + str(i) + "_" + str(j) + ".tif"
            os.system(com_string)

def mosaic_map(inpath,outpath,CRS):
    '''
    :param inpath: the directories comprise all tile tiffiles. File names are needed to end with .tif
    :param outpath: output directory. File names are needed to end with .tif
    CRS: THE NAME OF TARGETED GEOGRRAPHCIAL COORDINATE SYSTEM
    :return:
    '''
    # Creat an empty list for the datafiles
    src_files_to_mosaic = []

    for fp in inpath:
       src = rasterio.open(fp)
       src_files_to_mosaic.append(src)

    # Merge function returns a single mosaic array and the transformation info
    mosaic, out_trans = merge(src_files_to_mosaic,nodata=-999)
    show(mosaic, cmap='terrain')

    #save the image
    ## Copy the metadata
    out_meta = src.meta.copy()

    ## Update the metadata
    out_meta.update({"driver": "GTiff",
                     "height": mosaic.shape[1],
                     "width": mosaic.shape[2],
                     "transform": out_trans,
                     "crs": CRS,
                     "nodata":-999
                        }
                       )
    ## write the map
    with rasterio.open(outpath, "w", **out_meta) as dest:
        dest.write(mosaic)


def aggregate(map_list):
    '''
    aggregate the maps with the tidy_zero() function
    '''
    Result_array = tidy_zero(map_list[0])
    for i in map_list[1:]:
        Add_array = tidy_zero(i)
        Result_array = Result_array + Add_array
    return Result_array

def aggregate_ori(map_list):
    '''
    aggregate the original maps with the rasterio.open().read() function
    '''
    Result_array = rasterio.open(map_list[0]).read(1)
    for i in map_list[1:]:
        Add_array = rasterio.open(i).read(1)
        Result_array = Result_array + Add_array
    return Result_array

def find_str_infile(keyword, aim_dir):
    '''
    :param keyword: should be a string, like 'pig.tif'
    :aim_dir: r'E:\Code\Res_prj\Paper_PhD\Air_pollution\A_Self_code'
    '''
    for root, dirs, files in os.walk(aim_dir, onerror=None):  # walk the root dir
        for filename in files:  # iterate over the files in the current dir
            file_path = os.path.join(root, filename)  # build the file path
            try:
                with open(file_path, "rb") as f:  # open the file for reading
                    # read the file line by line
                    for line in f:  # use: for i, line in enumerate(f) if you need line numbers
                        try:
                            line = line.decode("utf-8")  # try to decode the contents to utf-8
                        except ValueError:  # decoding failed, skip the line
                            continue
                        if keyword in line:  # if the keyword exists on the current line...
                            print(file_path)  # print the file path
                            break  # no need to iterate over the rest of the file
            except (IOError, OSError):  # ignore read and permission errors
                pass

def read_matrix_shap(inpath):
    '''
    parameter inpath means the path of an array that you want its size
    '''
    result = rasterio.open(inpath).read(1).shape
    print(result)
    return

def get_geo_info(raster_path):
    # Open the raster dataset
    raster_dataset = gdal.Open(raster_path)

    if raster_dataset is None:
        print(f"Could not open the raster file: {raster_path}")
        return None

    # Get raster size (width and height)
    width = raster_dataset.RasterXSize
    height = raster_dataset.RasterYSize
    
    # Get geotransform (transformation matrix) and resolution
    geotransform = raster_dataset.GetGeoTransform()

    # Close the raster dataset
    raster_dataset = None

    return width, height, geotransform

def plot_formal(Raster_path, Vector_path, canva_size, canva_subfignum,crs_number, color_list_default, clas_list):
    '''
    :param Raster_path: the file path of being plotted raster
    :param Vector_path: the file path of being plotted raster
    :param canva_size: format-> (width,hight);default->(8,10)
    :param canva_subfignum: format->[subfigure row,subfigure column] ; default ->[1,1],because defaultly we only need one main figure
    :param crs_number: format -> use number directly ; default -> 3035
    :param color_list: format->['','',...]; default ->Yellow2Green_list = ['white', '#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']
    :Blue2Red_list = ['white', '#2B83BA', '#ABDDA4','#FFFFBF', '#FDAE61', '#D7191C']
    Gren2Red_list = ['white', '#1A9641','#A6D96A','#FFFFC0','#FDAE61','#D7191C']
    :param clas_list: format->[, , ...]; [0, 10, 30, 120, 240, np.inf]
    :return:
    '''
    # Plotting maps
    ## Obtaining the characteristics of the input data
    info_input = gdal.Open(Raster_path)

    ### Longitude and latitude
    geo_transform = info_input.GetGeoTransform()  # (obtain the basic information of raster data that used to set figures' properties)
    origin_x = geo_transform[0]  # (starting longitude)
    origin_y = geo_transform[3]  # (starting latitude)
    pixel_width = geo_transform[1]  # (widths of pixels)
    pixel_height = geo_transform[5]  # (heights of pixels)

    ### Plotting data extent
    n_rows = info_input.RasterYSize  # (the number of rows)
    n_cols = info_input.RasterXSize  # (the number of columns)
    in_data = info_input.ReadAsArray()  # (matrix information)
    lon_range_new = np.linspace(origin_x, (origin_x + pixel_width * n_cols - pixel_width), n_cols)  # (经度范围)
    lat_range_new = np.linspace(origin_y, (origin_y + pixel_height * n_rows - pixel_height), n_rows)  # (纬度范围)

    ### Define the bins for raster data
    class_bins = clas_list
    pre_input_class = np.digitize(in_data,class_bins,right=True)
    #pre_input_class = xr.apply_ufunc(np.digitize, in_data, class_bins)  # (classifying the raster)
    extent = (lon_range_new.min(), lon_range_new.max(), lat_range_new.min(), lat_range_new.max())

    ## Setting canvas
    ### Setting the size of the figures
    fig = plt.figure(figsize=canva_size)  # 定义figure的大小

    ### Setting the projection of the canvas
    proj = ccrs.epsg(crs_number)  # （choosing projecting system, filling the numbers of corresponding maps）
    ax = fig.subplots(canva_subfignum[0], canva_subfignum[1], subplot_kw={'projection': proj})  # (main figure)
    # (tht canvas' projection should be specified to espg:3035, but for vector and raster data, they should keep their original projections)

    ### Setting the showing extent of the canvas
    region = [-10, 35, 32, 72]  # (starting longitude, ending longitude, starting latitude, ending latitude)
    ax.set_extent(region)  # (setting the nets and dots to the specified extent)
    '''Setting the nets and dots (not use temporarily)
    lb = ax.gridlines(draw_labels=False, x_inline=False, y_inline=False, \
                      linewidth=0.1, color='gray', alpha=0.5, linestyles='--')

    lb.xlocator = mticker.FixedLocator(range(-64, 56, 10))
    lb.ylocator = mticker.FixedLocator(range(-22, 72, 10))
    lb.top_labels = False
    lb.right_labels = None
    lb.ylabel_style = {'size': 20, 'color': 'k'}
    lb.xlabel_style = {'size': 20, 'color': 'k' }
    lb.rotate_labels = False
    '''
    ##Color setting using listed colors because we are going to plot classification maps
    ### Calculate the frequency distribution
    unique_elements, counts = np.unique(pre_input_class, return_counts=True)
    color_list_pre = deepcopy(unique_elements).tolist()
    
    ###set color list dynamically according to the frequency distributions of color classes
    color_list = [None] * len(color_list_pre)
    u = 0
    while u < len(color_list_pre):
        if color_list_pre[u] == 0:
             color_list[u] = color_list_default[0]
        elif color_list_pre[u] == 1:
            color_list[u] = color_list_default[1]
        elif color_list_pre[u] == 2:
            color_list[u] = color_list_default[2]
        elif color_list_pre[u] == 3:
            color_list[u] = color_list_default[3]
        elif color_list_pre[u] == 4:
            color_list[u] = color_list_default[4]
        else:
            color_list[u] = color_list_default[5]
        u = u + 1 
    
    cmap = ListedColormap(color_list)
    '''
    # legends setting
    axpos = ax.get_position()
    caxpos = mpl.transforms.Bbox.from_extents(
        axpos.x1 + legend_interval,
        axpos.y0,
        axpos.x1 + legend_interval + legend_width,
        axpos.y1
    )
    cax = ax.figure.add_axes(caxpos)
    '''
    ## Plotting execuation
    ax.add_geometries(Reader(Vector_path).geometries(), ccrs.PlateCarree(), \
         facecolor = 'none', edgecolor = 'k', linewidth = 0.8)
    ### Plotting the raster
    ax.imshow(pre_input_class, cmap=cmap, extent=extent, interpolation='none', transform=ccrs.PlateCarree())
    plt.axis('off')
    #cs = ax.imshow(pre_Whea_class, cmap = cmap, extent= extent, transform = ccrs.PlateCarree())
    #(plotting an image)
    '''
    ##Adding legends
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 20
    plt.colorbar(cs,cax=cax).ax.tick_params(direction='in')
    '''
    plt.show()
    return

def dict_name_path(name_as_keys,file_paths):
    '''
    para: name_as_keys-> a list encompassing names of keys of the targeted dictionary->['Fruit','Vege']
    para: file_path-> a list encompassing pathways of maps->[r'xxx/vege.tif',r'xxx/fruit.tif']
    This function can help to sort file paths as the order in pre defined keys. But note that, if we have two files that satisfy the criteria, it only match the first file path
    '''
    result_dict = {}
    for keyword in name_as_keys:
        matching_paths = [path for path in file_paths if keyword in path]
        if matching_paths:
            result_dict[keyword] = matching_paths[0]  # Assuming you want to store only the first matching path
    return result_dict


def del_keys_dict(ori_dict,keys_delete_list):
    for key in keys_delete_list:
        if key in ori_dict:
            del ori_dict[key]
    return ori_dict
        
        

def replace_keys(orig_dict, replacement_list):
    replaced_dict = {}
    for new_key, old_key in zip(replacement_list, orig_dict.keys()):
        replaced_dict[new_key] = orig_dict[old_key]
    return replaced_dict

def filter_dict(dictionary, selected_keys):
    return {key: value for key, value in dictionary.items() if key in selected_keys}

def sort_dict_by_order(dictionary, order):
    # Create a dictionary to map each key to its position in the order
    order_dict = {key: index for index, key in enumerate(order)}
    
    # Sort the dictionary based on the order
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: order_dict.get(item[0], float('inf'))))
    
    return sorted_dict

def del_elemt_list(Ori_list,Del_elemt_ord,):
    '''
    para: ori_list, the original list to be processed
    para: Del_elemt_ord, the list of orders of elements to be deleted, eg:[5,8,10,14]
    '''
    Li_original = Ori_list
    indices_to_delete = Del_elemt_ord
    Li_new = [Li_original[i] 
              for i in range(len(Li_original)) 
               if i not in indices_to_delete]
    return Li_new


"""def cali_fig(raster_ori_path,shapfile_path,cali_fac_tab,attri_colum,cali_raster_path):
    '''
    : param raster_ori_path: the pathway of the original raster map.
    : param shapfile_path: the pathway of the shapefile
    : param cali_fac_tab: the calibration factor from excel files
    : attri_colum: the corresponding column number in the calibration factor file. for example, we use VitlCp_OneOne_name.index(i) + 1
      to represent the number of the column. And we must take care whether the number equels to index or index+1 
    : cali_raster_path: the pathways of calibrated raster pathways
    '''
    # Load clipping shapefile
    region_gdf = gpd.read_file(shapfile_path)
    # Load raster data
    with rasterio.open(raster_ori_path) as src:
        raster_data = src.read(1)  # Assuming single-band raster
        raster_crs = src.crs
        raster_transform = src.transform
        raster_meta = src.meta.copy()
    
        # Mask raster data with country boundaries
        for index, region in region_gdf.iterrows():
            geom = region.geometry
            out_image, out_transform = mask(src, [geom], crop=True)
            # get the indices of sliced rasters in the original raster
            row_start = int((out_transform[5] - raster_transform[5]) / raster_transform[4])  # Calculate row start
            col_start = int((out_transform[2] - raster_transform[2]) / raster_transform[0])  # Calculate column start
            row_end = row_start + out_image.shape[1]  # Calculate row end
            col_end = col_start + out_image.shape[2]  # Calculate column end
            if not np.all(out_image == -999): #(if not all values are -999)
                #(Note: identify the valid cells)
                Position_in_sliced_raster = np.where (out_image != -999)
                Position_in_sliced_raster_corr_ori = np.where( out_image[0,:,:] != -999 )
                # Calculate calibration factor for the country
                calibration_factor = cali_fac_tab.iloc[index,attri_colum]

                # Apply calibration factor to the raster values for the country
                calibration_result = out_image * calibration_factor
                out_image[Position_in_sliced_raster] =  calibration_result[Position_in_sliced_raster]

                # Write calibrated values back to raster data
                
                array1,array2 = Position_in_sliced_raster_corr_ori
                array1 = array1 + row_start
                array2 = array2 + col_start
                Position_in_ori_raster = (array1, array2)
                
                raster_data[Position_in_ori_raster] = \
                    out_image[Position_in_sliced_raster]

    # Save calibrated raster
    with rasterio.open(cali_raster_path, 'w', **raster_meta) as dst:
        dst.write(raster_data, 1)"""

def cali_fig(Ori_ras_path, Exam_ras_path, Shp_path,Fac_df, Shp_field, Fac_field, Value_field, Fac_reso, Cali_map_path):
    '''
    This function is based on rasterization of geopandas files
    para: Shp_path, the pathway of the original shapefile
    para: Fac_df, the dataframe containing the coefficient we need to multiply
    para: Shp_field, the common field(in the shapefile) to merge the shapefile and the dataframe file. eg:"FID_1"
    para: Fac_field, the common field(in the coefficient dataframe) to merge the shapefile and the dataframe file. eg:"Name_abbre"
    para: Value_field, the field consisting of the targeted coefficient.
    para: Ori_ras_path, the pathway of original map which would be calibrated
    para: Exam_ras_path, the example raster to provide geo information
    para: Fac_reso, the resolution of the rasterized map. eg: 0.0833333333333333
    Pj_path.output_wd+'test.tif'
    '''
    # Load the shapefile
    shapefile_path = Shp_path
    gdf = gpd.read_file(shapefile_path)
    # Load the dataframe with the field data
    df = Fac_df
    # Merge the shapefile and dataframe based on a common key
    # Assuming "your_key" is the common key in both the shapefile and the dataframe
    gdf = gdf.merge(df, left_on= Shp_field, right_on = Fac_field, how="inner")
    # Get the field to be rasterized from the dataframe
    field_to_rasterize = gdf[Value_field]
    # Create shapes with the field data
    shapes = [(geom, value) for geom, value in zip(gdf.geometry, field_to_rasterize)]


    existing_map_path = Exam_ras_path
    with rasterio.open(existing_map_path) as src:
        existing_transform = src.transform
        existing_bounds = src.bounds
        existing_crs = src.crs

    # Assign the existing map's transform and bounds to the rasterized map
    transform = existing_transform

    # Specify the desired resolution for the raster
    resolution = Fac_reso # Adjust as needed

    # Rasterize the shapefile based on the specified field
    width = int((existing_bounds[2] - existing_bounds[0]) / resolution)
    height = int((existing_bounds[3] - existing_bounds[1]) / resolution)
    raster_shape = (height, width)

    # Create transform for output raster based on spatial resolution and bounds
    transform = from_origin(existing_bounds[0], existing_bounds[3], resolution, resolution)

    mask = rasterize(
        shapes,
        out_shape=raster_shape,
        transform=transform,
        fill=0,
        dtype=np.float32,
    )
    
    
    # Load your original GeoTIFF file
    original_tif_path = Ori_ras_path
    # Multiply the exported array with your original GeoTIFF data
    original_data = tidy_zero(original_tif_path)
    result = original_data * mask
 
    # Define the output file path
    output_tif_path = Cali_map_path

    # Specify the metadata for the output GeoTIFF
    metadata = {
        'driver': 'GTiff',
        'count': 1,  # Number of bands
        'dtype': 'float64',  # Data type of the rasterized values
        'width': mask.shape[1],  # Width of the raster
        'height': mask.shape[0],  # Height of the raster
        'crs': existing_crs,  # Coordinate reference system
        'transform': transform  # Affine transformation
    }

    # Write the rasterized array to a GeoTIFF file
    with rasterio.open(output_tif_path, 'w', **metadata) as dst:
        dst.write(result, 1)  # Write the array to the first band


def text_to_tif(Inputpath,skiprow,latcol,loncol,datacol,reso,Intermethd, Outputpath):
    '''
    para: Inputpath, input pathway
    skiprow: rows needed to be deleted, starting from 1 not 0
    latcol: the column number of lattitude data, starting from 0
    loncol: the column number of longitude data, starting from 0
    datacol: the column number of main data, starting from 0
    Intermethd: can be 'linear', 'nearest', 'cubic', defult is 'linear'
    Outputpath: output pathway
    An example: Imp_func.text_to_tif(Pj_path.Input_prj_wd + 'Air_pollution_database/Database_collection/EDGAR Series/EDGAR_V6.1/v8.1_FT2022_AP_NH3_2017_MNM/v8.1_FT2022_AP_NH3_2017_MNM.txt',\
    3,0,1,2,0.1,'linear',Pj_path.Input_prj_wd + 'Air_pollution_database/Database_collection/EDGAR Series/EDGAR_V6.1/v8.1_FT2022_AP_NH3_2017_MNM/ManuMana2017.tif')
    '''
    
    
    textdata = np.genfromtxt(Inputpath, delimiter=';', skip_header=skiprow)
    latitude = textdata[:,latcol] 
    longitude = textdata[:, loncol]
    emission = textdata[:, datacol]
    
    # Define grid boundaries
    lat_min, lat_max = min(latitude), max(latitude)
    lon_min, lon_max = min(longitude), max(longitude)
    
    # Define grid resolution
    resolution1 = reso  # set the resolution of new maps, and since latitude will decrease from max to min, we need to use negetive resolution values here
    resolution2 = -reso 
    
    # Create a grid
    grid_lon, grid_lat = np.meshgrid(np.arange(lon_min, lon_max, resolution1),\
        np.arange(lat_max, lat_min,  resolution2)) #（the first parameter of meshgrid is x axis of the map, so we should use lon, while the socond parameter is y axis, which coresponds to lat)
    #(and noted that the latitude starts from max to min because south hemisphere has negetive latitude values)
    
    # Interpolate emission data onto the grid
    grid_emission = griddata((latitude,longitude), emission, (grid_lat,grid_lon), method=Intermethd)
    
    # Save the grid as a TIFF raster image
    with rasterio.open(Outputpath, \
        'w', driver='GTiff', height=grid_emission.shape[0], width=grid_emission.shape[1], count=1, dtype='float64', crs='+proj=latlong',\
        transform=from_origin(lon_min, lat_max, resolution1, resolution1)) as dst:
        dst.write(grid_emission, 1) #(here we can't use resolution2, it will lead to raster movements)

def asc_to_tif(input_path, output_path):
    asc_file = input_path
    tif_file = output_path

    # Open the ASC file
    with rasterio.open(asc_file) as src:
        # Read the data into a numpy array
        data = src.read(1)
        
        # Get the metadata from the source file
        meta = src.meta.copy()
        
        # Update the metadata for the GeoTIFF file
        meta.update({
            'driver': 'GTiff',
            'dtype': 'float32',
            'nodata': src.nodata
        })

    # Write the data to a GeoTIFF file
    with rasterio.open(tif_file, 'w', **meta) as dst:
        dst.write(data, 1)

    print(f"Conversion complete: {tif_file}")


def replace_raster(ori_ras,rep_ras,mask_shp,ori_ras_nodata,mod_ras):
    '''
    ori_ras: original raster which will be replaced parts of grids
    rep_ras: rasters providing new grid values
    ori_ras_nodata: the nodata value in the original raster, normally could be -999
    mod_ras: the pathway of newly modified rasters
    '''
    with rasterio.open(ori_ras) as target_src:
        target_data = target_src.read()
        target_profile = target_src.profile
        target_transform = target_src.transform
        
        # Open the shapefile mask
        mask_shapefile = gpd.read_file(mask_shp)
            
        # Apply the mask to the larger raster to get the region to replace
        masked_tarori_data, masked_tar_transform = mask(target_src, mask_shapefile.geometry.apply(mapping), crop=True)
        
        # Get the row and column numbers of shapfiles in the raster
        row_start = int((masked_tar_transform[5] - target_transform[5]) / target_transform[4])  # Calculate row start
        col_start = int((masked_tar_transform[2] - target_transform[2]) / target_transform[0])  # Calculate column start
        row_end = row_start + masked_tarori_data.shape[1]  # Calculate row end
        col_end = col_start + masked_tarori_data.shape[2]  # Calculate column end
        
        
        # Open the smaller raster (source)
        with rasterio.open(rep_ras) as source_src:
            source_data = source_src.read()
            source_profile = source_src.profile
            source_transform = source_src.transform
            
            # get the mask data in the source raster
            masked_sour_data, masked_sour_transform = mask(source_src, mask_shapefile.geometry.apply(mapping), crop=True)

            # check if the two masked data has the same size
            if masked_sour_data.shape == masked_tarori_data.shape:
                masked_tar_data = np.where(masked_tarori_data !=ori_ras_nodata, masked_sour_data, masked_tarori_data)
                #(if true, use masked_sour_data, otherwise use orginial -999)
            else:
                # Generate the coordinates for the target grid
                x = np.linspace(0, masked_sour_data.shape[2] - 1, masked_sour_data.shape[2])
                #（np.linspace(start, stop, num): This function returns num evenly spaced samples, calculated over the interval [start, stop].）
                y = np.linspace(0, masked_sour_data.shape[1] - 1, masked_sour_data.shape[1])
                x_target = np.linspace(0, masked_tarori_data.shape[2] - 1, masked_tarori_data.shape[2])
                y_target = np.linspace(0, masked_tarori_data.shape[1] - 1, masked_tarori_data.shape[1])

                # Create a meshgrid from the coordinates
                X, Y = np.meshgrid(x, y)
                X_target, Y_target = np.meshgrid(x_target, y_target)
                
                # Resample array2 along the second dimension to align with array1
                masked_tar_data_raw = griddata((X.flatten(), Y.flatten()), masked_sour_data.flatten(), (X_target, Y_target), method='linear')
                masked_tar_data_3D = np.broadcast_to(masked_tar_data_raw,masked_tarori_data.shape)
                masked_tar_data = np.where(masked_tarori_data !=ori_ras_nodata,masked_tar_data_3D,masked_tarori_data)


    # Update the corresponding pixels in the larger raster with the masked data from the smaller raster
    ## we don't want to give -999 to the original map,otherwise it will cause nodata in the rectangle area in other countries
    masked_tar_data_withoutnodata = (masked_tar_data != ori_ras_nodata)

    target_data[:, row_start:row_end, col_start:col_end][masked_tar_data_withoutnodata] = masked_tar_data[:,:,:][masked_tar_data_withoutnodata]
    ##(the first : means all bands. Target_data has three dimensions, the first is for banks information, the second for rows information, the third for column information)

    # Write the modified data back to a new raster
    with rasterio.open(mod_ras, 'w', **target_profile) as modified_src:
        modified_src.write(target_data)
    
def conv_df2dict(ori_df,df_col_key,df_col_value):
    '''
    para: ori_df, the dataframe to be converted, eg:OSDname_vital_SPAMcropmaps
    para: df_col_key, the column in the original dataframe to be converted to keys in the new dictionary
    para: df_col_value, the column in the original dataframe to be converted to values in the new dictionary,eg:'Crop_index'
    '''
    return ori_df.set_index(df_col_key)[df_col_value].to_dict()

def conv_dict2df(ori_dict,new_df_colname,new_df_colval):
    '''
    para: ori_dict, the dataframe to be processed
    para: new_df_column, the column name in the new dataframe
    para:  new_df_colval, the values under the column name
    '''
    KEY = ori_dict.keys()
    VALUES = ori_dict.values()
    
    return pd.DataFrame.from_dict({
        new_df_colname: KEY,
        new_df_colval:VALUES})

def dict_del_nan(ori_dict):
    return {key: value for key, value in ori_dict.items() if not (isinstance(value, float) and np.isnan(value))}

def dict_rep_keys(new_key_list,ori_dict):
    '''
    para: new key list is the list containing new keys
    para: ori_dict means the original dictionary
    '''
    {new_key_list[i]: value for i, (_, value) in enumerate(ori_dict.items())}

def join_dict2df(ori_df,join_dict,link_col_name,cotain_col_name):
    '''
    para: ori_df, the dataframe to be connectted, eg:SPAM_vital_cropsnames_df
    para: join_dict, the dictionary to link to the dataframe, eg: SPAM_vital_cropprod
    para: cotain_col_name, the column name that will contain the new field in the dataframe,eg:'globprod'
    para: link_col_name, the column which is regarded as the key to link both sides, eg:'xxx'
    '''
    ori_df[cotain_col_name] = ori_df[link_col_name].map(pd.Series(join_dict))
    return ori_df

def plot_array(Data_arr, lon_min,lon_max,lat_min,lat_max):
    '''
    para, the matrix to be mapped
    lon_min, lon_max, lat_min, lat_max: information needs to be gotten using xarray or information already known
    '''
    # Create a new figure
    plt.figure(figsize=(10, 6))
    # Define the map projection (e.g., PlateCarree for longitude/latitude data)
    ax = plt.axes(projection=ccrs.PlateCarree())
    # Plot the data on the map
    img = plt.imshow(Data_arr, origin='lower', extent=[lon_min, lon_max, lat_min, lat_max], transform=ccrs.PlateCarree(), cmap='viridis')
    # Add coastlines for reference
    ax.coastlines()
    # Add a colorbar
    cbar = plt.colorbar(img)
    cbar.set_label('Data Value')
    # Set title and show the plot
    plt.title('Plot')
    plt.show()
    
def conv_array2tif(lon,lat,values_of_database,outpath):
    '''
    using xarry needs to ensure the path is under full English pathways
    this function is based on the matrix obtained from xarray
    para:lon, the longitude vector of the matrix 
    para: lat, the latitude vector of the matrix
    para: tim, time dimention of the matrix
    para: xarray, the nc file opened by xarray
    para: values_of_database, should be two dimention matrix, the exact variable value
    '''
    longitude = lon
    latitude = lat
    # Define grid boundaries
    lat_min, lat_max = min(latitude), max(latitude)
    pixel_height = (lat_max - lat_min)/latitude.shape[0]
    lon_min, lon_max = min(longitude), max(longitude)
    pixel_width = (lon_max - lon_min)/longitude.shape[0]
    R = (lon_min, pixel_width, 0, lat_max, 0, -pixel_height)
    R = tuple(R)
    tiffile = outpath  # write to tiff file (!changable)
    geotiff = gdal.GetDriverByName('GTiff')
    dst_ds = geotiff.Create(tiffile, longitude.shape[0], latitude.shape[0], 1, gdal.GDT_Float64)
    dst_ds.SetGeoTransform(R)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    dst_ds.SetProjection(srs.ExportToWkt())
    dst_ds.GetRasterBand(1).WriteArray(values_of_database)
    dst_ds.FlushCache()

def covt_nc_to_tif(tif_path, nc_path):
    # Path to the input TIFF file
    tiff_file = tif_path

    # Path to the output NetCDF file
    nc_file = nc_path

    # Read the TIFF file
    with rasterio.open(tiff_file) as src:
        data = src.read(1)  # Read the first band
        transform = src.transform
        crs = src.crs
        width = src.width
        height = src.height

    # Create coordinates based on the transform
    x_coords = np.arange(width) * transform[0] + transform[2]
    y_coords = np.arange(height) * transform[4] + transform[5]

    # Create an xarray DataArray
    data_array = xr.DataArray(
        data,
        dims=("y", "x"),
        coords={"y": y_coords, "x": x_coords},
        attrs={"crs": crs.to_string(), "transform": transform}
    )

    # Create an xarray Dataset
    dataset = xr.Dataset({"data": data_array})

    # Save the dataset to a NetCDF file
    dataset.to_netcdf(nc_file)

    print(f"TIFF file has been converted to NetCDF file: {nc_file}")

def open_plk(plk_path):
    with open(plk_path, 'rb') as f:
        return pickle.load(f)

def save_plk(plk_path,plk_data):
    '''
    para: plk_data, the data to be saved
    '''
    with open(plk_path, 'wb') as f:
        pickle.dump(plk_data, f)
        return

def check_balance_ras(Balaarray,Qua_upbound,Qua_lowbound):
    '''
    para: Balarray, well organized array to be judged
    para: Qua_upbound, the upper boundary of quality check
    para: Qua_lowbound, the lower boundary of quality check
    '''
    print('Not_bala_pla:',np.where(Balaarray != 0))
    Not_good_number_mask = np.where((Balaarray > Qua_upbound)|(Balaarray < Qua_lowbound))
    High_number_mask = np.where(Balaarray > Qua_upbound)
    Low_number_mask = np.where(Balaarray < Qua_lowbound)
    print('Not_bala_num:',len(Not_good_number_mask[0]))
    print('High_val_num:',len(High_number_mask[0]))
    print('Low_val_num:',len(Low_number_mask[0]))
    print('Max:', np.max(Balaarray))
    print('Min:', np.min(Balaarray))
    print(np.sum(Balaarray) )
