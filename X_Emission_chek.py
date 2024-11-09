#%%
'''
This script is aiming to get emission data from crop side only (synthetic fertilizer), livestock side only (manure management),
and both side related emissions(manure on land)

'''
#%%
# Import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%

#OUTPUT_DATA
## Emissions from each detailed category
### All categories
Chemifer_df = Imp_func.open_plk(r'../B_Output/A51.pkl') #synthetic fertilizer pathways
Chemfer_EMI_wddt = Imp_func.conv_df2dict(Chemifer_df,'OSDCropname','Chemfer_EMI_kg') #pathways of emissions from synthetic fertilizer 

I15_Manrcroplink_dict=Imp_func.open_plk(r'../B_Output/I15Br1B.pkl') # pathways providing emissions from specific livestock to specific crops, including both deposition and application
Manr_applink_dict = I15_Manrcroplink_dict['Manr_app_emi_wddt'] # pathways providing manure applied on specific crops
Manr_depolink_dict = I15_Manrcroplink_dict['Manr_depo_emi_wddt'] # pathways providing manure deposited on specific crops

H89_dict =  Imp_func.open_plk(r'../B_Output/H89.pkl') #manure management emissions by livestock
Manr_mana_df = H89_dict['Manr_mana_df']
Hous_emi_wddt = Imp_func.conv_df2dict(Manr_mana_df,'Ani_manr_type','Hous_emi_wddt')
Hous_emi_wddt= {key: [value] for key, value in Hous_emi_wddt.items()}
Stor_emi_wddt = Imp_func.conv_df2dict(Manr_mana_df,'Ani_manr_type','Stor_emi_wddt')
Stor_emi_wddt = {key: [value] for key, value in Stor_emi_wddt.items()}

#%%
# OUTPUT_DATA
# Emissions from synthetic fertilizer
for i in list(Chemfer_EMI_wddt.keys()):
    source_path = Chemfer_EMI_wddt[i]
    
    destination_folder_path = Pj_path.output_prj_wd+r'Upload_files/Synthetic_fertilizer_use(SF)/'
    New_Emi_synfer_filename = f"SF_{i}_NH3-N.tif"  # Example: prefix "new_" to each file name
    destination_path = Imp_func.os.path.join(destination_folder_path, New_Emi_synfer_filename) 

    # Copy the file and rename it
    Imp_func.shutil.copy2(source_path, destination_path)

# Emissions from manure input
## Emissions from manure application by crop
Crop_manr_hierk_dict = {i: [] for i in Pj_path.MainCpNam}

for i in Pj_path.MainCpNam:
    for j in Manr_applink_dict:
        if i in j:
            Crop_manr_hierk_dict[i].append(Manr_applink_dict[j])

# Filter out keys with empty lists
Crop_manr_hierk_dict = {k: v for k, v in Crop_manr_hierk_dict.items() if v}


## Emissions from manure deposition by crop
### manure application emissions calculated by animal parameters
Gras_depo_hierk_dict = {i: [] for i in ['Tempgra','Permgra']}

for i in Gras_depo_hierk_dict:
    for j in Manr_depolink_dict:
        if i in j:
            Gras_depo_hierk_dict[i].append(Manr_depolink_dict[j])


## Emission from manure input by crop
for key, value in Gras_depo_hierk_dict.items():
    if key in Crop_manr_hierk_dict:  
        Crop_manr_hierk_dict[key].extend(value)  
    else:
        Crop_manr_hierk_dict[key] = value  

# OUTPUT_FILE
for k in Crop_manr_hierk_dict:
    Crop_manr_inputN = Imp_func.aggregate(Crop_manr_hierk_dict[k])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+\
        r'Upload_files/Manure_input(MI)/MI_'+k+'_NH3-N.tif',Pj_path.Exam_crop_reson_wd,\
        'EPSG:4326',Crop_manr_inputN)


#%%
## Emissions from manure management
# OUTPUT_DATA
### Emission from manure managment combining housing and storage
for key, value in Hous_emi_wddt.items():
    if key in Stor_emi_wddt:
        Hous_emi_wddt[key].extend(value)  
    else:
        Hous_emi_wddt[key] = value  

## Emissions from manure management by livestock
Livestk_manr_hierk_dict = {i: [] for i in Pj_path.Ani_name}

for i in Pj_path.Ani_name:
    for j in Hous_emi_wddt:
        if i in j:
            Livestk_manr_hierk_dict[i].append(Hous_emi_wddt[j])

for v in Livestk_manr_hierk_dict:
    Livestk_manr_hierk_dict[v] = [item for sublist in \
        Livestk_manr_hierk_dict[v] for item in sublist]

#OUTPUT_FILE
for k in Livestk_manr_hierk_dict:
    Livestk_manr_mana_N = Imp_func.aggregate(Livestk_manr_hierk_dict[k])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+\
            r'Upload_files/Manure_management(MM)/MM_'+k+'_NH3-N.tif',Pj_path.Exam_crop_reson_wd,\
            'EPSG:4326',Livestk_manr_mana_N)


#%%
## Emissions from Manure deposited on grassland by livestock
# OUTPUT_DATA
Livstk_depo_hierk_dict = {i: [] for i in Pj_path.Ani_name}

for i in Livstk_depo_hierk_dict:
    for j in Manr_depolink_dict:
        if i in j:
            Livstk_depo_hierk_dict[i].append(Manr_depolink_dict[j])


# Filter out keys with empty lists
Livstk_depo_hierk_dict = {k: v for k, v in Livstk_depo_hierk_dict.items() if v}

#OUTPUT_FILE
for k in Livstk_depo_hierk_dict:
    Livstk_manr_depo_N = Imp_func.aggregate(Livstk_depo_hierk_dict[k])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+\
        r'Upload_files/Manure_deposition(MD)/MD_'+k+'_NH3-N.tif',Pj_path.Exam_crop_reson_wd,\
            'EPSG:4326',Livstk_manr_depo_N)


## Emissions from Manure application on cropland by livestock
# OUTPUT_DATA
Livstk_app_hierk_dict = {i: [] for i in Pj_path.Ani_name}

for i in Livstk_app_hierk_dict:
    for j in Manr_applink_dict:
        if i in j:
            Livstk_app_hierk_dict[i].append(Manr_applink_dict[j])

for k in Livstk_app_hierk_dict:
    Livstk_manr_app_N = Imp_func.aggregate(Livstk_app_hierk_dict[k])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+\
        r'Upload_files/Manure_application(MA)/MA_'+k+'_NH3-N.tif',Pj_path.Exam_crop_reson_wd,\
            'EPSG:4326',Livstk_manr_app_N)

#%% 
#### execute the summarization
##### Summary for livestock related emissions
#OUTPUT_DATA
Livstk_manrapp_wddt = Imp_func.dict_name_path(Pj_path.Ani_name,Imp_func.glob.glob(Pj_path.output_prj_wd+\
        r'Upload_files/Manure_application(MA)/MA_*_NH3-N.tif',recursive=False))

Livstk_manrdepo_wddt = Imp_func.dict_name_path(['dair','othcatl','shep','goat'],\
    Imp_func.glob.glob(Pj_path.output_prj_wd+\
        r'Upload_files/Manure_deposition(MD)/MD_*_NH3-N.tif',recursive=False))

Livstk_manrmana_wddt = Imp_func.dict_name_path(Pj_path.Ani_name,Imp_func.glob.glob(Pj_path.output_prj_wd+\
            r'Upload_files/Manure_management(MM)/MM_*_NH3-N.tif',recursive=False))

#SUMMARY

Imp_func.zonal_summary([item + 'mana' for item in list(Livstk_manrmana_wddt.keys())] + \
    [item + 'app' for item in list(Livstk_manrapp_wddt.keys())] + [item + 'depo' for item in list(Livstk_manrdepo_wddt.keys())] ,\
    list(Livstk_manrmana_wddt.values()) + list(Livstk_manrapp_wddt.values()) + list(Livstk_manrdepo_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd + r'test_output/Emi_Livstkonly.xlsx')

#%%
### execute the summarization
#### Summary for emissions from both sides related emissions and compare data from livestock side and from crop side
#SUMMARY

#OUTPUT_DATA
Manr_Inputemi_bycrop_wddt = Imp_func.dict_name_path(
    Pj_path.MainCpNam,Imp_func.glob.glob(Pj_path.output_prj_wd+\
        r'Upload_files/Manure_input(MI)/MI_*_NH3-N.tif',recursive=False)
)

Syn_fertemi_bycrop_wddt = Imp_func.dict_name_path(Pj_path.MainCpNam,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Upload_files/Synthetic_fertilizer_use(SF)/*.tif',recursive=False))


Imp_func.zonal_summary([item + 'syntfert' for item in list(Syn_fertemi_bycrop_wddt.keys())] + \
    [item + 'manrinput' for item in list(Manr_Inputemi_bycrop_wddt.keys())], \
    list(Syn_fertemi_bycrop_wddt.values()) + list(Manr_Inputemi_bycrop_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd + r'test_output/Emi_Manrinput_bycrop.xlsx')



'''
###livestock shares one (manure management/agricultural soils)
#OUTPUT_DATA
livestock_share_one = Imp_func.tidy_zero(Pj_path.output_prj_wd + 'NH3_emi_by_stage/Manr_mana_emi.tif')/\
    (Imp_func.aggregate([Pj_path.output_prj_wd + 'NH3_emi_by_stage/Manr_mana_emi.tif',\
        Pj_path.output_prj_wd + 'NH3_emi_by_stage/Manr_toland_emi.tif',\
             Pj_path.output_prj_wd + 'NH3_emi_by_stage/feremi.tif']))


#OUTPUT_FILE
Imp_func.output_ras(Pj_path.output_wd + 'livestock_shareone.tif',Chemfer_EMI_wddt['Whea'],'EPSG:4326',livestock_share_one)
Imp_func.clip_map(Pj_path.output_prj_wd + 'livestock_shareone.tif',\
    Pj_path.output_wd + 'livestock_shareone.tif',Pj_path.EFTA_UK_wd)


###livestock share two (manure management chain/chemical fertilizer)
#OUTPUT_DATA
Manr_chain_aggwd = [r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/NH3_emi_by_stage/housemi.tif',\
    r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/NH3_emi_by_stage/storemi.tif',\
        r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/NH3_emi_by_stage/Grzemi.tif',\
            r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/NH3_emi_by_stage/appemi.tif']

livestock_share_two = Imp_func.aggregate(Manr_chain_aggwd)/(Imp_func.tidy_zero(Pj_path.output_prj_wd + 'NH3_emi_by_stage/feremi.tif') +\
    Imp_func.aggregate(Manr_chain_aggwd))


#OUTPUT_FILE
Imp_func.output_ras(Pj_path.output_wd + 'livestock_sharetwo.tif',Chemfer_EMI_wddt['Whea'],'EPSG:4326',livestock_share_two)
Imp_func.clip_map(Pj_path.output_prj_wd + 'livestock_sharetwo.tif',\
    Pj_path.output_wd + 'livestock_sharetwo.tif',Pj_path.EFTA_UK_wd)

'''