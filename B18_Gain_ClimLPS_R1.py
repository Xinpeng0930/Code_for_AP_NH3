'''
This script aims to get Bottom-up and Top-down based liquid livestock
This script could be run automatically. Running time is 35s
'''

#%%
#import necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
#----------------------------------------------------input_module----------------------------------------------------
start_time = Imp_func.time.time()
##directories of animals from NON grazing_SYSTEMS
H83 = Imp_func.open_plk(r'../B_Output/H83.pkl')
Non_grznum_wddt = Imp_func.conv_df2dict(H83,'Anim_name','MO_Nongraz_cali3')
G76 = Imp_func.open_plk(r'../B_Output/G76.pkl')
Monogastric_Anim = Imp_func.filter_dict(G76['Anim_numb'],['pig','potr'])
Non_grznum_new_wddt={**Monogastric_Anim,**Non_grznum_wddt}
Non_grznum_new_wddt = Imp_func.sort_dict_by_order(Non_grznum_new_wddt,Pj_path.Ani_name)


#%%
#----------------------------------------------------processing_module----------------------------------------------------
#OUTPUT_DATA
##obtaining the map of Top-down liquid animals. They will be the reference layers
Topdown_liquid_fac = Imp_func.pd.DataFrame(Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='liq_solid_frac_TD'))

### multiplying the factors with non-grazing animals
#OUTPUT_FILE
for j in Non_grznum_new_wddt:
    Imp_func.cali_fig_filter(Non_grznum_new_wddt[j],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,\
        Topdown_liquid_fac,'FID_1','Name_abbre',\
        Topdown_liquid_fac.columns.tolist()[list(Non_grznum_new_wddt.keys()).index(j)+3],\
        0.0833333333333333,Pj_path.output_prj_wd+'Liq_livstk_numb_TD/'+j+'_liqTD.tif')


#%%
##obtaining the map of bottom-up ratios, and we can multiply the factors with non-grazing animals and get the temperary bottom-up liquid non-grazing animals
### generating the vectors with targeted fields
#OUTPUT_DATA
Bottomup_liquid_fac = Imp_func.pd.DataFrame(Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,\
    sheet_name='liq_solid_frac_BU'))

### multiplying the factors with non-grazing animals
#OUTPUT_FILE
for i in Non_grznum_new_wddt:
    Imp_func.cali_fig_filter(Non_grznum_new_wddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_NUT2_wd,\
        Bottomup_liquid_fac,'NUTS_ID','NUTS_ID',\
        Bottomup_liquid_fac.columns.tolist()[list(Non_grznum_new_wddt.keys()).index(i)+3],\
        0.0833333333333333,Pj_path.output_prj_wd+'Liq_livstk_numb_BU_R1/'+i+'_liqBU_R1.tif')

#%%
#----------------------------------------------------output_module----------------------------------------------------
## Summarize top-down liquid animal numbers 
#SUMMARY
Liqani_TD_wddt = Imp_func.dict_name_path(list(Non_grznum_new_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Liq_livstk_numb_TD/*_liqTD.tif',recursive=False))

Imp_func.zonal_summary(list(Liqani_TD_wddt.keys()),list(Liqani_TD_wddt.values()),Pj_path.EFTA_UK_wd,\
    32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/Liqani_numb_TD.xlsx')

##Summarize bottom-up liquid animal numbers after the first round calibration
#SUMMARY
Liqani_BU_wddt =Imp_func.dict_name_path(list(Non_grznum_new_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Liq_livstk_numb_BU_R1/*_liqBU_R1.tif',recursive=False))

Imp_func.zonal_summary(list(Liqani_BU_wddt.keys()),\
    list(Liqani_BU_wddt.values()),Pj_path.EFTA_UK_wd,32,'sum',-999,
    Pj_path.output_prj_excel_wd+'test_output/Liqani_numb_BU_R1.xlsx')

## Save important pathway
#SUMMARY
H84 = {'TD_liq_livestknumb':Liqani_TD_wddt, 'BU_liq_livestknumb':Liqani_BU_wddt}
Imp_func.save_plk(r'../B_Output/H84.pkl',H84)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
