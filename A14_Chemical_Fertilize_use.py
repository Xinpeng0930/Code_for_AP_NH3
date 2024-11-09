
'''
This script is aiming to get the fertilizer use by crop
This script could be run automatically. Running time is 65s.

'''

#%%
# Import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#----------------------------------------------------input_module----------------------------------------------------
#%%
start_time = Imp_func.time.time()
# Setting pathways
## Pathways for crop areas
Vital_crop_df = Imp_func.open_plk(r'../B_Output/J20.pkl') #Provides crop area data
Vital_crop_EFTA_wddt = Imp_func.conv_df2dict(Vital_crop_df,'Cropname','Final_cropmaps') #maps for crop areas

#%%
#----------------------------------------------------processing_module----------------------------------------------------
## Preprocessing the maps
#OUTPUT_DATA
###Rasterizing N use intensity maps
N_use_inten = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='crop_fertilizer_use')

'''
N_use_inten.iloc[:,4:24] = N_use_inten.iloc[:,4:24].astype(float)
Imp_func.add_field(Pj_path.EFTA_UK_wd,N_use_inten,4,24)
'''

#%%
# OUTPUT_FILE
#### we can use new method to rasterize and calculate N use intensity now, here is an example for permanent grassland

for i in Vital_crop_EFTA_wddt:
    Imp_func.cali_fig_filter(Vital_crop_EFTA_wddt[i],Pj_path.Exam_crop_reson_wd,\
        Pj_path.EFTA_UK_wd,N_use_inten, \
    'FID_1','Name_abbre',N_use_inten.columns.tolist()[list(Vital_crop_EFTA_wddt.keys()).index(i) + 4],\
    0.0833333333333333,Pj_path.output_prj_wd + 'Fertilizer_use_total/' + i +'_TferuseEFTA.tif')



#%%
#----------------------------------------------------output_module----------------------------------------------------
## Summarizing data
# SUMMARY
Vital_cropferN_wddt = Imp_func.dict_name_path(list(Vital_crop_EFTA_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd + 'Fertilizer_use_total/*_TferuseEFTA.tif',recursive=False))


Imp_func.zonal_summary(list(Vital_cropferN_wddt.keys()),\
    list(Vital_cropferN_wddt.values()),Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd + 'test_output/Fert_use_byprod.xlsx')

#%%
# SUMMARY
Chemfer_df = Imp_func.conv_dict2df(Vital_cropferN_wddt,'OSDCropname','Chemfer_use_map')
Imp_func.save_plk(r'../B_Output/A50.pkl',Chemfer_df)


'''##plotting fertilization maps
for i in Vital_cropferN_wddt:
    Imp_func.plot_formal(Vital_cropferN_wddt[i],
                Pj_path.EFTA_UK_wd,(8,10),[1,1],3035,\
                ['white', '#1A9641','#A6D96A','#FFFFC0','#FDAE61','#D7191C'],\
                [-0.01, 0.3, 1, 5, 15, Imp_func.np.inf])
'''
#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
