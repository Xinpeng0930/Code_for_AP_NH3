'''
This script is aimming to get several disaggregated maps for analyzing. 
For instance, grassland, fodder crops, maize, green maize

This script can be run automatically. Running time is 148s.
'''

#%%
# import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path


#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
# setting directories
## directory of vital crops
Cropall_wd = r'K:/基础数据/A.数据/Crop_Grids_DB/CROPGRIDS_maps_convt/Crop_harvest/'
Othfod_area_wd = r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/Fodder/fodder_new.tif'
Maiz_area_wd = r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/Maize/Maize_new.tif'

LUCAS_disaggre_crop_wddt = {'Fodder':Othfod_area_wd,'Maize':Maiz_area_wd}

#%%
#----------------------------------------------------processing_module----------------------------------------------------
## obtainging new legume and maize map
### convert unit and resample raw maps
# OUTPUT_FILE
for i in LUCAS_disaggre_crop_wddt:
    #### convert to correct unit
    Convtunit_data = 0.01 * Imp_func.rasterio.open(LUCAS_disaggre_crop_wddt[i]).read(1) #(to have a correct unit of ha)
    Imp_func.output_ras(r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/'+i+'/'+i+'_area_map/LUCAS_'+i+'_Mosaic_Unitrev.tif',\
           LUCAS_disaggre_crop_wddt[i],'EPSG:3035',Convtunit_data)
    Convtunit_file = Imp_func.gdal.Open(r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/'+i+'/'+i+'_area_map/LUCAS_'+i+'_Mosaic_Unitrev.tif')
    #### resample to 0.05 degrees
    Imp_func.gdal.Warp(r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/'+i+'/'+i+'_area_map/LUCAS_'+i+'_Mosaictrans.tif',
                       Convtunit_file, dstSRS= 'EPSG:4326', xRes = 0.05, yRes = 0.05, resampleAlg = Imp_func.gdal.GRA_Sum)
    #### clip to the extent of Europe
    Imp_func.clip_map(r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/'+i+'/'+i+'_area_map/LUCAS_'+i+'_Mosaictrans_clip.tif',\
         r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/'+i+'/'+i+'_area_map/LUCAS_'+i+'_Mosaictrans.tif',\
         Pj_path.EFTA_UK_wd)

# OUTPUT_DATA
LUCAS_disaggre_cropnew_wddt = {'Fodder':r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/Fodder/Fodder_area_map/LUCAS_Fodder_Mosaictrans_clip.tif',\
       'Maize':r'K:/基础数据/A.数据/LUCAS_dataset/LUCAS_result/Maize/Maize_area_map/LUCAS_Maize_Mosaictrans_clip.tif'}

### Extract green maize, grain maize and legume fodders
# OUTPUT_DATA
Maiz_fac_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='greenmaize_shares')
Legum_fac_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='legume_shares')

# OUTPUT_FILE
Imp_func.cali_fig(LUCAS_disaggre_cropnew_wddt['Fodder'],\
       Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Fruit_EFTA.tif',\
       Pj_path.EFTA_NUT2_wd,Legum_fac_df,'NUTS_ID','NUTS2_ID','SH',0.05,\
       Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Legufod_EFTA.tif')


# OUTPUT_FILE
Imp_func.cali_fig(LUCAS_disaggre_cropnew_wddt['Maize'],\
       Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Fruit_EFTA.tif',\
       Pj_path.EFTA_NUT2_wd,Maiz_fac_df,'NUTS_ID','NUTS2_ID','Sh_gremaiz',0.05,\
       Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Grenmaiz_EFTA.tif')


# OUTPUT_FILE
Imp_func.cali_fig(LUCAS_disaggre_cropnew_wddt['Maize'],\
       Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Fruit_EFTA.tif',\
       Pj_path.EFTA_NUT2_wd,Maiz_fac_df,'NUTS_ID','NUTS2_ID','Sh_gramaiz',0.05,\
       Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Granmaiz_EFTA.tif')

#%%
#----------------------------------------------------output_module----------------------------------------------------
## Summarize areas of maize and other fodders
# SUMMARY
Imp_func.zonal_summary(list(LUCAS_disaggre_cropnew_wddt.keys()),list(LUCAS_disaggre_cropnew_wddt.values()),\
       Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/LUCAS_Fodder_Maiz.xlsx')

# passed the test after checking data in the LUCAS paper.

## Summarize areas of other fodders at the NUTS2 level
# SUMMARY
Imp_func.zonal_summary(['Fodder','Maize'],\
       [LUCAS_disaggre_cropnew_wddt['Fodder'],LUCAS_disaggre_cropnew_wddt['Maize']],\
       Pj_path.EFTA_NUT2_wd,295,\
       'sum',-999,Pj_path.output_prj_excel_wd+'test_output/LUCAS_Maize_Fodder_NUTS2.xlsx')

## Summarize areas of green maize and grain maize(don't have to be consistent with total maize, but the ratio between green maize and grain maize should be correct)
# SUMMARY
Imp_func.zonal_summary(['Maize','Green maize','Grain maize'],\
       [LUCAS_disaggre_cropnew_wddt['Maize'],Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Grenmaiz_EFTA.tif',\
       Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Granmaiz_EFTA.tif'],\
       Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/Maize_green_grain.xlsx')

## Summarize important pathways
# SUMMARY
Maiz_fodder_wddt = {'Grenmaiz':Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Grenmaiz_EFTA.tif',\
       'Granmaiz':Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Granmaiz_EFTA.tif',\
       'Legufod':Pj_path.Input_prj_wd + r'Air_polu_prj/Vital_crops/Vital_Cp_area/Legufod_EFTA.tif'}

Imp_func.save_plk(r'../B_Output/A14.pkl',Maiz_fodder_wddt)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
