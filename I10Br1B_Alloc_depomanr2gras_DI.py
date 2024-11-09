'''
This manuscript aims to allocate manure deposited on grassland to specific grasses based on their areas

'''


#%%
# Import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path


#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
# Load important data
I11_dict = Imp_func.open_plk(r'../B_Output/I10B.pkl')
Manrinput_byland_df = I11_dict['Manrapp_byland'] #get manure N going to grassland
Manrinput_byland_wddt = Imp_func.conv_df2dict(Manrinput_byland_df,'land_type','ori_manrbyland_map')
Manrinput_grassland_wd = Manrinput_byland_wddt['Grass_manrapp']


H87_dt = Imp_func.open_plk(r'../B_Output/H87.pkl') #get manure N deposited in grazing areas
Manr_graz_excrN_wddt = Imp_func.conv_df2dict(H87_dt,'Anim_name','Graz_ExcrN')

J20_dict = Imp_func.open_plk(r'../B_Output/J20.pkl') #provides crop maps
Crop_area_wddt = Imp_func.conv_df2dict(J20_dict,'Cropname','Final_cropmaps')
Gras_area_wddt = Imp_func.filter_dict(Crop_area_wddt,['Tempgra','Permgra'])
#get areas of permanent grass and temporary grass
Crop_area_only_wddt = Imp_func.del_keys_dict(Crop_area_wddt,['Tempgra','Permgra'])


#%%
#----------------------------------------------------processing_module----------------------------------------------------
# Get the comparison between deposited manure N and total input N to grassland
#OUTPUT_DATA
ManureN_depost_graz = Imp_func.aggregate(list(Manr_graz_excrN_wddt.values()))

# Get the share of each grass and corresponding manure N
Gras_area_tot_value = Imp_func.aggregate(list(Gras_area_wddt.values()))
Gras_area_shar = {'Tempgra':None,'Permgra':None}
Gras_area_manrN = {'Tempgra':None,'Permgra':None}

#%%
#OUTPUT_FILE
for i in Gras_area_wddt:
    Area_indiv_gras = Imp_func.tidy_zero(Gras_area_wddt[i])
    Shar_indiv_area = Area_indiv_gras/Gras_area_tot_value
    Shar_indiv_area[Imp_func.np.isnan(Shar_indiv_area)]=0
    Gras_area_shar[i] = Shar_indiv_area
    Gras_area_manrN[i] = Shar_indiv_area * ManureN_depost_graz
    
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Manur_depo_bygras_realDI/'+i+'_graz_depo.tif',\
        Pj_path.Exam_crop_reson_wd,'EPSG:4326',Gras_area_manrN[i])

#%%
#OUTPUT_DATA
Grazdepo_bygras_wddt = Imp_func.dict_name_path(['Tempgra','Permgra'],\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Manur_depo_bygras_realDI/*_graz_depo.tif',recursive=False))

ManrNdepo_by_grass_df =Imp_func.conv_dict2df(Grazdepo_bygras_wddt,'Cropname','Manr_depoN_by_plant')

Imp_func.save_plk(r'../B_Output/I10Br1B.pkl',ManrNdepo_by_grass_df)

#----------------------------------------------------output_module----------------------------------------------------

