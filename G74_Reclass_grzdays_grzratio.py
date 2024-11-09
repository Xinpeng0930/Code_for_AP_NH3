'''
This script aims to count grazing days and get the grazing ratios based on Vira's assumptions
This script could be excuated automatically
'''

#%%
#Necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
#----------------------------------------------------input_module----------------------------------------------------
temp_wd = Imp_func.glob.glob(r'K:/基础数据/A.数据/Copernicus_Europe_data/E-OBS_Convt/*.tif',recursive=False)
Temp_output_wd = r'K:/基础数据/A.数据/Copernicus_Europe_data/'
# Open and read raster
grz_ratio = Imp_func.rasterio.open(Pj_path.output_prj_wd+"Graz_ratio/grz_days_ratio_clip.tif").read(1)
grz_ratio_interpo_wd = Pj_path.output_prj_wd+"Graz_ratio/grzday_ratio_spline.tif"
# (WE used the r.fillnulls tool in QGIS to generate the layer)

#%%
#----------------------------------------------------processing_module----------------------------------------------------
# see G73 for the obtaining of daily temporature maps

# get the tempertature 
# OUTPUT_DATA
with Imp_func.rasterio.open(temp_wd[0]) as src:
    ## read source array and get its geo-information
    temp_profile = src.profile
    temp_array = src.read()
    ## reclassify temperature with accordance to criteria
    temp_array[temp_array < 10] = 0
    temp_array[temp_array >= 10] = 1


## continue adding resting figures
for f in temp_wd[1:]:
    with Imp_func.rasterio.open(f) as rest:
        assert temp_profile == rest.profile, 'stopping, file {} and  {} do not have matching profiles'\
            .format(temp_wd[0],f)
        rest_array = rest.read()
        ## reclassify temperature with accordance to criteria
        rest_array[rest_array < 10] = 0
        rest_array[rest_array >= 10] = 1
        temp_array = temp_array + rest_array

#OUTPUT_INTE_FILE
with Imp_func.rasterio.open(Temp_output_wd + 'Temp_count.tif', 'w', **temp_profile) as dst:
    dst.write(temp_array, indexes=[1])

#%%
# get the grazing ratio
Grz_ratio = Imp_func.rasterio.open(Temp_output_wd + 'Temp_count.tif').read(1) / 365
Grz_ratio [Imp_func.np.where(Grz_ratio==0)] = Imp_func.np.nan

#OUTPUT_INTE_FILE
Imp_func.output_ras(Temp_output_wd + 'Temp_ratio',Temp_output_wd + 'Temp_count.tif',\
    'EPSG:4326',Grz_ratio)
Imp_func.clip_map(Pj_path.output_prj_wd+"Graz_ratio/grz_days_ratio_clip.tif",\
    Temp_output_wd + 'Temp_ratio',Pj_path.EFTA_UK_wd)

#%%
#fill nan values
## get the interpolation layer using r.fillnulls tool in qgis
#OUTPUT_INTE_FILE
Imp_func.clip_map(Pj_path.output_prj_wd+'Graz_ratio/grzday_ratio_splineEFTA.tif',\
    grz_ratio_interpo_wd,Pj_path.EFTA_UK_wd)

#OUTPUT_DATA
grz_ratio[Imp_func.np.isnan(grz_ratio)] = \
    Imp_func.rasterio.open(Pj_path.output_prj_wd+'Graz_ratio/grzday_ratio_splineEFTA.tif').read(1)[Imp_func.np.isnan(grz_ratio)]

# Export raster
# OUTPUT_FILE
Imp_func.output_ras_filtered(Pj_path.output_prj_wd + 'Graz_ratio/grz_ratio_filled.tif',\
    Pj_path.output_prj_wd+"Graz_ratio/grz_days_ratio_clip.tif",'EPSG:4326',grz_ratio)

#(Filled the data in small islands in Greece, but border areas in the layer still have missed values)



