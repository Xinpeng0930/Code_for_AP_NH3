
'''
This script aims to calibrate liquid system livestock when the NIR number is lower than that in ClimLPS or higher but not exceeding 1 after multiplied with calibration factors.
Running time is 75s
'''
#%%
#import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
#----------------------------------------------------input_module----------------------------------------------------
start_time = Imp_func.time.time()
H84= Imp_func.open_plk(r'../B_Output/H84.pkl')
TD_liq_livstk_numb = H84['TD_liq_livestknumb']
BU_liq_livstk_numb_cali1 = H84['BU_liq_livestknumb']
Shp_countr_wddt = Imp_func.dict_name_path(Pj_path.Country_name_abbr,Pj_path.Shpwd) #country shapefiles

#%%
#----------------------------------------------------processing_module----------------------------------------------------
## calibrate the inbalanced countries after the first round calibration. Replace the data in these countries with top-down data
#OUTPUT_INTE_FILE
for i in Pj_path.Country_name_abbr:
    for j in TD_liq_livstk_numb:
        Imp_func.clip_map(Pj_path.output_prj_wd + r'Liq_livstknumb_TD_bycountr/'+ i + '_' + j + '_TDliqnumb.tif', \
            TD_liq_livstk_numb[j], Shp_countr_wddt[i])

#OUTPUT_INTE_FILE
for i in Pj_path.Country_name_abbr:
    for j in BU_liq_livstk_numb_cali1:
        Imp_func.clip_map(Pj_path.output_prj_wd + r'Liq_livestknumb_BU_Cali1_bycoutr/' + i +'_'+j+'_BUliqcali1.tif',\
            BU_liq_livstk_numb_cali1[j],Shp_countr_wddt[i])

#%%
### identify countries and livestock need to be replaced with Top-down liquid data
#OUTPUT_DATA
Iden_liq_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Liq_solid_cali_Leve')

Iden_result = []
for index, row in Iden_liq_df.iterrows():
    for col in Iden_liq_df.columns[1:]: # Skip the Name_abbre column
        if row[col] == 1:
            Iden_result.append((row["Name_abbre"],col,row[col]))

Iden_result_new = [f"{country}_{livestock}" for country, livestock, _ in Iden_result]
All_Coutr_livstk_key = [i+'_'+j for i in Pj_path.Country_name_abbr for j in TD_liq_livstk_numb]
Non_iden_result = [item for item in All_Coutr_livstk_key if item not in Iden_result_new]


TD_liq_livstk_bycountr = Imp_func.dict_name_path(Iden_result_new,\
    Imp_func.glob.glob(Pj_path.output_prj_wd + r'Liq_livstknumb_TD_bycountr/*_TDliqnumb.tif',recursive=False))

BU_liq_livstk_cali1_bycountr = Imp_func.dict_name_path(Non_iden_result,\
    Imp_func.glob.glob(Pj_path.output_prj_wd + r'Liq_livestknumb_BU_Cali1_bycoutr/*_BUliqcali1.tif',recursive=False))

Mixed_replaced_TDBU = {**TD_liq_livstk_bycountr,**BU_liq_livstk_cali1_bycountr}


#### Masaic maps by livestock
#OUTPUT_DATA
Mixed_replaced_TDBU_bylivstk_keys ={}
for i in TD_liq_livstk_numb:
    Mixed_replaced_TDBU_bylivstk_keys [i] = [keys for keys in list(Mixed_replaced_TDBU.keys()) 
                              if i in keys]


Mixed_replaced_TDBU_bylivstk_wddt = {}
for i in TD_liq_livstk_numb:
    Mixed_replaced_TDBU_bylivstk_wddt[i] = Imp_func.filter_dict(Mixed_replaced_TDBU,\
        Mixed_replaced_TDBU_bylivstk_keys[i])

#%%
#### Export the maps by livestock
#OUTPUT_INTE_FILE
for i in Mixed_replaced_TDBU_bylivstk_wddt:
    Indi_listk_list = list(Mixed_replaced_TDBU_bylivstk_wddt[i].values())
    Imp_func.mosaic_map(Indi_listk_list,\
    Pj_path.output_prj_wd+'Liq_livstknum_replace_TD/'+i+'_Liqnumb_rep.tif','EPSG:4326')

#%%
#OUTPUT_DATA
BU_liq_livstk_numb_repwddt = Imp_func.dict_name_path(Pj_path.Ani_name,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Liq_livstknum_replace_TD/*_Liqnumb_rep.tif',recursive=False))

#%%
## calibrate the countries with lower NIR data than ClimGLP (or not exceeding 100% after multiplying a factor higher than 1)
#OUTPUT_DATA
Cali_low_NIR_or_Notexcd_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='liq_lownotexcd_TD_to_BU')

#OUTPUT_FILE
for i in BU_liq_livstk_numb_repwddt:
    Imp_func.cali_fig(BU_liq_livstk_numb_repwddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,\
        Cali_low_NIR_or_Notexcd_df,'FID_1','Name_abbre',\
        i,0.0833333333333333,Pj_path.output_prj_wd+'Liq_livestknumb_BU_Cali2/'+i+'_BUliq_livstknumb_cali2.tif')

#%%
#----------------------------------------------------output_module----------------------------------------------------
## Summarize the livstock numbers in liquid systems after replacing with TD maps

#SUMMARY
Imp_func.zonal_summary(list(BU_liq_livstk_numb_repwddt.keys()),list(BU_liq_livstk_numb_repwddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/BU_liq_livestk_rep.xlsx')
#passed the test

## Summarize the livestock number in liquid systems after calibrating Bottom-up to equal lower NIR data
#SUMMARY
Liqnumb_cali2_wddt = Imp_func.dict_name_path(Pj_path.Ani_name,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Liq_livestknumb_BU_Cali2/*_BUliq_livstknumb_cali2.tif',\
        recursive=False))

Imp_func.zonal_summary(Liqnumb_cali2_wddt.keys(),Liqnumb_cali2_wddt.values(),Pj_path.EFTA_UK_wd,\
    32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/BU_liq_livstk_cali2.xlsx')
# passed the test

## Export important pathways
# SUMMARY
Imp_func.save_plk(r'../B_Output/H85.pkl',Liqnumb_cali2_wddt)


#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")