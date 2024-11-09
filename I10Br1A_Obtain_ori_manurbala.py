#%%
'''
Could be run directly
running time is 37s

This script is to...
Land areas -> land capacities(three types) -> manure application shares -> manure application N -> manure application N resample to 0.05° -> manure balance

Outputs:
-crop and grass areas: total cropland area(Pysi_area_EFTA_wd, all crops in CROPGRID dataset) ; temporary grassland area(Tempgras_wd); permanant grassland area()
-manure capacities: cropland capacity by different constrains (Map: Pysi_capat_crop_wddt; Excel:), temporary grassland capacity(Pysi_capat_tempgras_wd),permanent grassland capacity(Pysi_capat_permgras_wd); 
-manure applied to cropland and grassland by livestock type: to cropland(Map:App_manrtoC_wdlt,Excel:Manur_app_N_toC.xlsx); to grassland(Map:App_manrtoG_wdlt,Excel:Manur_app_N_toG.xlsx)
-manure applied to cropland and grassland total: to cropland(Map:Tot_manrsamp_EFTAwd); to grassland(Map: Tot_manrsamp_gras_EFTAwd)
-manure balance: cropland by different constrains (Map:Capat_marNsign_EFTAwddt), grassland(Map:Capat_marNsign_gras_EFTAwd)

'''

#%%
# Import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
# Load necessary pathways
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
## basic output paths
output_wd = r'K:/Default_database/raster/'
output_prj_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/'

##basic crop maps
Cropmap_df = Imp_func.open_plk(r'../B_Output/J20.pkl')
#Basic manure maps
H89_dt = Imp_func.open_plk(r'../B_Output/H89.pkl')
Manr_appN_wddt = Imp_func.conv_df2dict(H89_dt['Manr_app_df'],'Ani_manr_type',\
    'App_manr_N')

H87_dt = Imp_func.open_plk(r'../B_Output/H87.pkl')
Manr_graz_excrN_wddt = Imp_func.conv_df2dict(H87_dt,'Anim_name','Graz_ExcrN')

## output paths
Pysi_area_EFTA_wd = output_prj_wd + 'CG_phytot_EFTA.tif'#(USED)
Pysi_capat_wd = output_prj_wd + 'Manur_capacity/Pysi_capat.tif' #(USED, capacity for cropland)
Pysi_capat_tempgras_wd = output_prj_wd + 'Manur_capacity/Pysi_capat_tempgras.tif'#(USED)
Pysi_capat_permgras_wd = output_prj_wd + 'Manur_capacity/Pysi_capat_permgras.tif'#(USED)
Pysi_capat_graswd = output_prj_wd + 'Manur_capacity/Pysi_capat_totgras.tif'#(USED)
Pysi_capat_totwd = Pj_path.output_prj_wd + 'Manur_capacity/Tot_manur_capa.tif'#(USED)


Tot_manr_wd = output_prj_wd + 'Manur_tot_CropGrass/Tot_manur_crop.tif'#(USED)
Tot_manr_realapp_gras_wd = output_prj_wd + 'Manur_tot_CropGrass/Tot_manur_gras_realapp.tif'#(USED)
Tot_manr_gras_wd = output_prj_wd + 'Manur_tot_CropGrass/Tot_manur_gras.tif'#(USED)
Tot_manr_tot_wd = output_prj_wd + 'Manur_tot_CropGrass/Tot_manur_tot.tif'#(USED)

## manure capacity data
Capat_marNsign_EFTAwd = output_prj_wd + 'Manur_capacity/Capat_marNsign.tif' #(USED)
Capat_marNsign_gras_EFTAwd = output_prj_wd + 'Manur_capacity/Capat_grasmarNsign.tif'#(USED)


Total_bala_wd = Pj_path.output_prj_wd + 'Manur_capacity/Capat_TotmarNsign.tif'#(USED)

Manr_appl_intn_wd = output_wd + 'Manr_intn.tif'
Manr_appl_intn_EFTA_wd = output_prj_wd + 'Manur_capacity/Manr_intn_EFTA.tif'


## basic vectors
EFTA_UK_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/EFTA_UK2_WGS.shp'
EFTA_NUTS2_wd = r'K:/Default_database/shapefile/EFTA_NUTS2.shp'

#%%
#----------------------------------------------------processing_module----------------------------------------------------
# Identify supplus and non-surplus cropland and grassland (export the map of cropland capacity)
#OUTPUT_DATA

## Get total physical area of vital CROPGRID maps, note that physical areas are actually the same as harvested areas
Input_CROPGRID_ori_wddt = Imp_func.conv_df2dict(Cropmap_df,'Cropname','Final_cropmaps')

Input_CROPGRID_wddt = Imp_func.conv_df2dict(Cropmap_df,'Cropname','Final_cropmaps')
for key in ['Tempgra','Permgra']:
    if key in Input_CROPGRID_wddt:
        del Input_CROPGRID_wddt[key]


Input_CROPGRID_wdlt = list(Input_CROPGRID_wddt.values())
#(we confirmed that harvested areas equel to physical area in Europe)

Tot_phygrid = Imp_func.aggregate(Input_CROPGRID_wdlt)

#%%
# OUTPUT_INTE_FILE
Imp_func.output_ras_filtered(Pysi_area_EFTA_wd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Tot_phygrid)


#%%
## Calculate the capacities of cropland and grassland (export maps of grassland capacities)
### Cropland capacity
Capat_marN = Imp_func.tidy_zero(Pysi_area_EFTA_wd) * 170

#%%
#OUTPUT_FILE
Imp_func.output_ras_filtered(Pysi_capat_wd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Capat_marN)

#%%
#OUTPUT_DATA
### grassland capacity
Gras_shar = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='gras_capacity')

####multiply grassland with allowed manure application intensities
Gras_wddt = dict(zip(['Tempgra','Permgra'],\
    [Input_CROPGRID_ori_wddt['Tempgra'] ,Input_CROPGRID_ori_wddt['Permgra']]))
Gras_capat_wddt = dict(zip(['Tempgra','Permgra'],[Pysi_capat_tempgras_wd,Pysi_capat_permgras_wd]))

#%%
#OUTPUT_FILE
for i in Gras_wddt:
    Imp_func.cali_fig(Gras_wddt[i],Pj_path.Exam_crop_reson_wd,\
        Pj_path.EFTA_UK_wd,Gras_shar,'FID_1','Name_abbre','capa',\
        0.0833333333333333, Gras_capat_wddt[i])

#OUTPUT_DATA
Capat_marN_gras = Imp_func.aggregate(list(Gras_capat_wddt.values()))
Capat_manN_tot = Capat_marN_gras + Capat_marN

#OUTPUT_FILE
Imp_func.output_ras_filtered(Pysi_capat_graswd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Capat_marN_gras)
Imp_func.output_ras_filtered(Pysi_capat_totwd ,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Capat_manN_tot)


#%%
## Compare manure production and capacity and identify exceeded cells
#OUTPUT_DATA
### manure fates to cropland
#### get the fractions of manure to cropland
Anim_fate_wdlt = ['pig_sld','pig_liq','dair_sld','dair_liq','othcatl_sld','othcatl_liq','potr_sld','potr_liq']


#%%
#OUTPUT_FILE

## Calculate the parts of manure to cropland and grassland
Manr_fate_crop = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='manureNfate_crop')
Manr_fate_gras = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='manureNfate_gras')

#Note: 1. all manure produced by sheep and goats goes to grassland; 2.all poultry manure is solid manure
for i in Anim_fate_wdlt:
    Imp_func.cali_fig_filter(Manr_appN_wddt[i],Pj_path.Exam_crop_reson_wd,\
        Pj_path.EFTA_UK_wd,Manr_fate_crop,'FID_1','Name_abbre',\
        Manr_fate_crop.columns.tolist()[Anim_fate_wdlt.index(i) + 4], 0.0833333333333333, \
            output_prj_wd+'manrN_fate_to_C/'+ i +'_NtoC.tif')
    Imp_func.cali_fig_filter(Manr_appN_wddt[i],Pj_path.Exam_crop_reson_wd,\
        Pj_path.EFTA_UK_wd,Manr_fate_gras,'FID_1','Name_abbre',\
        Manr_fate_gras.columns.tolist()[Anim_fate_wdlt.index(i) + 4],0.0833333333333333,\
            output_prj_wd+'manrN_fate_to_G/'+ i +'_NtoG.tif')


#(GET THE MANURE TO cropland and grassland for animals both existed in the two categories. For sheep and goat manure to
# grassland, we will add them later)

#%%
#OUTPUT_DATA
App_manrtoC_wddt = Imp_func.dict_name_path(Anim_fate_wdlt,Imp_func.glob.glob( output_prj_wd+'manrN_fate_to_C/*_NtoC.tif'))

App_manrtoG_wdltorg = Imp_func.glob.glob(Pj_path.output_prj_wd+'manrN_fate_to_G/*.tif',recursive = False) +\
    [Manr_appN_wddt['shep_sld'],Manr_appN_wddt['shep_liq'],Manr_appN_wddt['goat_sld'],Manr_appN_wddt['goat_liq']] +\
        list(Manr_graz_excrN_wddt.values())

App_manrtoG_onlyapp_wdlt = Imp_func.glob.glob(Pj_path.output_prj_wd+'manrN_fate_to_G/*.tif',recursive = False) +\
    [Manr_appN_wddt['shep_sld'],Manr_appN_wddt['shep_liq'],Manr_appN_wddt['goat_sld'],Manr_appN_wddt['goat_liq']]

App_manr_nameall1 = Anim_fate_wdlt + ['solid_shep','liq_shep','solid_goat','liq_goat']
App_manr_nameall2 = Anim_fate_wdlt + ['solid_shep','liq_shep','solid_goat','liq_goat'] + ['dair_graz','othcatl_graz','shep_graz','goat_graz']

App_manrtoG_realapp_wddt = Imp_func.dict_name_path(App_manr_nameall1,App_manrtoG_onlyapp_wdlt)
App_manrtoG_wddt = Imp_func.dict_name_path(App_manr_nameall2,App_manrtoG_wdltorg)


#### Aggregate to manure application by land
Tot_appmanr = Imp_func.aggregate(list(App_manrtoC_wddt.values()))
Tot_appmanr_gras_realapp = Imp_func.aggregate(list(App_manrtoG_realapp_wddt.values()))
Tot_appmanr_gras = Imp_func.aggregate(list(App_manrtoG_wddt.values()))

Tot_appmanr_tot = Tot_appmanr + Tot_appmanr_gras

#%%
#OUTPUT_FILE
Imp_func.output_ras_filtered(Tot_manr_wd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Tot_appmanr)
Imp_func.output_ras_filtered(Tot_manr_realapp_gras_wd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Tot_appmanr_gras_realapp)
Imp_func.output_ras(Tot_manr_gras_wd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Tot_appmanr_gras)
Imp_func.output_ras(Tot_manr_tot_wd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Tot_appmanr_tot)


#%%
#OUTPUT_DATA
Capat_marN_sign = Imp_func.tidy_zero(Pysi_capat_wd) - Imp_func.tidy_zero(Tot_manr_wd)
Capat_marN_signgras = Imp_func.tidy_zero(Pysi_capat_graswd)- Imp_func.tidy_zero(Tot_manr_gras_wd)
Capat_manrN_signtot = Capat_marN_sign + Capat_marN_signgras

#%%
#OUTPUT_FILE
Imp_func.output_ras_filtered(Capat_marNsign_EFTAwd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Capat_marN_sign)
Imp_func.output_ras_filtered(Capat_marNsign_gras_EFTAwd,Pj_path.Exam_crop_reson_wd,'EPSG:4326',Capat_marN_signgras)
Imp_func.output_ras_filtered(Pj_path.output_prj_wd + 'Manur_capacity/Capat_TotmarNsign.tif',\
    Pj_path.Exam_crop_reson_wd,'EPSG:4326',Capat_manrN_signtot)

#%%
#----------------------------------------------------output_module----------------------------------------------------
#Collect output data
# OUTPUT_DATA
All_manr_livstk_lt = list(App_manrtoG_wddt.keys())[:8] + ['shep_sld','shep_liq','goat_sld','goat_liq'] \
    + list(App_manrtoG_wddt.keys())[12:]

App_manrtoG_wddt2 = Imp_func.replace_keys(App_manrtoG_wddt,All_manr_livstk_lt)

Manrapp_byani_df = Imp_func.conv_dict2df(App_manrtoG_wddt2,'Ani_manr_type','Grass_app_maps')
Manrapp_byani_df = Imp_func.join_dict2df(Manrapp_byani_df,App_manrtoC_wddt,'Ani_manr_type','Crop_app_maps')


Manr_appN_wddt.update({'dair_graz':App_manrtoG_wddt['dair_graz'],'othcatl_graz':App_manrtoG_wddt['othcatl_graz'],\
    'shep_graz':App_manrtoG_wddt['shep_graz'],'goat_graz':App_manrtoG_wddt['goat_graz']})
Manrapp_byani_df = Imp_func.join_dict2df(Manrapp_byani_df,Manr_appN_wddt,'Ani_manr_type','Tot_app_maps')


Manr_landtype_oriwddt = dict(zip(['Crop_manrapp','Grass_manrapp','Total_manrapp'],[Tot_manr_wd,Tot_manr_gras_wd,Tot_manr_tot_wd]))
Manrapp_byland_df = Imp_func.conv_dict2df(Manr_landtype_oriwddt,'land_type','ori_manrbyland_map')

Manr_landtype_orirealapp_wddt = dict(zip(['Crop_manrapp','Grass_manrapp'],[Tot_manr_wd,Tot_manr_realapp_gras_wd]))
Manrapp_byland_df = Imp_func.join_dict2df(Manrapp_byland_df,Manr_landtype_orirealapp_wddt,'land_type','ori_manr_realapp_map')

Capa_landtype_wddt = dict(zip(['Crop_manrapp','Grass_manrapp','Total_manrapp'],[Pysi_capat_wd,Pysi_capat_graswd,Pysi_capat_totwd]))
Manrapp_byland_df = Imp_func.join_dict2df(Manrapp_byland_df,Capa_landtype_wddt,'land_type','capacity_byland_map')

Manubala_landtype_wddt = dict(zip(['Crop_manrapp','Grass_manrapp','Total_manrapp'],[Capat_marNsign_EFTAwd,Capat_marNsign_gras_EFTAwd,Total_bala_wd]))
Manrapp_byland_df = Imp_func.join_dict2df(Manrapp_byland_df,Manubala_landtype_wddt,'land_type','Manrbala_byland_map')

#%%
# Export important files
# OUTPUT_FILE
I10A = {'Manrapp_byani_maps':Manrapp_byani_df,\
        'Manrapp_byland_maps':Manrapp_byland_df,\
        'Capa_bygrass':Gras_capat_wddt}

Imp_func.save_plk(r'../B_Output/I10A.pkl',I10A)


#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")