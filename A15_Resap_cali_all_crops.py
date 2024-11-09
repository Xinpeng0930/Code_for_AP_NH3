'''
This script aims to get all crop maps under our categorization at 0.05d and 0.083d. Also we calibrate them to aglign with FAOSTAT data.

This script can be run automatically. Running time is 207s.
'''

#%%
# import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path


#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
Gras_area_wddt = Imp_func.open_plk(r'../B_Output/A12.pkl') # grasslands areas
Harmo_area_df = Imp_func.open_plk(r'../B_Output/A13.pkl') # Harmonized crops areas
Harmo_area_wddt = Imp_func.conv_df2dict(Harmo_area_df,'Cropname','Harmo_crop_EFTA')
Disaggre_area_wddt = Imp_func.open_plk(r'../B_Output/A14.pkl') # Disaggregated crops areas

CROPGRID_VitlCp_One_wdlt = [Pj_path.Whea_area_EFTA_wd,Pj_path.Barl_area_EFTA_wd,Pj_path.Rapesd_area_EFTA_wd,\
    Pj_path.Sunflrsd_area_EFTA_wd,Pj_path.Soya_area_EFTA_wd,Pj_path.Oats_area_EFTA_wd,Pj_path.Rice_area_EFTA_wd,\
    Pj_path.Rye_area_EFTA_wd,Pj_path.Pota_area_EFTA_wd,Pj_path.Sugbt_area_EFTA_wd] #these maps were already clipped
# Normal crop maps from CROPGRID


#----------------------------------------------------processing_module----------------------------------------------------
#OUTPUT_DATA
## Resample harvested area maps(because original CROPGRIDS is 0.05°*0.05°)
### All map pathways
VitlCp_all_wdlt = CROPGRID_VitlCp_One_wdlt + list(Disaggre_area_wddt.values()) \
    + list(Harmo_area_wddt.values()) + \
    [Gras_area_wddt['Temp_gras']] + [Gras_area_wddt['Perm_gras']]

VitlCp_name = ['Whea','Barl','Rapesd','Sunflrsd','Soya','Oats','Rice','Rye',
               'Pota','Sugbt','Grenmaiz','Maiz','Legumfod','Peabean','Fruit','Nuts',\
                'Vege','Tempgra','Permgra']

VitlCp_all_wddt = dict(zip(VitlCp_name,VitlCp_all_wdlt))
VitlCp_all_wddt = Imp_func.sort_dict_by_order(VitlCp_all_wddt,Pj_path.MainCpNam)

#%%
# OUTPUT_INTE_FILE
for i in VitlCp_all_wddt:
    Imp_func.gdal.Warp(Pj_path.output_prj_wd + 'Vital_crops/Vital_Cp_resample/' + i + '_resap.tif',\
        VitlCp_all_wddt[i],dstSRS='EPSG:4326',\
        xRes = 0.08333333333333331483, yRes = 0.08333333333333331483,\
        resampleAlg = Imp_func.gdal.GRA_Sum)


#%%
#OUTPUT_DATA
VitlCp_Resp_wddt = Imp_func.dict_name_path(Pj_path.MainCpNam,\
    Imp_func.glob.glob(Pj_path.output_prj_wd + 'Vital_crops/Vital_Cp_resample/*.tif'))

#%%
# OUTPUT_INTE_FILE
Imp_func.zonal_summary(list(VitlCp_Resp_wddt.keys()),list(VitlCp_Resp_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,\
    'sum',-999,Pj_path.output_prj_excel_wd + 'test_output/Resap_Croparea_by_prod.xlsx')

#%%
## Calibrate the resampled maps with FAOSTAT data.
Crop_cali_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='crop_adjust')

# OUTPUT_FILE
for i in VitlCp_Resp_wddt:
    Imp_func.cali_fig_filter(VitlCp_Resp_wddt[i],Pj_path.Exam_crop_wd,Pj_path.EFTA_UK_wd,\
        Crop_cali_df,'FID_1','abb',Crop_cali_df.columns.tolist()[list(VitlCp_Resp_wddt.keys()).index(i)+3],\
        0.0833333333333333,\
        Pj_path.output_prj_wd+r'Vital_crops/Vital_Cp_cali/'+i+'_EFTA_cali.tif')

# OUTPUT_DATA
Crop_cali_wddt =Imp_func.dict_name_path(Pj_path.MainCpNam,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Vital_crops/Vital_Cp_cali/*_EFTA_cali.tif',recursive=False))

# OUTPUT_INTE_FILE
Imp_func.zonal_summary(list(Crop_cali_wddt.keys()),list(Crop_cali_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd + 'test_output/Croparea.xlsx')


#%%
## calculate total agricultural area
# OUTPUT_DATA
All_croparea_wdlt = list(Crop_cali_wddt.values())
All_agri_area = Imp_func.aggregate(All_croparea_wdlt)
All_agri_area_reson = Imp_func.np.where((All_agri_area > 50),All_agri_area,-999)


#OUTPUT_FILE
Imp_func.output_ras_filtered(Pj_path.output_prj_wd + r'All_croparea/All_agri_area_reson.tif',\
    Pj_path.Exam_crop_wd,\
    'EPSG:4326',All_agri_area_reson)
# Now the new example figure is Pj_path.Exam_crop_reson_wd

#%%
### Output maps excluding small agriculture areas

# OUTPUT_FILE
for i in Crop_cali_wddt:
    Crop_cali_ori = Imp_func.rasterio.open(Crop_cali_wddt[i]).read(1)
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+r'Vital_crops/Vital_Cp_cali2/'+i+'_EFTA_cali_nosml.tif',
                                 Pj_path.Exam_crop_reson_wd,'EPSG:4326',Crop_cali_ori)



#----------------------------------------------------output_module----------------------------------------------------
# OUTPUT_DATA
Crop_calinosml_wddt =Imp_func.dict_name_path(Pj_path.MainCpNam,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Vital_crops/Vital_Cp_cali2/*_EFTA_cali_nosml.tif',recursive=False))

# OUTPUT_INTE_FILE
Imp_func.zonal_summary(list(Crop_calinosml_wddt.keys()),list(Crop_calinosml_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd + 'test_output/Croparea_calinosml.xlsx')
#we found we don't have to calibrate twice, since the results after removing small areas didn't change a lot


#%%
# OUTPUT_FILE
OSD_vital_cropdf = Imp_func.conv_dict2df(VitlCp_all_wddt,'Cropname','Ori_0.05cropmaps')
OSD_vital_cropdf = Imp_func.join_dict2df(OSD_vital_cropdf,Crop_calinosml_wddt,'Cropname',\
    'Final_cropmaps')

J20 = OSD_vital_cropdf

with open('../B_Output/J20.pkl', 'wb') as f:
    Imp_func.pickle.dump(J20, f)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")