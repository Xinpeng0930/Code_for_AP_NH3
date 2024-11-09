'''
This script aims to calibrate the condition that more grazing animals in bottom-up MO systems than that in top-down grazing animals. 
We also add the extra grazing animals to MO non-grazing layer
This script can be run automatically. Running time is 51s. 
'''
#%%
#Necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
# set input directories
H81 = Imp_func.open_plk(r'../B_Output/H81.pkl') # newly calibrated MO and PU grazing animals
G76 =  Imp_func.open_plk(r'../B_Output/G76.pkl') #animals by livestock systems, equvelent grazing animals, MO animals
GrazMO_Numb_wddt = Imp_func.conv_df2dict(G76['Rumi_byGraz'],'Anim_name','Graz_MO') # grazing animas from mixed and other systems
Non_GrazMO_Numb_cali1_wddt = Imp_func.conv_df2dict(H81,'Anim_name','MO_Nongraznumb_Cali1') #Non-grazing animals from mixed and other systems


#%%
#----------------------------------------------------processing_module----------------------------------------------------
## Calibrate the circumstance of lower number in top-down dataset than that in initial bottom-up dataset
### calibrate the grazing animal layers
#OUTPUT_DATA
LowgrazingMO_cali_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='MOgraz_low_cali')

#OUTPUT_FILE
for i in GrazMO_Numb_wddt:
    Imp_func.cali_fig_filter(GrazMO_Numb_wddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,\
        LowgrazingMO_cali_df,'FID_1','FID_1',\
        LowgrazingMO_cali_df.columns.tolist()[list(GrazMO_Numb_wddt.keys()).index(i)+1],\
        0.0833333333333333,Pj_path.output_prj_wd+r'Anim_Ruminant_Graz_MOCali1/'+i+'_MOGraz_Cali1.tif')
#(it's important to pair the i and the column number in the calibration dataframe)

#OUTPUT_DATA
GrazMO_Numb_cali1_wddt = Imp_func.dict_name_path(list(GrazMO_Numb_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Anim_Ruminant_Graz_MOCali1/*_MOGraz_Cali1.tif',recursive=False))

#%%
### add the extra animals in orginal MO grazing systems to Non_grazing animals in MO systems 
# OUTPUT_INTE_FILE
for i in GrazMO_Numb_wddt:
    Extra_MO_graz_numb = Imp_func.tidy_zero(GrazMO_Numb_wddt[i])-Imp_func.tidy_zero(GrazMO_Numb_cali1_wddt[i])
    NongrazMO_numb_cali2 = Extra_MO_graz_numb + Imp_func.tidy_zero(Non_GrazMO_Numb_cali1_wddt[i])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_Ruminant_Nongraz_MOCali2/'+i+'_Nongraz_MOCali2.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',NongrazMO_numb_cali2)

# OUTPUT_DATA
Nongraz_MO_Cali2_wddt = Imp_func.dict_name_path(list(GrazMO_Numb_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Anim_Ruminant_Nongraz_MOCali2/*_Nongraz_MOCali2.tif',recursive=False))


#----------------------------------------------------output_module----------------------------------------------------

## Summarize the calibration of MOgrazing animals
#SUMMARY
Imp_func.zonal_summary([item + 'MOgraz_ori' for item in list(GrazMO_Numb_wddt.keys())]+\
    [item+'MOgraz_cali' for item in list(GrazMO_Numb_cali1_wddt.keys())],\
    list(GrazMO_Numb_wddt.values())+list(GrazMO_Numb_cali1_wddt.values()),Pj_path.EFTA_UK_wd,32,\
    'sum',-999,Pj_path.output_prj_excel_wd+'test_output/MO_grazcali1.xlsx')
# passed the test

## Summarize the balance of MO_Nongraz_cali1+MO_graz_ini = MO_Nongraz_cali2 + MO_graz_cali1
# SUMMARY  
Imp_func.zonal_summary([item + 'MO_Nongraz_Cali1' for item in list(Non_GrazMO_Numb_cali1_wddt.keys())] + \
    [item + 'MO_Graz_Ini' for item in list(GrazMO_Numb_wddt.keys())] + \
    [item + 'MO_Nongraz_Cali2' for item in list(Nongraz_MO_Cali2_wddt.keys())]+\
    [item + 'MO_Graz_Cali1' for item in list(GrazMO_Numb_cali1_wddt.keys())],\
    list(Non_GrazMO_Numb_cali1_wddt.values()) + list(GrazMO_Numb_wddt.values()) + list(Nongraz_MO_Cali2_wddt.values())+\
    list(GrazMO_Numb_cali1_wddt.values()),Pj_path.EFTA_UK_wd,32,'sum','-999',Pj_path.output_prj_excel_wd+'test_output/Chek_MOgraz_Cali1.xlsx')

## Summarize important pathways got in this script
# SUMMARY
MO_GrazCali1_df = Imp_func.conv_dict2df(GrazMO_Numb_cali1_wddt,'Anim_name','MO_Graznumb_Cali1')
MO_GrazCali1_df = Imp_func.join_dict2df(MO_GrazCali1_df,Nongraz_MO_Cali2_wddt,'Anim_name','MO_Nongraznumb_Cali2')

Imp_func.save_plk(r'../B_Output/H82.pkl',MO_GrazCali1_df)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
