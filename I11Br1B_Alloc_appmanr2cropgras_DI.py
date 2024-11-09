'''
This script aims to allocate livestock manure to specific crops and grasses directly
This script can be run automatically. Running time is 34s.
'''

#%%
# Import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path


#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
# Import important pathways
## We have already got the manure to cropland and grassland in I10A/I10B.plk
I10B_dict = Imp_func.open_plk(r'../B_Output/I10B.pkl') #provides manure maps by land
Manraap_byland_df = I10B_dict['Manrapp_byland']

## original manure application maps
Manrapp_ori_wddt = Imp_func.conv_df2dict(Manraap_byland_df,'land_type','ori_manr_realapp_map')
Manrapp_ori_wddt = Imp_func.dict_del_nan(Manrapp_ori_wddt)
Tot_manr_gras_wd = Manrapp_ori_wddt['Grass_manrapp']

## Cropmaps
OSD_CROPGRID_df = Imp_func.open_plk(r'../B_Output/J20.pkl') #provides crop maps
OSD_CROPGRID_area_wddt = Imp_func.conv_df2dict(OSD_CROPGRID_df,'Cropname','Final_cropmaps')

Tempgras_wd = OSD_CROPGRID_area_wddt['Tempgra']
Permgras_wd = OSD_CROPGRID_area_wddt['Permgra']


#%%
#----------------------------------------------------Processing_module----------------------------------------------------
## Allocate total marure to different grasses, including grazing manure
#OUTPUT_DATA
### Manure fractions to different grasses
Manur_frac_gras = 1 * Imp_func.tidy_zero(Tempgras_wd) + 0.5 * Imp_func.tidy_zero(Permgras_wd) 

### Get the manure application intensities for temporary grass when not considering capacities
Manur_appl_intn_grasnolimit = Imp_func.tidy_zero(Tot_manr_gras_wd) / Manur_frac_gras # manure revised
Manur_appl_intn_grasnolimit[Imp_func.np.isnan(Manur_appl_intn_grasnolimit)] = 0 # adjust cells with 0 grassland
Manur_appl_intn_grasnolimit[Imp_func.np.isneginf(Manur_appl_intn_grasnolimit)] = 0 # adjust cells with very small grassland
Manur_appl_intn_grasnolimit[Imp_func.np.isinf(Manur_appl_intn_grasnolimit)] = 0 # adjust cells with very small grassland


#%%
#OUTPUT_DATA
### Calculate manure N on different grasses 
Manur_tempgras_nolim = Manur_appl_intn_grasnolimit * Imp_func.tidy_zero(Tempgras_wd) # manure applied on temporary grass
Manur_permgras_nolim = Manur_appl_intn_grasnolimit * 0.5 * Imp_func.tidy_zero(Permgras_wd) # manure applied on permanent grass

#%%
#OUTPUT_FILE
### Get the maps for grass manure application
Imp_func.output_ras_filtered(Pj_path.output_prj_wd+r'Manur_Ngras_realnolimit/Manur_tempgras_realnolim.tif',\
    Pj_path.Exam_crop_reson_wd,'EPSG:4326',\
    Manur_tempgras_nolim) # export mannure N on temporary grass
Imp_func.output_ras_filtered(Pj_path.output_prj_wd+r'Manur_Ngras_realnolimit/Manur_Permgras_realnolim.tif',\
    Pj_path.Exam_crop_reson_wd, 'EPSG:4326',\
    Manur_permgras_nolim) # export manure N on permanent grass


#%%
## Get the manure application intensities for group1 when not considering capacities
### Get the coefficients that will be divided later
#OUTPUT_DATA
#### Get the harvested area map for each group
G1_crop_wdlt = [OSD_CROPGRID_area_wddt['Whea'],OSD_CROPGRID_area_wddt['Barl'],OSD_CROPGRID_area_wddt['Rapesd'],OSD_CROPGRID_area_wddt['Sugbt']]
G2_crop_wdlt = [OSD_CROPGRID_area_wddt['Maiz'],OSD_CROPGRID_area_wddt['Grenmaiz'],OSD_CROPGRID_area_wddt['Sunflrsd'],OSD_CROPGRID_area_wddt['Oats'],\
    OSD_CROPGRID_area_wddt['Rye'],OSD_CROPGRID_area_wddt['Pota'],OSD_CROPGRID_area_wddt['Vege']]
G3_crop_wdlt = [OSD_CROPGRID_area_wddt['Nuts'],OSD_CROPGRID_area_wddt['Fruit']]
G4_crop_wdlt = [OSD_CROPGRID_area_wddt['Legumfod'],OSD_CROPGRID_area_wddt['Soya'],OSD_CROPGRID_area_wddt['Rice'],OSD_CROPGRID_area_wddt['Peabean']]


G1_crop_wddt = dict(zip(['Whea','Barl','Rapesd','Sugbt'],G1_crop_wdlt))
G2_crop_wddt = dict(zip(['Maiz','Grenmaiz','Sunflrsd','Oats','Rye','Pota','Vege'],G2_crop_wdlt))
G3_crop_wddt = dict(zip(['Nuts','Fruit'],G3_crop_wdlt))
G4_crop_wddt = dict(zip(['Legumfod','Soya','Rice','Peabean'],G4_crop_wdlt))

Crop_group_wddt = dict(zip(['G1','G2','G3','G4'],[G1_crop_wdlt,G2_crop_wdlt,G3_crop_wdlt,G4_crop_wdlt]))
Crop_group_wddt2 = dict(zip(['G1','G2','G3','G4'],[G1_crop_wddt,G2_crop_wddt,G3_crop_wddt,G4_crop_wddt]))

for i in Crop_group_wddt :
    Tot_G_phygrid = Imp_func.aggregate(Crop_group_wddt[i])
    #OUTPUT_FILE
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + 'Croparea_by_ManralloGroup/CGG_phytot_'+i+'_EFTA.tif',\
        Pj_path.Exam_crop_reson_wd,'EPSG:4326',Tot_G_phygrid)

#OUTPUT_DATA
Manur_frac=1 * Imp_func.tidy_zero(Pj_path.output_prj_wd + 'Croparea_by_ManralloGroup/CGG_phytot_G1_EFTA.tif') + \
    0.5 * Imp_func.tidy_zero(Pj_path.output_prj_wd + 'Croparea_by_ManralloGroup/CGG_phytot_G2_EFTA.tif') +\
        0.25 * Imp_func.tidy_zero(Pj_path.output_prj_wd + 'Croparea_by_ManralloGroup/CGG_phytot_G3_EFTA.tif')


Manur_appl_intn_nolimit = Imp_func.tidy_zero(Manrapp_ori_wddt['Crop_manrapp'])/ Manur_frac
Manur_appl_intn_nolimit[Imp_func.np.isnan(Manur_appl_intn_nolimit)] = 0 # adjust cells with 0 CROPland
Manur_appl_intn_nolimit[Imp_func.np.isneginf(Manur_appl_intn_nolimit)] = 0 # adjust cells with very small cropland
Manur_appl_intn_nolimit[Imp_func.np.isinf(Manur_appl_intn_nolimit)] = 0 #adjust cells with very small cropland


#%%
## Calculate MANURE N on each crop
for i in Crop_group_wddt2:
    #OUTPUT_FILE
    if i == 'G1':
        for j in Crop_group_wddt2[i]:
            Manur_appl_onC = Imp_func.tidy_zero(Crop_group_wddt2[i][j]) * 1 * Manur_appl_intn_nolimit
            Imp_func.output_ras_filtered(Pj_path.output_prj_wd+r'Manur_Ncrop_realnolimit/' + j +'_Mnurcp_REALDInolimt.tif',\
                Pj_path.Exam_crop_reson_wd,'EPSG:4326',Manur_appl_onC)
    elif i == 'G2':
        for j in Crop_group_wddt2[i]:
            Manur_appl_onC = Imp_func.tidy_zero(Crop_group_wddt2[i][j]) * 0.5 * Manur_appl_intn_nolimit
            Imp_func.output_ras_filtered(Pj_path.output_prj_wd+r'Manur_Ncrop_realnolimit/' + j +'_Mnurcp_REALDInolimt.tif',\
                Pj_path.Exam_crop_reson_wd,'EPSG:4326',Manur_appl_onC)
    else:
        for j in Crop_group_wddt2[i]:
            Manur_appl_onC = Imp_func.tidy_zero(Crop_group_wddt2[i][j]) * 0.25 * Manur_appl_intn_nolimit
            Imp_func.output_ras_filtered(Pj_path.output_prj_wd+r'Manur_Ncrop_realnolimit/' + j +'_Mnurcp_REALDInolimt.tif',\
                Pj_path.Exam_crop_reson_wd,'EPSG:4326',Manur_appl_onC)


#%%
## Summarize and plotting all maps for cropland manure N application
# OUTPUT_DATA
Vital_manr_cropname = Pj_path.MainCpNam
indices_to_delete = [5,8,10,14]

Vital_manr_cropname_new = [Vital_manr_cropname[i] 
                           for i in range(len(Vital_manr_cropname)) 
                           if i not in indices_to_delete]


Vital_manr_cropwddt =Imp_func.dict_name_path(Vital_manr_cropname_new,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Manur_Ncrop_realnolimit/*_Mnurcp_REALDInolimt.tif',\
        recursive=False))

Vital_manr_graswddt = {'Tempgra':Pj_path.output_prj_wd+r'Manur_Ngras_realnolimit/Manur_tempgras_realnolim.tif',\
    'Permgra':Pj_path.output_prj_wd+r'Manur_Ngras_realnolimit/Manur_Permgras_realnolim.tif'}

Vital_manr_plantwddt = {**Vital_manr_cropwddt,**Vital_manr_graswddt}

#%%
#----------------------------------------------------Output_module----------------------------------------------------
#SUMMARY
### Summarize manure N on grassland without limitations
Imp_func.zonal_summary(['Manure_on_permgras_nolimt','Manure_on_tempgras_nolimt'],\
    Imp_func.glob.glob(Pj_path.output_prj_wd + r'Manur_Ngras_realnolimit/*.tif'),Pj_path.EFTA_UK_wd,\
        32,'sum',-999,Pj_path.output_prj_excel_wd + 'test_output/Manur_app_N_toG_bytype_REALDInolimt.xlsx')


# SUMMARY
Imp_func.zonal_summary(list(Vital_manr_cropwddt.keys()),\
    list(Vital_manr_cropwddt.values()),Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd + 'test_output/Manur_app_N_toC_bytype_REALDInolimt.xlsx')


#%%
## Export data
OSD_CROPGRID_df_new=Imp_func.join_dict2df(OSD_CROPGRID_df, Vital_manr_plantwddt , 'Cropname', 'Manr_appl_DI') #Manure on land by crop
Imp_func.save_plk(r'../B_Output/I11Br1B.pkl',OSD_CROPGRID_df_new)


#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")