'''
This script aims to rescale the original GLW4.0 maps to align to data in FAOSTAT
This script can be run automatically in the interactive interface. Running time: 63s
'''


#%%
#Necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
#Set directories

Ani_numb_raw_wddt = {'pig':r'K:/基础数据/B.数据/畜禽分布数据/GLW4.0/5_Pg_2015_Da.tif',
                     'catl':r'K:/基础数据/B.数据/畜禽分布数据/GLW4.0/5_Ct_2015_Da.tif',\
                     'shep':r'K:/基础数据/B.数据/畜禽分布数据/GLW4.0/5_Sh_2015_Da.tif',\
                     'goat':r'K:/基础数据/B.数据/畜禽分布数据/GLW4.0/5_Gt_2015_Da.tif',\
                         'chicken':r'K:/基础数据/B.数据/畜禽分布数据/GLW4.0/5_Ch_2015_Da.tif',
                         'duck':r'K:/基础数据/B.数据/畜禽分布数据/GLW4.0/5_Dk_2015_Da.tif'}

## agricultural area data (prepare for identifying low agricultural areas)
Pysi_area_EFTA_wd = Pj_path.output_prj_wd + r'CG_phytot_EFTA.tif'
Temp_gras_EFTA_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Vital_crops/Vital_Cp_resample/Tempgra_resap.tif'
Perm_gras_EFTA_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Vital_crops/Vital_Cp_resample/Permgra_resap.tif'


#%%
#----------------------------------------------------processing_module----------------------------------------------------
#start to process data
## get the original animal numbers in EEA areas
### firstly, filter the original maps to convert negative values to zero. This helps to count animal numbers correctly
# OUTPUT_INTE_FILE
for i in Ani_numb_raw_wddt:
    Ani_numb_filtered = Imp_func.tidy_zero(Ani_numb_raw_wddt[i])
    Imp_func.output_ras(r'K:/基础数据/B.数据/畜禽分布数据/GLW4.0/Ani_numb_filtered/'+i+'_numb_fltred.tif',\
        Ani_numb_raw_wddt[i],'EPSG:4326',Ani_numb_filtered)

### Secondly clip the maps
#OUTPUT_DATA
Ani_numb_filtered_wddt = Imp_func.dict_name_path(list(Ani_numb_raw_wddt.keys()),\
    Imp_func.glob.glob(r'K:/基础数据/B.数据/畜禽分布数据/GLW4.0/Ani_numb_filtered/*.tif',recursive=False))

# OUTPUT_INTE_FILE
for i in Ani_numb_filtered_wddt:
    Imp_func.clip_map(Pj_path.output_prj_wd+r'Anim_numb/'+i+'_numb.tif',\
        Ani_numb_filtered_wddt[i],Pj_path.EFTA_UK_wd)

### Thirdly, remove grids with small agricultural land, as well as combine duck and chicken
#OUTPUT_DATA
Anim_numb_EFTA_wddt = Imp_func.dict_name_path(list(Ani_numb_raw_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Anim_numb/*.tif',recursive=False))

Agri_area = Imp_func.tidy_zero(Pysi_area_EFTA_wd) + Imp_func.tidy_zero(Temp_gras_EFTA_wd) + \
    Imp_func.tidy_zero(Perm_gras_EFTA_wd)


# OUTPUT_FILE
for i in ['pig','catl','shep','goat']:
    Anim_num1 = Imp_func.rasterio.open(Anim_numb_EFTA_wddt[i]).read(1)
    Anim_num2 = Imp_func.np.where((Agri_area > 50),Anim_num1,-999)
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_numb_reson/'+i+'_reson.tif',\
        Pj_path.Exam_wd,'EPSG:4326',Anim_num2)

Poultr_numb = Imp_func.aggregate([Anim_numb_EFTA_wddt['chicken'],Anim_numb_EFTA_wddt['duck']])
Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_numb_reson/potr_reson.tif',\
    Pj_path.Exam_new_wd,'EPSG:4326',Poultr_numb)


#%%
## execuate the calibration
### get the dictionary of the maps
# OUTPUT_DATA
Anim_numb_resonEFTA_wddt = Imp_func.dict_name_path(['pig','catl','shep','goat','potr'],\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Anim_numb_reson/*_reson.tif',recursive=False))

### get the calibration dataframe
Ani_cali_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Ani_cali')

### run the code for calibration
# OUTPUT_FILE
for i in Anim_numb_resonEFTA_wddt:
    Imp_func.cali_fig_filter(Anim_numb_resonEFTA_wddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,Ani_cali_df, \
    'FID_1','Name_abbre',Ani_cali_df.columns.tolist()[list(Anim_numb_resonEFTA_wddt.keys()).index(i) + 1],\
    0.0833333333333333,Pj_path.output_prj_wd + 'Anim_numb_cali/' + i +'_numbcali.tif')

### generate the corresponding dictionary for summary
# OUTPUT_DATA
Anim_numb_cali_wddt = Imp_func.dict_name_path(['pig','catl','shep','goat','potr'],\
    Imp_func.glob.glob(Pj_path.output_prj_wd + 'Anim_numb_cali/*_numbcali.tif',recursive=False))


#%%
#----------------------------------------------------output_module----------------------------------------------------
##Summarize animal number before calibration but with filtering small agriculatural areas
# SUMMARY
Imp_func.zonal_summary(list(Anim_numb_resonEFTA_wddt.keys()),\
    list(Anim_numb_resonEFTA_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/AnimNUM.xlsx')

## Summarize animal number after calibration
# SUMMARY
Imp_func.zonal_summary(list(Anim_numb_cali_wddt.keys()),list(Anim_numb_cali_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/AnimNUM_cali.xlsx')

## Summarize important map pathways
# SUMMARY
Ani_numb_df = Imp_func.conv_dict2df(Anim_numb_resonEFTA_wddt,'Anim_type','Numb_before_cali')
Ani_numb_df = Imp_func.join_dict2df(Ani_numb_df,Anim_numb_cali_wddt,'Anim_type','Numb_after_cali')

Imp_func.save_plk(r'../B_Output/G75.pkl',Ani_numb_df)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")