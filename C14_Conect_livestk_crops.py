#%%
'''
This script is used to identify manure types on each type of cropland

Step1: get the share of each type manure to total manure
Step2: multiply the shares with manure on each crop areas
Step3: multiply manure N with corresponding emission factors

This script could be run automatically
Running time is 21min 40s for scenario one, 10min for scenario two.
'''

#%%
# Import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%% 
start_time = Imp_func.time.time()
Manradj_opt = 2

#----------------------------------------------------input_module----------------------------------------------------
# Inputs general---------------------------------------------------------------------
## manure application by animal and by land (only distinguising cropland and grassland)
I10B_dict = Imp_func.open_plk(r'../B_Output/I10B.pkl') # this dictionary is from I11Br1A -> I10Br1A
Manr_byani_df = I10B_dict['Manrapp_byani'] 

### Manure on cropland by animal type (based on proportions to lands from Einarson et al)
Animanr_cropapp_wddt = Imp_func.conv_df2dict(Manr_byani_df,'Ani_manr_type','Crop_app_maps')
Animanr_cropapp_wddt = Imp_func.dict_del_nan(Animanr_cropapp_wddt)

### Manure applied and deposited on grassland by animal type (based on proportions to lands from Einarson et al)
Animanr_grasapp_wddt = Imp_func.conv_df2dict(Manr_byani_df,'Ani_manr_type','Grass_app_maps')
Animanr_grasdepo_wddt = Imp_func.filter_dict(Animanr_grasapp_wddt,['dair_graz','othcatl_graz','shep_graz','goat_graz'])
Animanr_grasapp_wddt = Imp_func.del_keys_dict(Animanr_grasapp_wddt,['dair_graz','othcatl_graz','shep_graz','goat_graz'])

### collect the emission factors by animal
pig_solidapp_emifac = 0.45
dair_solidapp_emifac = 0.68
othcatl_solidapp_emifac = 0.68
shep_solidapp_emifac = 0.9
goat_solidapp_emifac = 0.9
potr_solidapp_emifac = 0.43

#pig_liqapp_emifac = 0.35 #eea 2019 data
pig_liqapp_emifac = 0.18
# dair_liqapp_emifac = 0.55 #eea 2019 data
# othcatl_liqapp_emifac = 0.55 #eea 2019 data
dair_liqapp_emifac = 0.25
othcatl_liqapp_emifac = 0.25
shep_liqapp_emifac = 0.9
goat_liqapp_emifac = 0.9
potr_liqapp_emifac = 0.69

App_emifac_wdlt = [pig_solidapp_emifac,pig_liqapp_emifac,dair_solidapp_emifac,dair_liqapp_emifac,othcatl_solidapp_emifac,\
    othcatl_liqapp_emifac,potr_solidapp_emifac,potr_liqapp_emifac,shep_solidapp_emifac,shep_liqapp_emifac,\
        goat_solidapp_emifac,goat_liqapp_emifac]

App_emifac_wddt = dict(zip(list(Animanr_grasapp_wddt.keys()),App_emifac_wdlt))

### manure application efs by crop
I13B_dict = Imp_func.open_plk(r'../B_Output/I13B.pkl') 
Crop_manrapp_emifac_wddt = Imp_func.replace_keys(I13B_dict,['Whea', 'Barl', 'Maiz', \
    'Grenmaiz', 'Tempgra', 'Legumfod', 'Rapesd', 'Sunflrsd', 'Soya', 'Oats', 'Rice', \
        'Rye', 'Pota', 'Sugbt', 'Peabean', 'Nuts', 'Fruit', 'Vege', 'Permgra'])

### Get deposition emission factors
Graz_EF_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='graz_depo_EFs')

## get the ratios between applied manure N and applied TAN
H89_dict = Imp_func.open_plk(r'../B_Output/H89.pkl') 
App_manr_RatioTAN = Imp_func.conv_df2dict(H89_dict['Manr_app_df'],'Ani_manr_type','Ratio_TAN')


# Inputs and outputs based on different strategies
if Manradj_opt == 1:
    ## provides manure application by specific crops with the consideration of application limits
    I12_dt = Imp_func.open_plk(r'../B_Output/I12A.pkl') 
    Manrapp_by_cropdf =  I12_dt['Vital_manr_appland']
    ## get manure application by specific crops
    Manr_appli_onagri_wddt = Imp_func.conv_df2dict(Manrapp_by_cropdf,'Cropname','Manr_appl_DI')
    Manr_appli_ongras_wddt = Imp_func.filter_dict(Manr_appli_onagri_wddt,['Tempgra','Permgra'])
    Manr_appli_oncrop_wddt =  Imp_func.deepcopy(Manr_appli_onagri_wddt)
    Manr_appli_oncrop_wddt = Imp_func.del_keys_dict(Manr_appli_oncrop_wddt,['Tempgra','Permgra'])
    ##provides manure deposition by specific crops
    I12_depo_df = Imp_func.open_plk(r'../B_Output/I12.pkl') 
    Manr_depo_onagri_wddt = Imp_func.conv_df2dict(I12_depo_df,'Cropname','Manr_depoN_by_plant')
    
    ##define output folders of connected specific livestock-crop manure
    Fold_path_spc_livstkcrop_manr = 'Connect_manre_N/'
    Fold_path_spc_livstkgras_manr = 'Connect_manre_N_gras_app/'
    Fold_path_spc_livstkcropgras_manrdepo = 'Connect_manre_N_depo/'
    Fold_path_spc_livstkcrop_manrEMI = 'Connect_Manr_Emi/'
    Fold_path_spc_livstkcrop_manrdepoEMI = 'Connect_Manr_Depo_Emi/'
    Fold_path_spc_livstkcrop_manrEMI_bycrop = 'Manr_App_Emi_bycrop/'
    Excel_name_spc_livstkcrop_manr = 'Connect_CropAniManrN.xlsx'
    Excel_name_spc_livstkgras_manr = 'Connect_GrasAniManrappN.xlsx'
    Excel_name_spc_livstkcropgras_manrdepo =  'Connect_GrasAniManrdepoN.xlsx'
    Excel_name_spc_livstkcrop_manrEMI = 'Emi_Connect_CropAniManr.xlsx'
    Excel_name_spc_livstkcrop_manrEMI_bycrop ='Emi_manrappN_bycrop.xlsx'
    Excel_name_spc_livstkcrop_manrdepoEMI = 'Emi_Connect_AniManrdepo.xlsx'
    Pickle_name_output = 'I14.pkl'
elif Manradj_opt==2:
    ## provides manure application by specific crops with no consideration of application limits
    Manrapp_realDI_df = Imp_func.open_plk(r'../B_Output/I11Br1B.pkl')
    ## get manure application by specific crops
    Manr_appli_onagri_wddt = Imp_func.conv_df2dict(Manrapp_realDI_df,'Cropname','Manr_appl_DI')
    Manr_appli_onagri_wddt = Imp_func.dict_del_nan(Manr_appli_onagri_wddt)
    Manr_appli_ongras_wddt = Imp_func.filter_dict(Manr_appli_onagri_wddt,['Tempgra','Permgra'])
    Manr_appli_oncrop_wddt =  Imp_func.deepcopy(Manr_appli_onagri_wddt)
    Manr_appli_oncrop_wddt = Imp_func.del_keys_dict(Manr_appli_oncrop_wddt,['Tempgra','Permgra'])   
    ##provides manure deposition by specific crops
    Depo_bygras_realDI_df = Imp_func.open_plk(r'../B_Output/I10Br1B.pkl')
    Manr_depo_onagri_wddt = Imp_func.conv_df2dict(Depo_bygras_realDI_df,'Cropname','Manr_depoN_by_plant')
    
    ##define output folders of connected specific livestock-crop manure
    Fold_path_spc_livstkcrop_manr = 'Connect_manre_N_realDI/'
    Fold_path_spc_livstkgras_manr = 'Connect_manre_N_gras_app_realDI/'
    Fold_path_spc_livstkcropgras_manrdepo = 'Connect_manre_N_depo_realDI/'
    Fold_path_spc_livstkcrop_manrEMI = 'Connect_Manr_Emi_realDI/'
    Fold_path_spc_livstkcrop_manrdepoEMI = 'Connect_Manr_Depo_Emi_realDI/'
    Fold_path_spc_livstkcrop_manrEMI_bycrop = 'Manr_App_Emi_bycrop_realDI/'
    Excel_name_spc_livstkcrop_manr = 'Connect_CropAniManrN_readDI.xlsx'
    Excel_name_spc_livstkgras_manr = 'Connect_GrasAniManrappN_readDI.xlsx'
    Excel_name_spc_livstkcropgras_manrdepo =  'Connect_GrasAniManrdepoN_readDI.xlsx'
    Excel_name_spc_livstkcrop_manrEMI = 'Emi_Connect_CropAniManr_readDI.xlsx'
    Excel_name_spc_livstkcrop_manrEMI_bycrop ='Emi_manrappN_bycrop_readDI.xlsx'
    Excel_name_spc_livstkcrop_manrdepoEMI = 'Emi_Connect_AniManrdepo_readDI.xlsx'
    Pickle_name_output = 'I15Br1B.pkl'    
else:    
    print('We do not have the scenario yet.')




#----------------------------------------------------Processing_module----------------------------------------------------

All_animanr_cropapp_value = Imp_func.aggregate(list(Animanr_cropapp_wddt.values()))
All_animanr_grasapp_value = Imp_func.aggregate(list(Animanr_grasapp_wddt.values()))
All_animanr_grasdepo_value = Imp_func.aggregate(list(Animanr_grasdepo_wddt.values()))

## Connecting animal_manure_type with crop_type
## (use the proportions of individual animal manure to total manure to time total manure on individual crops)
#OUTPUT_FILE
for i in Animanr_cropapp_wddt:
    for j in Manr_appli_oncrop_wddt:
        Anim_manr_sys_shar = Imp_func.tidy_zero(Animanr_cropapp_wddt[i])/All_animanr_cropapp_value
        Anim_manr_sys_shar[Imp_func.np.isnan(Anim_manr_sys_shar)]=0
        Animanr_con_crop = Imp_func.tidy_zero(Manr_appli_oncrop_wddt[j]) * Anim_manr_sys_shar
        Imp_func.output_ras_filtered(Pj_path.output_prj_wd + Fold_path_spc_livstkcrop_manr + j+'_'+i+'_manrNapp.tif',\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',Animanr_con_crop)


# OUTPUT_DATA
CropAniManrapp_N_wdlt = Imp_func.glob.glob(Pj_path.output_prj_wd + Fold_path_spc_livstkcrop_manr +'*.tif',recursive=False)

CropAniManrappN_name = []
for path in CropAniManrapp_N_wdlt:
    filename = path.split('\\')[-1]
    result='_'.join(filename.split('_')[:3])
    CropAniManrappN_name.append(result)

CropAniManrapp_N_wddt = Imp_func.dict_name_path(CropAniManrappN_name,CropAniManrapp_N_wdlt)


## connect manure applied on grassland 
# OUTPUT_FILE

for i in Animanr_grasapp_wddt:
    for j in Manr_appli_ongras_wddt:
        Anim_manr_sys_shar = Imp_func.tidy_zero(Animanr_grasapp_wddt[i])/All_animanr_grasapp_value
        Anim_manr_sys_shar[Imp_func.np.isnan(Anim_manr_sys_shar)]=0
        Animanr_con_gras = Imp_func.tidy_zero(Manr_appli_ongras_wddt[j]) * Anim_manr_sys_shar
        Imp_func.output_ras_filtered(Pj_path.output_prj_wd + Fold_path_spc_livstkgras_manr + j+'_'+i+'_manrNapp.tif',\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',Animanr_con_gras)


#OUTPUT_DATA
GrasAniManrapp_N_wdlt = Imp_func.glob.glob(Pj_path.output_prj_wd + Fold_path_spc_livstkgras_manr +'*_manrNapp.tif',\
    recursive=False)

GrasAniManrappN_name = []
for path in GrasAniManrapp_N_wdlt:
    filename = path.split('\\')[-1]
    result='_'.join(filename.split('_')[:3])
    GrasAniManrappN_name.append(result)

GrasAniManrapp_N_wddt=Imp_func.dict_name_path(GrasAniManrappN_name,GrasAniManrapp_N_wdlt)


#%%
### connect manure deposited on agricultural land
# OUTPUT_FILE

for i in Animanr_grasdepo_wddt:
    for j in Manr_depo_onagri_wddt:
        Anim_manr_deposys_shar = Imp_func.tidy_zero(Animanr_grasdepo_wddt[i])/All_animanr_grasdepo_value 
        Anim_manr_deposys_shar[Imp_func.np.isnan(Anim_manr_deposys_shar)] = 0
        Animanr_con_depo = Imp_func.tidy_zero(Manr_depo_onagri_wddt[j]) * Anim_manr_deposys_shar
        Imp_func.output_ras_filtered(Pj_path.output_prj_wd+Fold_path_spc_livstkcropgras_manrdepo + j+'_'+i+'_manrNdepo.tif',\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',Animanr_con_depo)

AniManrdepo_N_wdlt = Imp_func.glob.glob(Pj_path.output_prj_wd+Fold_path_spc_livstkcropgras_manrdepo+'*.tif',recursive=False) 

AniManrdepoN_name = []
for path in AniManrdepo_N_wdlt:
    filename = path.split('\\')[-1]
    result='_'.join(filename.split('_')[:3])
    AniManrdepoN_name.append(result)

# OUTPUT_DATA
AniManrdepo_N_wddt=Imp_func.dict_name_path(AniManrdepoN_name,AniManrdepo_N_wdlt) 



#%%
# OUTPUT_DATA
## generate multi-layer lists for manure applied on crops. Outlayer is livestock-manure type.
Connect_listkcrop_manr_app = {}
Connect_listkgras_manr_app = {}

for i in App_emifac_wddt:
    Connect_listkcrop_manr_app[i]= {}
    Connect_listkgras_manr_app[i]= {}
    Connect_listkcrop_manr_app[i] = Imp_func.dict_name_path(list(Manr_appli_oncrop_wddt.keys()),\
            Imp_func.glob.glob(Pj_path.output_prj_wd+Fold_path_spc_livstkcrop_manr+'*_'+ i + r'_*.tif',\
                recursive = False))
    Connect_listkgras_manr_app[i] =  Imp_func.dict_name_path(list(Manr_appli_ongras_wddt.keys()),\
            Imp_func.glob.glob(Pj_path.output_prj_wd + Fold_path_spc_livstkgras_manr+'*_'+i+r'_*.tif',\
                recursive=False))
    
Connect_listkcrop_manr_app = {k: v for k, v in Connect_listkcrop_manr_app.items() if v != {}}

## generate multi-layer lists for manure applied on crops. Outlayer is crop types
### don't have to do. Because we already had them from Manr_appli_onagri_wddt 


## generate multi-layer lists for manure deposited on agricultural land. Outlayer is livestock-manure type.
Connect_listkagri_manr_depo = {}
Graz_livstk_name = ['dair','othcatl','shep','goat']
for i in Graz_livstk_name:
    Connect_listkagri_manr_depo[i] = {}
    Connect_listkagri_manr_depo[i] = Imp_func.dict_name_path(list(Manr_appli_onagri_wddt.keys()),\
        Imp_func.glob.glob(Pj_path.output_prj_wd+Fold_path_spc_livstkcropgras_manrdepo +'*_'+i+r'_*.tif',\
            recursive=False))



# %%
## Export Connected CropAniManr emission maps by livestock emission factors
### emissions from manure applied on cropland
#OUTPUT_FILE
for i in Connect_listkcrop_manr_app:
    for j in Manr_appli_oncrop_wddt:
        Emi_connectted_Crop_Animanr = App_emifac_wddt[i]*Imp_func.tidy_zero(App_manr_RatioTAN[i])*\
            Imp_func.tidy_zero(Connect_listkcrop_manr_app[i][j])
        Imp_func.output_ras(Pj_path.output_prj_wd + Fold_path_spc_livstkcrop_manrEMI + j +'_'+ i + '_Emi.tif',\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',Emi_connectted_Crop_Animanr)


### emissions from manure applied on grassland
#OUTPUT_FILE
for i in Connect_listkgras_manr_app:
    for j in Manr_appli_ongras_wddt:
        Emi_connectted_Gras_Animanr = App_emifac_wddt[i] * Imp_func.tidy_zero(App_manr_RatioTAN[i])*\
            Imp_func.tidy_zero(Connect_listkgras_manr_app[i][j])
        Imp_func.output_ras_filtered(Pj_path.output_prj_wd + Fold_path_spc_livstkcrop_manrEMI + j +'_'+ i + '_Emi.tif',\
            Pj_path.Exam_crop_reson_wd,'EPSG:4326',Emi_connectted_Gras_Animanr)


### emissions from manure deposited on agricultural land
#OUTPUT_FILE
for i in Connect_listkagri_manr_depo:
    if Manradj_opt == 1:
        for j in Manr_appli_onagri_wddt:
            Emi_connected_depo_animanr = Imp_func.cali_fig_filter(Connect_listkagri_manr_depo[i][j],\
                Pj_path.Exam_crop_reson_wd,Pj_path.EFTA_UK_wd, Graz_EF_df, 'FID_1','Name_abbre',\
                Graz_EF_df.columns.tolist()[list( Connect_listkagri_manr_depo.keys()).index(i)+11],\
                0.0833333333333333,Pj_path.output_prj_wd+Fold_path_spc_livstkcrop_manrdepoEMI +j +'_'+ i + '_Emi.tif')
    if Manradj_opt == 2:
        for j in Manr_depo_onagri_wddt:
            Emi_connected_depo_animanr = Imp_func.cali_fig_filter(Connect_listkagri_manr_depo[i][j],\
                Pj_path.Exam_crop_reson_wd,Pj_path.EFTA_UK_wd, Graz_EF_df, 'FID_1','Name_abbre',\
                Graz_EF_df.columns.tolist()[list(Connect_listkagri_manr_depo.keys()).index(i)+11],\
                0.0833333333333333,Pj_path.output_prj_wd+Fold_path_spc_livstkcrop_manrdepoEMI +j +'_'+ i + '_Emi.tif')


## Export Connected CropAniManr emission maps by crop emission factors
#OUTPUT_FILE
for i in Manr_appli_onagri_wddt:
    Emi_crop_manrapp = Imp_func.tidy_zero(Manr_appli_onagri_wddt[i]) * Imp_func.tidy_zero(Crop_manrapp_emifac_wddt[i])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+Fold_path_spc_livstkcrop_manrEMI_bycrop+i+'_ManrlandEmi.tif',\
        Pj_path.Exam_crop_reson_wd,'EPSG:4326',Emi_crop_manrapp)



#%%
#----------------------------------------------------output_module----------------------------------------------------
# SUMMARY
## manure applied N on crops
Imp_func.zonal_summary(CropAniManrappN_name,CropAniManrapp_N_wdlt,Pj_path.EFTA_UK_wd,32,'sum',-999,\
                       Pj_path.output_prj_excel_wd+'test_output/'+ Excel_name_spc_livstkcrop_manr) 

# SUMMARY
## manure applied N on grassland
Imp_func.zonal_summary(GrasAniManrappN_name, GrasAniManrapp_N_wdlt, Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd+'test_output/'+Excel_name_spc_livstkgras_manr)


## manure deposited N on grassland
#SUMMARY
Imp_func.zonal_summary(AniManrdepoN_name,AniManrdepo_N_wdlt,Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd+'test_output/'+ Excel_name_spc_livstkcropgras_manrdepo)


#%%
## Summarize emissions connected CropAniManr
#SUMMARY
### manure application emissions calculated by animal parameters
AniManrapp_Emi_wdlt = Imp_func.glob.glob(Pj_path.output_prj_wd+Fold_path_spc_livstkcrop_manrEMI+'*.tif',\
    recursive=False)

AniManrapp_Emi_name = []
for path in AniManrapp_Emi_wdlt:
    filename = path.split('\\')[-1]
    result='_'.join(filename.split('_')[:3])
    AniManrapp_Emi_name.append(result)

AniManrapp_Emi_wddt = Imp_func.dict_name_path(AniManrapp_Emi_name,AniManrapp_Emi_wdlt) 

Imp_func.zonal_summary(AniManrapp_Emi_name,AniManrapp_Emi_wdlt,Pj_path.EFTA_UK_wd,32,'sum',-999,\
                       Pj_path.output_prj_excel_wd+'test_output/'+ Excel_name_spc_livstkcrop_manrEMI)

 
#SUMMARY
### manure application emissions calculated by crop parameters
Emi_manrapp_bycrop_wddt = Imp_func.dict_name_path(list(Manr_appli_onagri_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+Fold_path_spc_livstkcrop_manrEMI_bycrop+'*_ManrlandEmi.tif',\
        recursive=False))

Imp_func.zonal_summary(list(Emi_manrapp_bycrop_wddt.keys()),list(Emi_manrapp_bycrop_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/'+Excel_name_spc_livstkcrop_manrEMI_bycrop)


#SUMMARY
### manure deposition emissions calculated by animal parameters
AniManrdepo_Emi_wdlt = Imp_func.glob.glob(Pj_path.output_prj_wd+Fold_path_spc_livstkcrop_manrdepoEMI+'*_Emi.tif',\
    recursive=False)

AniManrdepo_Emi_name = []
for path in AniManrdepo_Emi_wdlt:
    filename = path.split('\\')[-1]
    result='_'.join(filename.split('_')[:2])
    AniManrdepo_Emi_name.append(result)

AniManrdepo_Emi_wddt=Imp_func.dict_name_path(AniManrdepo_Emi_name,AniManrdepo_Emi_wdlt)

Imp_func.zonal_summary(AniManrdepo_Emi_name,AniManrdepo_Emi_wdlt,Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd+'test_output/'+ Excel_name_spc_livstkcrop_manrdepoEMI)


## Summarize important pathways
I14_dict={'Manr_cropapp_N_wddt':CropAniManrapp_N_wddt,\
    'Manr_grasapp_N_wddt':GrasAniManrapp_N_wddt,\
    'Manr_depo_N_wddt':AniManrdepo_N_wddt,\
    'Manr_app_emi_wddt':AniManrapp_Emi_wddt,\
    'Manr_depo_emi_wddt':AniManrdepo_Emi_wddt}


Imp_func.save_plk(r'../B_Output/'+Pickle_name_output,I14_dict)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")


