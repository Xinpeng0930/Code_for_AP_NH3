#%%
'''
This script is aiming to get the ammonia emissions from fertilizer by crop
This script can be run automatically
running time is 400s
'''

#%%
# Import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
# Setting pathways
## Pathway for Chemical fertilizer use 
Chemfer_df = Imp_func.open_plk(r'../B_Output/A50.pkl')

## Pathway for soil pH (Europe)
Soil_phEFTA_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/Soilph_EFTA.tif'
Soil_phEFTA_revisewd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/Soilph_revise.tif'

## Pathway for monthly mean air temperature (Europe)
Airtemp_meanEFTA_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/Airtempmean_EFTA.tif'

Temp_ds = Imp_func.xr.open_dataset(r'K:/Default_database/Temperature/cruts1120_temp.nc') #we got that the dataset is a monthly dataset
#(can't use Chinese directory, otherwise the computer can't identify it)
#Imp_func.find_str_infile('xr.open_dataset',r'E:\Code\Res_prj\Paper_PhD\Air_pollution\A_Self_code')

## Pathways for air temperature (original)
Air_temp_Jan_wd = r'K:/基础数据/B.数据/cruts1120temp/Jan_temp.tif'
Air_temp_Feb_wd = r'K:/基础数据/B.数据/cruts1120temp/Feb_temp.tif'
Air_temp_Mar_wd = r'K:/基础数据/B.数据/cruts1120temp/Mat_temp.tif'
Air_temp_Apr_wd = r'K:/基础数据/B.数据/cruts1120temp/Apr_temp.tif'
Air_temp_May_wd = r'K:/基础数据/B.数据/cruts1120temp/May_temp.tif'
Air_temp_June_wd = r'K:/基础数据/B.数据/cruts1120temp/June_temp.tif'
Air_temp_July_wd = r'K:/基础数据/B.数据/cruts1120temp/July_temp.tif'
Air_temp_Aug_wd = r'K:/基础数据/B.数据/cruts1120temp/Aug_temp.tif'
Air_temp_Sep_wd = r'K:/基础数据/B.数据/cruts1120temp/Sep_temp.tif'
Air_temp_Oct_wd = r'K:/基础数据/B.数据/cruts1120temp/Oct_temp.tif'
Air_temp_Nov_wd = r'K:/基础数据/B.数据/cruts1120temp/Nov_temp.tif'
Air_temp_Dec_wd = r'K:/基础数据/B.数据/cruts1120temp/Dec_temp.tif'

Air_temp_wdlt = [Air_temp_Jan_wd,Air_temp_Feb_wd,Air_temp_Mar_wd,Air_temp_Apr_wd,\
                Air_temp_May_wd,Air_temp_June_wd,Air_temp_July_wd,Air_temp_Aug_wd,\
                Air_temp_Sep_wd,Air_temp_Oct_wd,Air_temp_Nov_wd,Air_temp_Dec_wd]


## Pathways for windspeed (original)
Wind_speed_Jan_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Jan_ws.tif'
Wind_speed_Feb_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Feb_ws.tif'
Wind_speed_Mar_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Mar_ws.tif'
Wind_speed_Apr_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Apr_ws.tif'
Wind_speed_May_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/May_ws.tif'
Wind_speed_June_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/June_ws.tif'
Wind_speed_July_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/July_ws.tif'
Wind_speed_Aug_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Aug_ws.tif'
Wind_speed_Sep_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Sep_ws.tif'
Wind_speed_Oct_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Oct_ws.tif'
Wind_speed_Nov_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Nov_ws.tif'
Wind_speed_Dec_wd = r'K:/基础数据/A.数据/TerraClimate_windspeed/Dec_ws.tif'

Wind_speed_wdlt = [Wind_speed_Jan_wd,Wind_speed_Feb_wd,Wind_speed_Mar_wd,Wind_speed_Apr_wd,Wind_speed_May_wd,Wind_speed_June_wd,\
    Wind_speed_July_wd,Wind_speed_Aug_wd,Wind_speed_Sep_wd,Wind_speed_Oct_wd,Wind_speed_Nov_wd,Wind_speed_Dec_wd ]


## Pathways for fertilization factors in Europe
Fertfac_EFTA_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/fertyp_fac_EFTA.tif'
Fertmedfac_EFTA_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/fermed_fac_EFTA.tif'
Ferttyfac_rice_wd = r'K:/Default_database/raster/Fertilizer_tpmd_fac/Fert_ty_fac_rice.tif'
Fertmedfac_rice_wd = r'K:/Default_database/raster/Fertilizer_tpmd_fac/Fert_md_fac_rice.tif'
Ferttyfac_EFTArice_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/fertp_facrice_EFTA.tif'
Fertmedfac_EFTArice_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/fermed_facrice_EFTA.tif'


## Pathways for total fertilizer use by crop
Cropname = ['Whea','Bar','Maiz','Grenmaiz','Tempgra','Legumfod','Rapesd','Sunflrsd','Soya','Oat','Rice','Rye','Pota',\
    'Sugbt','Peabean','Nuts','Fruit','Vege','Permgra']



#----------------------------------------------------processing_module----------------------------------------------------
#%%
#OUTPUT_DATA
#Calculating fertilizer volatilition factors
## VR_0
VR_0 = 0.093408
VR_0_for_rice = 0.132992

#%%
## f(pH)
### Getting the matrix of European soil pH
#OUTPUT_INTE_FILE
Imp_func.clip_map(r'K:/基础数据/B.数据/HWSD_ORNL/soilph_EFTA.tif',\
r'K:/基础数据/B.数据/HWSD_ORNL/soilph.tif',Pj_path.EFTA_UK_wd)

#%%
### Then we filled some non value gaps in the soilph.tif using ArcGIS
### Next we move to fill the gaps in the original map with the values in the filled map
#OUTPUT_DATA
Soil_ph_ori = Imp_func.rasterio.open(r'K:/基础数据/B.数据/HWSD_ORNL/soilph_EFTA.tif').read(1)
Soil_ph_interp = Imp_func.rasterio.open(Pj_path.output_wd + 'Soil_interpo.tif').read(1) #Get from interpolation in ArcGIS
New_soilph_revise = Imp_func.np.where(Imp_func.np.isnan(Soil_ph_ori),Soil_ph_interp,Soil_ph_ori)

#%%
#OUTPUT_INTE_FILE
Imp_func.output_ras(Soil_phEFTA_wd,\
    r'K:/基础数据/B.数据/HWSD_ORNL/soilph_EFTA.tif','EPSG:4326',New_soilph_revise)

Imp_func.gdal.Warp(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/Soilph_resp.tif', \
        Soil_phEFTA_wd, dstSRS='EPSG:4326', xRes = 0.08333333333333331483, yRes = 0.08333333333333331483,\
            resampleAlg = Imp_func.gdal.GRA_Bilinear)

Imp_func.clip_map(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/Soilph_revise.tif',\
    r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/Soilph_resp.tif',\
    Pj_path.EFTA_UK_wd)

#%%
#OUTPUT_DATA
Soil_ph = Imp_func.tidy_zero(Soil_phEFTA_revisewd) 

### Calculating f(pH) according to Zhan et al.,2021(EST)
e = Imp_func.math.exp(1) #(getting euler's number first)
f_pH = 0.0429 * pow(e,0.4955 * Soil_ph)
f_pH_rice = 0.0224 * pow(e,0.5555 * Soil_ph)

#%%
#OUTPUT_DATA
## f(A)
### Defining the growth periods of crops
Whea_grow_prid_Win = [9,10,11,12,1,2,3,4,5,6,7,8]  
Whea_grow_prid_Win = list(Imp_func.np.array(Whea_grow_prid_Win) -1) # Minusing one is to align the numbers in growth period lists to that in air temperature list 
Whea_grow_prid_Spr = [4,5,6,7,8,9,10]
Whea_grow_prid_Spr = list(Imp_func.np.array(Whea_grow_prid_Spr) -1)

Barl_grow_prid_Win = [9,10,11,12,1,2,3,4,5,6,7]
Barl_grow_prid_Win = list(Imp_func.np.array(Barl_grow_prid_Win) -1)
Barl_grow_prid_Spr = [4,5,6,7,8,9,10]
Barl_grow_prid_Spr = list(Imp_func.np.array(Barl_grow_prid_Spr) -1)

Maiz_grow_prid = [4,5,6,7,8,9,10]
Maiz_grow_prid = list(Imp_func.np.array(Maiz_grow_prid) -1)

Grenmaiz_grow_prid = [4,5,6,7,8,9,10]
Grenmaiz_grow_prid = list(Imp_func.np.array(Grenmaiz_grow_prid) -1)

Tempgras_grow_prid = [1,2,3,4,5,6,7,8,9,10,11,12]
Tempgras_grow_prid = list(Imp_func.np.array(Tempgras_grow_prid) -1)

Legufod_grow_prid = [1,2,3,4,5,6,7,8,9,10,11,12]
Legufod_grow_prid = list(Imp_func.np.array(Legufod_grow_prid) -1)

Rapesd_grow_prid = [8,9,10,11,12,1,2,3,4,5,6,7]
Rapesd_grow_prid = list(Imp_func.np.array(Rapesd_grow_prid) -1)

Sunflrsd_grow_prid = [4,5,6,7,8,9,10]
Sunflrsd_grow_prid = list(Imp_func.np.array(Sunflrsd_grow_prid) -1)

Soya_grow_prid = [4,5,6,7,8,9,10]
Soya_grow_prid = list(Imp_func.np.array(Soya_grow_prid) -1)

Oat_grow_prid = [4,5,6,7,8,9,10]
Oat_grow_prid = list(Imp_func.np.array(Oat_grow_prid) -1)

Rice_grow_prid = [4,5,6,7,8,9,10]
Rice_grow_prid = list(Imp_func.np.array(Rice_grow_prid) -1)

Rye_grow_prid = [9,10,11,12,1,2,3,4,5,6,7]
Rye_grow_prid = list(Imp_func.np.array(Rye_grow_prid) -1)

Pota_grow_prid = [3,4,5,6,7,8,9,10,11]
Pota_grow_prid = list(Imp_func.np.array(Pota_grow_prid) -1)

Sugbt_grow_prid = [4,5,6,7,8,9,10,11]
Sugbt_grow_prid = list(Imp_func.np.array(Sugbt_grow_prid) -1)

Peabean_grow_prid = [2,3,4,5,6,7,8,9]
Peabean_grow_prid = list(Imp_func.np.array(Peabean_grow_prid) -1)

Nuts_grow_prid = [1,2,3,4,5,6,7,8,9,10,11,12]
Nuts_grow_prid = list(Imp_func.np.array(Nuts_grow_prid) -1)

Fruit_grow_prid = [1,2,3,4,5,6,7,8,9,10,11,12]
Fruit_grow_prid = list(Imp_func.np.array(Fruit_grow_prid) -1)

Vegetable_grow_prid =  [1,2,3,4,5,6,7,8,9,10,11,12]
Vegetable_grow_prid = list(Imp_func.np.array(Vegetable_grow_prid) -1)

Permgras_grow_prid = [1,2,3,4,5,6,7,8,9,10,11,12]
Permgras_grow_prid = list(Imp_func.np.array(Permgras_grow_prid)-1)

Crop_grow_prid_wdlt = [Whea_grow_prid_Win,Whea_grow_prid_Spr,Barl_grow_prid_Win,Barl_grow_prid_Spr,\
                       Maiz_grow_prid,Grenmaiz_grow_prid,Tempgras_grow_prid,Legufod_grow_prid,Rapesd_grow_prid,Sunflrsd_grow_prid,\
                           Soya_grow_prid,Oat_grow_prid,Rice_grow_prid,Rye_grow_prid,Pota_grow_prid,Sugbt_grow_prid,\
                               Peabean_grow_prid,Nuts_grow_prid,Fruit_grow_prid,Vegetable_grow_prid,Permgras_grow_prid]


Cropnam_airtemp = ['Whea_Win','Whea_Spr','Bar_Win','Bar_Spr','Maiz','Grenmaiz','Tempgra','Legumfod','Rapesd','Sunflrsd','Soya','Oat','Rice','Rye','Pota',\
    'Sugbt','Peabean','Nuts','Fruit','Vege','Permgras']
Crop_grow_prid_wddt = dict(zip(Cropnam_airtemp,Crop_grow_prid_wdlt))

#%%
#OUTPUT_DATA
### Getting air temperature map for each crop
Air_temp_WhealWin_wdlt = [None] * 12
Air_temp_WheaSpr_wdlt = [None] * 12
Air_temp_BarlWin_wdlt = [None] * 12
Air_temp_BarlSpr_wdlt = [None] * 12
Air_temp_Maiz_wdlt = [None] * 12
Air_temp_Grenmaiz_wdlt = [None] * 12
Air_temp_Tempgras_wdlt = [None] * 12
Air_temp_Legufod_wdlt = [None] * 12
Air_temp_Rapesd_wdlt = [None] * 12
Air_temp_Sunflrsd_wdlt = [None] * 12
Air_temp_Soya_wdlt = [None] * 12
Air_temp_Oat_wdlt = [None] * 12
Air_temp_Rice_wdlt = [None] * 12
Air_temp_Rye_wdlt = [None] * 12
Air_temp_Pota_wdlt = [None] * 12
Air_temp_Sugbt_wdlt = [None] * 12
Air_temp_Peabean_wdlt = [None] * 12
Air_temp_Nuts_wdlt = [None] * 12
Air_temp_Fruit_wdlt = [None] * 12
Air_temp_Vegetable_wdlt = [None] * 12
Air_temp_Permgras_wdlt = [None] * 12

Air_temp_crop_wdlt = [Air_temp_WhealWin_wdlt,Air_temp_WheaSpr_wdlt,Air_temp_BarlWin_wdlt,Air_temp_BarlSpr_wdlt,\
                      Air_temp_Maiz_wdlt,Air_temp_Grenmaiz_wdlt,Air_temp_Tempgras_wdlt,Air_temp_Legufod_wdlt,Air_temp_Rapesd_wdlt,\
                        Air_temp_Sunflrsd_wdlt,Air_temp_Soya_wdlt,Air_temp_Oat_wdlt,Air_temp_Rice_wdlt,\
                      Air_temp_Rye_wdlt,Air_temp_Pota_wdlt,Air_temp_Sugbt_wdlt,Air_temp_Peabean_wdlt,Air_temp_Nuts_wdlt,\
                          Air_temp_Fruit_wdlt,Air_temp_Vegetable_wdlt,Air_temp_Permgras_wdlt]

Air_temp_crop_wddt = dict(zip(Cropnam_airtemp,Air_temp_crop_wdlt))

#%%
### Getting the corresponding air temporature maps for each crop
#### Preliminarily getting the list of air temporature maps for each crop(with none list)
#OUTPUT_DATA
for i in Crop_grow_prid_wddt:
        for j in Crop_grow_prid_wddt[i]:
            Air_temp_crop_wddt[i][j] = Air_temp_wdlt[j]
#### Getting the list of air temporature maps for each crop(without none list)
for i in Air_temp_crop_wddt:
    Air_temp_crop_wddt[i] = [x for x in Air_temp_crop_wddt[i] if x != None] #（removing the none value)


#%%
###Aggregating maps and caculating mean values for each crop 
for i in Air_temp_crop_wddt:
    #OUTPUT_DATA
    Air_temp_aggr = Imp_func.aggregate_ori(Air_temp_crop_wddt[i]) #use aggregate_ori because some grids have negetive temperatures
    Air_temp_mean = Air_temp_aggr / len(Air_temp_crop_wddt[i])
    #OUTPUT_INTE_FILE
    Imp_func.output_ras(r'K:/Default_database/raster/Meteorologic_data/By_crop/Original/' + i +'_Airtemp_monthmean.tif',\
               Air_temp_Jan_wd,'EPSG:4326',Air_temp_mean)
    Imp_func.clip_map(r'K:/Default_database/raster/Meteorologic_data/By_crop/Original_EFTA/'+ i +'_Airtemp_monthmeanEFTA.tif' ,\
        r'K:/Default_database/raster/Meteorologic_data/By_crop/Original/' + i +'_Airtemp_monthmean.tif',Pj_path.EFTA_UK_wd)


#%%
###Interpolate the data in ArCGIS

#%%
### Resampling
#OUTPUT_DATA
Air_temp_cropmap_wddt = Imp_func.dict_name_path(Cropnam_airtemp,\
    Imp_func.glob.glob(r'K:/Default_database/raster/Meteorologic_data/By_crop/Original_EFTA/*_Airtemp_monthmeanEFTA.tif',\
        recursive=False))

# OUTPUT_INTE_FILE
for i in Air_temp_cropmap_wddt:
    Imp_func.gdal.Warp(r'K:/Default_database/raster/Meteorologic_data/By_crop/Resample/Airtemp_monthmean'+i+'_resamp.tif', \
              Air_temp_cropmap_wddt[i],dstSRS='EPSG:4326', xRes=0.08333333333333331483,yRes=0.08333333333333331483,\
                  resampleAlg=Imp_func.gdal.GRA_Bilinear)

###(map size is not 1110*1427 any more, hence we need to cut again)

#%%
#OUTPUT_DATA
### Getting the airtemp by crop for Europe
Air_temp_cropmaprsp_wddt = Imp_func.dict_name_path(Cropnam_airtemp,\
    Imp_func.glob.glob(r'K:/Default_database/raster/Meteorologic_data/By_crop/Resample/*.tif',recursive=False))


# OUTPUT_INTE_FILE
for i in Air_temp_cropmaprsp_wddt:
    Imp_func.clip_map(Pj_path.output_prj_wd + '/Meteorological_data/Airtempmean_by_crop/Airtempmean'+i+'_EFTA.tif',\
             Air_temp_cropmaprsp_wddt[i],Pj_path.EFTA_UK_wd)


#%%
## f(u)
#OUTPUT_DATA
### Getting air speed map for each crop
Windsd_WhealWin_wdlt = [None] * 12
Windsd_WheaSpr_wdlt = [None] * 12
Windsd_BarlWin_wdlt = [None] * 12
Windsd_BarlSpr_wdlt = [None] * 12
Windsd_Maiz_wdlt = [None] * 12
Windsd_Grenmaiz_wdlt = [None] * 12
Windsd_Tempgras_wdlt = [None] * 12
Windsd_Legufod_wdlt = [None] * 12
Windsd_Rapesd_wdlt = [None] * 12
Windsd_Sunflrsd_wdlt = [None] * 12
Windsd_Soya_wdlt = [None] * 12
Windsd_Oat_wdlt = [None] * 12
Windsd_Rice_wdlt = [None] * 12
Windsd_Rye_wdlt = [None] * 12
Windsd_Pota_wdlt = [None] * 12
Windsd_Sugbt_wdlt = [None] * 12
Windsd_Peabean_wdlt = [None] * 12
Windsd_Nuts_wdlt = [None] * 12
Windsd_Fruit_wdlt = [None] * 12
Windsd_Vegetable_wdlt = [None] * 12
Windsd_Permgras_wdlt = [None] * 12

Windsd_crop_wdlt = [Windsd_WhealWin_wdlt,Windsd_WheaSpr_wdlt,Windsd_BarlWin_wdlt,Windsd_BarlSpr_wdlt,\
                    Windsd_Maiz_wdlt,Windsd_Grenmaiz_wdlt,Windsd_Tempgras_wdlt,Windsd_Legufod_wdlt,Windsd_Rapesd_wdlt,\
                        Windsd_Sunflrsd_wdlt,Windsd_Soya_wdlt,Windsd_Oat_wdlt,Windsd_Rice_wdlt,\
                      Windsd_Rye_wdlt,Windsd_Pota_wdlt,Windsd_Sugbt_wdlt,Windsd_Peabean_wdlt,Windsd_Nuts_wdlt,\
                          Windsd_Fruit_wdlt,Windsd_Vegetable_wdlt,Windsd_Permgras_wdlt]

Windsd_crop_wddt = dict(zip(Cropnam_airtemp,Windsd_crop_wdlt))

### Getting the corresponding air speed maps for each crop
#### Preliminarily getting the list of air speed maps for each crop(with none list)
for i in Crop_grow_prid_wddt:
        for j in Crop_grow_prid_wddt[i]:
            Windsd_crop_wddt[i][j] = Wind_speed_wdlt[j]

####  getting the list of air speed maps for each crop(without none list)
for i in Windsd_crop_wddt:
    Windsd_crop_wddt[i] = [x for x in Windsd_crop_wddt[i] if x != None] #（removing the none value)


#%%
###Aggregating windspeed maps and caculating mean values for each crop 
'''for i in Windsd_crop_wddt:
    #OUTPUT_DATA
    Windsd_aggr = Imp_func.aggregate(Windsd_crop_wddt[i])
    Windsd_mean = Windsd_aggr / len(Windsd_crop_wddt[i])
    #OUTPUT_INTE_FILE
    Imp_func.output_ras(r'K:/Default_database/raster/Meteorologic_data/Windsd_by_crop/Original/' + i +'_Windsd_monthmean.tif',\
               Wind_speed_Jan_wd,'EPSG:4326',Windsd_mean)
# long time, need to run 25 minutes. Normally we can skip this'''

#%%
### Resampling wind speed maps
#OUTPUT_DATA
Wind_speedmap_wddt = Imp_func.dict_name_path(Cropnam_airtemp,Imp_func.glob.glob(r'K:/Default_database/raster/Meteorologic_data/Windsd_by_crop/Original/*.tif'))

'''#OUTPUT_INTE_FILE
for i in Wind_speedmap_wddt:
    Imp_func.gdal.Warp(r'K:/Default_database/raster/Meteorologic_data/Windsd_by_crop/Resampled/Windsd_monthmean'+i+'_resamp.tif', \
            Wind_speedmap_wddt[i],dstSRS='EPSG:4326', xRes=0.08333333333333331483,yRes=0.08333333333333331483,\
                resampleAlg=Imp_func.gdal.GRA_Bilinear)
    
# long time, need to run 5 minutes. Normally we can skip this'''

#%%
### Getting the wind speed maps by crop for Europe
#OUTPUT_DATA
Wind_speedmaprsp_wddt = Imp_func.dict_name_path(Cropnam_airtemp,\
    Imp_func.glob.glob(r'K:/Default_database/raster/Meteorologic_data/Windsd_by_crop/Resampled/*.tif'))

#OUTPUT_INTE_FILE
for i in Wind_speedmaprsp_wddt:
    Imp_func.clip_map(Pj_path.output_prj_wd + '/Meteorological_data/Windspmean_by_crop/Windsdmean'+i+'_EFTA.tif',\
             Wind_speedmaprsp_wddt[i],Pj_path.EFTA_UK_wd)


#OUTPUT_DATA
Air_temp_cropmapEFTA_wddt = Imp_func.dict_name_path(Cropnam_airtemp,\
    Imp_func.glob.glob(Pj_path.output_prj_wd + r'/Meteorological_data/Airtempmean_by_crop/*.tif',recursive=False))
Air_temp_cropmapEFTA_wdlt = list(Air_temp_cropmapEFTA_wddt.values()) 

Windsd_cropmapEFTA_wddt = Imp_func.dict_name_path(Cropnam_airtemp,\
     Imp_func.glob.glob(Pj_path.output_prj_wd + r'/Meteorological_data/Windspmean_by_crop/*.tif',recursive=False))
Windsd_cropmapEFTA_wdlt = list(Windsd_cropmapEFTA_wddt.values())

#%%
##f(T) and f(M)
#OUTPUT_DATA
f_TM_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='fert_type_fac') #(get the factors from a sheet)
f_TM_df.iloc[:,4:8] = f_TM_df.iloc[:,4:8].astype(float) #(ensure the data type is float)
## Imp_func.add_field(Pj_path.EFTA_UK_wd,f_TM_df,4,8)


#OUTPUT_INTE_FILE
Imp_func.clip_map(Fertfac_EFTA_wd,Pj_path.output_prj_wd + r'Meteorological_data/fertp_fac_gene.tif',\
    Pj_path.EFTA_UK_wd)
Imp_func.clip_map(Fertmedfac_EFTA_wd,Pj_path.output_prj_wd + r'Meteorological_data/fermd_fac_gene.tif',\
    Pj_path.EFTA_UK_wd)
Imp_func.clip_map(Ferttyfac_EFTArice_wd,Ferttyfac_rice_wd,Pj_path.EFTA_UK_wd)
Imp_func.clip_map(Fertmedfac_EFTArice_wd,Fertmedfac_rice_wd,Pj_path.EFTA_UK_wd)


#%%
#OUTPUT_DATA
f_T = Imp_func.tidy_zero(Fertfac_EFTA_wd)
f_M = Imp_func.tidy_zero(Fertmedfac_EFTA_wd)

f_T_for_rice = Imp_func.tidy_zero(Ferttyfac_EFTArice_wd)
f_M_for_rice = Imp_func.tidy_zero(Fertmedfac_EFTArice_wd)

#（these two factors are derived from E:\工作学习2\Online_work\1.Air_pollution\Air_pollution_database\Database_collection\IFAdata\IFADATA Plant Nutrition query.xlsx)

#%%
## Caclulate the emission factors
#OUTPUT_DATA
for i in Air_temp_cropmapEFTA_wddt:
    Airtemp = Imp_func.rasterio.open(Air_temp_cropmapEFTA_wddt[i]).read(1)
    Winsd = Imp_func.tidy_zero(Windsd_cropmapEFTA_wddt[i])
    if i == 'Rice':
        f_A = 0.0033 * pow(e,0.2233*Airtemp)
        f_u = (0.2737 * Imp_func.np.log(Winsd)) + 1.0605
        f_u[Imp_func.np.isneginf(f_u)] = 0
        f_pH_rice[f_pH_rice==0.0224] = 0
        f_EF = VR_0_for_rice * f_pH_rice * f_A * f_u * f_T_for_rice * f_M_for_rice
    else:
        f_A = 0.179 * pow(e,0.094*Airtemp)    
        f_u = (0.2737 * Imp_func.np.log(Winsd)) + 0.9975
        f_u[Imp_func.np.isneginf(f_u)] = 0
        f_pH[f_pH == 0.0429] = 0
        f_EF = VR_0 * f_pH * f_A * f_u * f_T * f_M
    #OUTPUT_INTE_FILE
    Imp_func.output_ras(Pj_path.output_prj_wd +'Fert_N_EFfac/N_EF_'+i+'.tif',\
        Pj_path.output_prj_wd + 'Fertilizer_use_total/Whea_TferuseEFTA.tif','EPSG:4326',f_EF)

#%%
#OUTPUT_DATA
Crop_NEF_EFTA_wddt = Imp_func.dict_name_path(Cropname,\
    Imp_func.glob.glob(Pj_path.output_prj_wd +'Fert_N_EFfac/N_EF_*.tif'))

Crop_NEF_EFTA_wddt.update({'Whea': 'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Fert_N_EFfac/N_EF_Whea_Win.tif',\
    'Bar': 'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Fert_N_EFfac/N_EF_Bar_Win.tif'})

#%%
# Getting all emissions from Crop
#OUTPUT_DATA
Vital_cropTN_EFTA_wddt = Imp_func.conv_df2dict(Chemfer_df,'OSDCropname','Chemfer_use_map')

# List of new keys
Crop_keys = list(Vital_cropTN_EFTA_wddt.keys())

# Create a new dictionary with replaced keys
Crop_NEF_EFTA_wddt = {Crop_keys[i]: value for i, (_, value) in enumerate(Crop_NEF_EFTA_wddt.items())}


#%%
## execuate the final calculateion
for i in Vital_cropTN_EFTA_wddt:
#OUTPUT_DATA
    N_fert = Imp_func.tidy_zero(Vital_cropTN_EFTA_wddt[i])
    N_NEF = Imp_func.tidy_zero(Crop_NEF_EFTA_wddt[i]) # we just still use the original NEF for rice
    # N_fert = Imp_func.tidy_zero(Pj_path.output_prj_wd + 'Fertilizer_use_total/RiceTferusEFTArsp.tif')
    # N_NEF = Imp_func.tidy_zero(Rice_NEF_newwd)
    Nfert_emi = N_fert * N_NEF
    #OUTPUT_FILE
    Imp_func.output_ras_filtered(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Vital_crops_emissions/'+i+'_fertemiEFTA.tif',\
        Pj_path.Exam_crop_reson_wd,'EPSG:4326',Nfert_emi)


#%%
#----------------------------------------------------output_module----------------------------------------------------
#SUMMARY
## Soil pH summary
Imp_func.zonal_summary(['Ori_pH','Rep_pH'],[r'K:/基础数据/B.数据/HWSD_ORNL/soilph.tif',\
    r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Meteorological_data/Soilph_revise.tif'],\
    Pj_path.EFTA_UK_wd,32,'mean',-999,Pj_path.output_prj_excel_wd+'test_output/Compar_resap_soilpH.xlsx')

#SUMMARY 
## Mean temperature summary
Air_temp_realmean = Imp_func.aggregate_ori(Air_temp_wdlt) / 12
Imp_func.output_ras(r'K:/Default_database/Temperature/Mean_temp.tif',Air_temp_Jan_wd,'EPSG:4326',Air_temp_realmean)
Imp_func.clip_map(Airtemp_meanEFTA_wd,r'K:/Default_database/Temperature/Mean_temp.tif',Pj_path.EFTA_UK_wd)

#%%
#SUMMARY
### Mean crop-specific airtemparature and windspeed
Air_TempWind_name = [item + 'Airtemp' for item in Cropnam_airtemp] + [item + 'Windsp' for item in Cropnam_airtemp]
Air_TempWind_wdlt = Air_temp_cropmapEFTA_wdlt + Windsd_cropmapEFTA_wdlt

Imp_func.zonal_summary(Air_TempWind_name,Air_TempWind_wdlt,\
    Pj_path.EFTA_UK_wd,32,'mean',-999,Pj_path.output_prj_excel_wd + 'test_output/Mean_airwind.xlsx')

#%%
#SUMMARY
## crop-specific EFs
Crop_NEF_EFTA_wdlt = list(Crop_NEF_EFTA_wddt.values())

Imp_func.zonal_summary(Cropname,Crop_NEF_EFTA_wdlt,Pj_path.EFTA_UK_wd,32,'mean',-999,\
    Pj_path.output_prj_excel_wd + 'test_output/Mean_Chemfert_EFs_byprod.xlsx')


#%%
#SUMMARY
## Also convert the units to kg, because we need to aggregate them with other maps(in X_Emission_chek) whose units are kg
Emi_kg_wd = Imp_func.glob.glob(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Vital_crops_emissions/*.tif',recursive=False)
Emi_kg_wddt = Imp_func.dict_name_path(Vital_cropTN_EFTA_wddt.keys(),Emi_kg_wd)

Imp_func.zonal_summary(list(Emi_kg_wddt.keys()),list(Emi_kg_wddt.values()),Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd + 'test_output/Emi_Chemfert_byprod.xlsx')


#%%
#OUTPUT_DATA
## Export important pathways
Chemfer_df = Imp_func.join_dict2df(Chemfer_df,Crop_NEF_EFTA_wddt,'OSDCropname','Chemfer_EFs')
Chemfer_df = Imp_func.join_dict2df(Chemfer_df,Emi_kg_wddt,'OSDCropname','Chemfer_EMI_kg')


#SUMMARY
Imp_func.save_plk(r'../B_Output/A51.pkl',Chemfer_df)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")

'''
## Plotting figures
Blue2Red_colorlist = ['white', '#2B83BA', '#ABDDA4','#FFFFBF', '#FDAE61', '#D7191C']

for i in Emi_kg_wddt:
    Imp_func.plot_formal(Emi_kg_wddt[i],Pj_path.EFTA_UK_wd,(8,10),[1,1],3035,Blue2Red_colorlist,\
        [-0.01,100,500,1500,3000,Imp_func.np.inf])'''
