'''
This script aims to get emissions from manure deposited on grassland
This script can be run automatically. Running time is 23s.
'''


#%%
#Environment: Air_pollu_datproc1 based on anaconda
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path


#%%
#set directories
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
H83 = Imp_func.open_plk(r'../B_Output/H83.pkl')
PU_graz_wddt = Imp_func.conv_df2dict(H83,'Anim_name','PU_graz_cali1')
MO_graz_wddt = Imp_func.conv_df2dict(H83,'Anim_name','Rev_grazMO_final')


#%%
# Processing data
#----------------------------------------------------processing_module----------------------------------------------------
## Get integrated grazing animals
# OUTPUT_FILE
for i in PU_graz_wddt:
    Graz_all = Imp_func.tidy_zero(PU_graz_wddt[i]) + \
        Imp_func.tidy_zero(MO_graz_wddt[i])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + 'Graz_inte_MO_PU/'+i+'_CombGraz.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',Graz_all)

## Get the manure N deposited on grassland
# OUTPUT_DATA
Excre_fac = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Excre_fac')
del Excre_fac['Pig N excretion parameters(kg N animal-1 yr-1)']
del Excre_fac['Poultry N excretion parameters(kg N animal-1 yr-1)']

Graz_PUMO_wddt = Imp_func.dict_name_path(list(MO_graz_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd + r'Graz_inte_MO_PU/*_CombGraz.tif',recursive=False))


# OUTPUT_FILE
for i in Graz_PUMO_wddt:
    Imp_func.cali_fig_filter(Graz_PUMO_wddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,\
        Excre_fac,'FID_1','Name_abbre',\
        Excre_fac.columns.tolist()[list(Graz_PUMO_wddt.keys()).index(i)+1],\
        0.0833333333333333,Pj_path.output_prj_wd+'Graz_excre/'+i+'_graz_excr.tif')


#%%
## Get emissions from manure depositions on grassland 
# OUTPUT_DATA
Graz_EF_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='graz_depo_EFs')

Graz_PUMO_grazexcr_wddt = Imp_func.dict_name_path(list(MO_graz_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Graz_excre/*_graz_excr.tif',recursive=False))

# OUTPUT_FILE
for i in Graz_PUMO_grazexcr_wddt:
    Imp_func.cali_fig_filter(Graz_PUMO_grazexcr_wddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,\
        Graz_EF_df,'FID_1','Name_abbre',\
        Graz_EF_df.columns.tolist()[list(Graz_PUMO_grazexcr_wddt.keys()).index(i)+11],\
        0.0833333333333333,Pj_path.output_prj_wd+'Graz_excr_emi/'+i+'_graz_depoemi.tif')


#----------------------------------------------------output_module----------------------------------------------------
# OUTPUT_DATA
## Summarize emissions from manure deposition on grassland
Graz_PUMO_grazexcr_emi_wddt = Imp_func.dict_name_path(list(MO_graz_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Graz_excr_emi/*_graz_depoemi.tif',recursive=False))

# SUMMARY
Imp_func.zonal_summary(list(Graz_PUMO_grazexcr_emi_wddt.keys()),list(Graz_PUMO_grazexcr_emi_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/PUMO_grazemi.xlsx')

## Summarize all manure deposisted on grazing areas
# SUMMARY
Imp_func.zonal_summary(list(Graz_PUMO_grazexcr_wddt.keys()),list(Graz_PUMO_grazexcr_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+r'test_output/Manr_depoN_bylivstk.xlsx')


## Summarize important pathways
Graz_emi_df = Imp_func.conv_dict2df(Graz_PUMO_wddt,'Anim_name','Graz_Animnumb_PUMO')
Graz_emi_df = Imp_func.join_dict2df(Graz_emi_df,Graz_PUMO_grazexcr_wddt,'Anim_name','Graz_ExcrN')
Graz_emi_df = Imp_func.join_dict2df(Graz_emi_df,Graz_PUMO_grazexcr_emi_wddt,'Anim_name','Graz_depo_emi')

Imp_func.save_plk(r'../B_Output/H87.pkl',Graz_emi_df)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")



'''
### Extra test (not important)
Tot_extre_N = Imp_func.aggregate(list(Graz_PUMO_grazexcr_wddt.values()))
Imp_func.output_ras_filtered(Pj_path.output_wd+'test.tif',Pj_path.Exam_crop_reson_wd,'EPSG:4326',Tot_extre_N)

Crop_cali_wddt =Imp_func.dict_name_path(Pj_path.MainCpNam,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Vital_crops/Vital_Cp_cali/*_EFTA_cali.tif',recursive=False))
Gras_land_wd = [Crop_cali_wddt['Permgra'],Crop_cali_wddt['Tempgra']] 
Tot_gras_land = Imp_func.aggregate(Gras_land_wd )
Imp_func.output_ras_filtered(Pj_path.output_wd+'test1.tif',Pj_path.Exam_crop_reson_wd,'EPSG:4326',Tot_gras_land)

'''
