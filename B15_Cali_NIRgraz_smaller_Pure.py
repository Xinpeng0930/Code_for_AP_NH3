'''
This script aims to calibrate the circumstance that bottom-up grazing animals in pure grazing systems greater than that from NIRs estimates.
This script also adds the extra pure grazing animals to non-grazing animal in MO systems
This script can be run automatically. Running time is 51s. 

'''
# import packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
#set directories
#----------------------------------------------------input_module----------------------------------------------------
G76 =  Imp_func.open_plk(r'../B_Output/G76.pkl') #animals by livestock systems, equvelent grazing animals, MO animals
GrazPU_Numb_wddt = Imp_func.conv_df2dict(G76['Rumi_byGraz'],'Anim_name','Graz_PU') # grazing animals from the grass-based systems
GrazMO_Numb_wddt = Imp_func.conv_df2dict(G76['Rumi_byGraz'],'Anim_name','Graz_MO') # grazing animas from mixed and other systems
NongrazMO_Numb_wddt = Imp_func.conv_df2dict(G76['Rumi_byGraz'],'Anim_name','Nongraz_MO') # Non- grazing animals from mixed and other systems

#%%
start_time = Imp_func.time.time()
#----------------------------------------------------processing_module----------------------------------------------------
## Calibrate the circumstance of lower number in top-down dataset than that in initial bottom-up dataset
### calibrate the grazing animal layers
#OUTPUT_DATA
Lowgrazing_cali_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='PUgraz_low_cali')

#OUTPUT_FILE
for i in GrazPU_Numb_wddt:
    Imp_func.cali_fig_filter(GrazPU_Numb_wddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,\
        Lowgrazing_cali_df,'FID_1','Name_abbre',\
        Lowgrazing_cali_df.columns.tolist()[list(GrazPU_Numb_wddt.keys()).index(i)+1],\
        0.0833333333333333,Pj_path.output_prj_wd+r'Anim_Ruminant_Graz_PUCali1/'+i+'_PUGraz_Cali1.tif')
#(it's important to pair the i and the column number in the calibration dataframe)

#OUTPUT_DATA
GrazPU_Numb_cali1_wddt = Imp_func.dict_name_path(list(GrazPU_Numb_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Anim_Ruminant_Graz_PUCali1/*_PUGraz_Cali1.tif',recursive=False))

### add the extra animals in orginal pure grazing systems to Non_grazing animals in MO system 
# OUTPUT_INTE_FILE
for i in GrazPU_Numb_wddt:
    Extra_PU_graz_numb = Imp_func.tidy_zero(GrazPU_Numb_wddt[i])-Imp_func.tidy_zero(GrazPU_Numb_cali1_wddt[i])
    NongrazMO_numb_cali1 = Extra_PU_graz_numb + Imp_func.tidy_zero(NongrazMO_Numb_wddt[i])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_Ruminant_Nongraz_MOCali1/'+i+'_Nongraz_MOCali1.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',NongrazMO_numb_cali1)

# OUTPUT_DATA
Nongraz_MO_Cali_wddt = Imp_func.dict_name_path(list(GrazPU_Numb_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Anim_Ruminant_Nongraz_MOCali1/*_Nongraz_MOCali1.tif',recursive=False))

#----------------------------------------------------output_module----------------------------------------------------

## Summarize the calibration of PUgrazing animals
#SUMMARY
Imp_func.zonal_summary([item + 'PUgraz_ori' for item in list(GrazPU_Numb_wddt.keys())]+\
    [item+'PUgraz_cali' for item in list(GrazPU_Numb_cali1_wddt.keys())],\
    list(GrazPU_Numb_wddt.values())+list(GrazPU_Numb_cali1_wddt.values()),Pj_path.EFTA_UK_wd,32,\
    'sum',-999,Pj_path.output_prj_excel_wd+'test_output/PU_grazcali1.xlsx')
# passed the test

## Summarize the balance of MO_Nongraz_cali+PU_graz_cali = MO_Nongraz_ini + PU_graz_ini
# SUMMARY  
Imp_func.zonal_summary([item + 'MO_Nongraz_Ini' for item in list(NongrazMO_Numb_wddt.keys())] + \
    [item + 'PU_Graz_Ini' for item in list(GrazPU_Numb_wddt.keys())] + \
    [item + 'MO_Nongraz_Cali1' for item in list(Nongraz_MO_Cali_wddt.keys())]+\
    [item + 'PU_Graz_Cali1' for item in list(GrazPU_Numb_cali1_wddt.keys())],\
    list(NongrazMO_Numb_wddt.values()) + list(GrazPU_Numb_wddt.values()) + list(Nongraz_MO_Cali_wddt.values())+\
    list(GrazPU_Numb_cali1_wddt.values()),Pj_path.EFTA_UK_wd,32,'sum','-999',Pj_path.output_prj_excel_wd+'test_output/Chek_PUgraz_Cali1.xlsx')

## Summarize important pathways got in this script
# SUMMARY
PU_GrazCali1_df = Imp_func.conv_dict2df(GrazPU_Numb_cali1_wddt,'Anim_name','PU_Graznumb_Cali1')
PU_GrazCali1_df = Imp_func.join_dict2df(PU_GrazCali1_df,Nongraz_MO_Cali_wddt,'Anim_name','MO_Nongraznumb_Cali1')

Imp_func.save_plk(r'../B_Output/H81.pkl',PU_GrazCali1_df)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
