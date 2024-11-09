#%%
'''
This script is aiming to align crop types(pulses,nuts,fruits,and vegetables ) in CROPGRID 
with our own classification

This script can be run automatically. Running time is 165s.
'''

#%%
# import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
# setting directories
##directory of all crops
Cropall_wd = r'K:/基础数据/A.数据/Crop_Grids_DB/CROPGRIDS_maps_convt/Crop_harvest/'

## directories of peas and pulses
Bean_area_wd = Cropall_wd + 'CROPGRIDSv1.05_bean.nc.tif'
Chikpea_area_wd = Cropall_wd + 'CROPGRIDSv1.05_chickpea.nc.tif'
Cowpea_area_wd = Cropall_wd + 'CROPGRIDSv1.05_cowpea.nc.tif'
Pigonpea_area_wd = Cropall_wd + 'CROPGRIDSv1.05_pigeonpea.nc.tif'
Lentil_area_wd = Cropall_wd + 'CROPGRIDSv1.05_lentil.nc.tif'
Bambra_area_wd = Cropall_wd + 'CROPGRIDSv1.05_bambara.nc.tif'
Brodbean_area_wd = Cropall_wd + 'CROPGRIDSv1.05_broadbean.nc.tif'
Lupin_area_wd = Cropall_wd + 'CROPGRIDSv1.05_lupin.nc.tif'
Pea_area_wd = Cropall_wd + 'CROPGRIDSv1.05_pea.nc.tif'
Pulsenes_area_wd = Cropall_wd + 'CROPGRIDSv1.05_pulsenes.nc.tif'
Grenbean_area_wd = Cropall_wd + 'CROPGRIDSv1.05_greenbean.nc.tif'
Grenbrodbean_area_wd = Cropall_wd + 'CROPGRIDSv1.05_greenbroadbean.nc.tif'
Grenpea_area_wd = Cropall_wd + 'CROPGRIDSv1.05_greenpea.nc.tif'
Stribean_area_wd = Cropall_wd + 'CROPGRIDSv1.05_stringbean.nc.tif'

Bean_pea_wd = [Bean_area_wd,Chikpea_area_wd,Cowpea_area_wd,Pigonpea_area_wd,Lentil_area_wd,Bambra_area_wd,\
               Brodbean_area_wd,Lupin_area_wd,Pea_area_wd,Pulsenes_area_wd,Grenbean_area_wd,Grenbrodbean_area_wd,\
               Grenpea_area_wd,Stribean_area_wd]

## directories of Nuts and Fruit
Harmo_cells = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Harmonize_classes')
### get the crop names belonged to fruits, nuts and vegetables
Harmo_fruit_cells = Harmo_cells['Fruit_CROPGRID']
Harmo_nut_cells = Harmo_cells['Nuts']
Harmo_vege_cells = Harmo_cells['Vegetable']

Harmo_wddt_ori = {'Fruits':Harmo_fruit_cells,'Nuts':Harmo_nut_cells,\
    'Vegetables':Harmo_vege_cells}

Harmo_wddt = {}
for i in Harmo_wddt_ori:
    Harmo_name =  Harmo_wddt_ori[i].to_dict()
    Harmo_name = Imp_func.dict_del_nan(Harmo_name)
    Harmo_wddt[i] =  Imp_func.replace_keys(Harmo_name,list(Harmo_name.values()))


Str_add_fron = Cropall_wd + 'CROPGRIDSv1.05_'
Str_add_beh = '.nc.tif'

for j in  Harmo_wddt:
    for k in Harmo_wddt[j]:
        Harmo_wddt[j][k]= Str_add_fron + k + Str_add_beh


#%%
#----------------------------------------------------processing_module----------------------------------------------------
## Aggregating all maps for Beans and peas 
# OUTPUT_DATA
Peabean_result= Imp_func.aggregate(Bean_pea_wd)

# OUTPUT_FILE
Imp_func.output_ras(Pj_path.output_wd+'Harmo_crops/Peabean.tif',Bean_pea_wd[0],\
    'EPSG:4326',Peabean_result)

#%%
## Aggregating all maps for Nuts, fruit and vegetables
# OUTPUT_FILE
for i in Harmo_wddt:
    Aggr_crop_result = Imp_func.aggregate(list(Harmo_wddt[i].values()))
    Imp_func.output_ras(Pj_path.output_wd +'Harmo_crops/'+i+'.tif',\
        list(Harmo_wddt[i].values())[0],'EPSG:4326',Aggr_crop_result)

# OUTPUT_DATA
Harmo_crop_wddt = Imp_func.dict_name_path(['Peabean','Fruits','Nuts','Vegetable'],\
    Imp_func.glob.glob(Pj_path.output_wd+'Harmo_crops/*.tif',recursive=False))
Harmo_crop_wddt = Imp_func.replace_keys(Harmo_crop_wddt,['Peabean','Fruit','Nuts','Vege'])

## Clip to the extent of Europe
# OUTPUT_FILE
for i in Harmo_crop_wddt:
    Imp_func.clip_map(Pj_path.output_prj_wd+r'Vital_crops/Vital_Cp_area/'+i+'_EFTA.tif',\
        Harmo_crop_wddt[i],Pj_path.EFTA_UK_wd)

# OUTPUT_DATA
Harmo_crop_EFTA_wddt = Imp_func.dict_name_path(['Peabean','Fruit','Nuts','Vege'],\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Vital_crops/Vital_Cp_area/*_EFTA.tif',\
    recursive=False))



#%%
#----------------------------------------------------output_module----------------------------------------------------
# SUMMARY
Harmo_crop_df = Imp_func.conv_dict2df(Harmo_crop_wddt,'Cropname','Harmo_crop_ori')
Harmo_crop_df = Imp_func.join_dict2df(Harmo_crop_df,Harmo_crop_EFTA_wddt,'Cropname','Harmo_crop_EFTA')

Imp_func.save_plk(r'../B_Output/A13.pkl',Harmo_crop_df)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
