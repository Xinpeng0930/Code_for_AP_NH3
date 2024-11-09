'''
This script aims to get emissions along the manure management chain.
This script can be run automatically. Running time is 142s.
'''

#%%
#Necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
start_time = Imp_func.time.time()

#----------------------------------------------------input_module----------------------------------------------------
I10B_dict = Imp_func.open_plk(r'../B_Output/I10B.pkl') # manure application by land and by animal dataframes
Manr_byani_df = I10B_dict['Manrapp_byani'].iloc[:, [0]].copy()
Manr_byani_Appdf = I10B_dict['Manrapp_byani']

H86 = Imp_func.open_plk(r'../B_Output/H86.pkl') # provides livestock in solid and liquid systems

##directories for liquid system animal numbers
Liq_aninum_wd = Imp_func.conv_df2dict(H86,'Anim_numb','Rev_liq_livestknumb')
Liq_aninum_wd2 = Imp_func.replace_keys(Liq_aninum_wd,['pig_liq','dair_liq','othcatl_liq','shep_liq',\
    'goat_liq','potr_liq'])

##directories for excretion factors

## TAN fractions
pig_TAN = 0.7
dair_TAN = 0.6
othcatl_TAN = 0.6
shep_TAN = 0.5
goat_TAN = 0.5
potr_TAN = 0.7

livstk_TAN_wdlt = [pig_TAN,dair_TAN,othcatl_TAN,shep_TAN,goat_TAN,potr_TAN]
livstk_TAN_wddt = dict(zip(Pj_path.Ani_name,livstk_TAN_wdlt))

##liquid housing emission factors
pig_liqhous_emifac = 0.31
dair_liqhous_emifac = 0.24
othcatl_liqhous_emifac = 0.24
shep_liqhous_emifac = 0.22
goat_liqhous_emifac = 0.22
potr_liqhous_emifac = 0.41

liq_hous_emifac_wdlt = [pig_liqhous_emifac,dair_liqhous_emifac,othcatl_liqhous_emifac,shep_liqhous_emifac,\
                           goat_liqhous_emifac,potr_liqhous_emifac]
liq_hous_emifac_wddt = dict(zip(Pj_path.Ani_name,liq_hous_emifac_wdlt))
liq_hous_emifac_wddt2 = Imp_func.replace_keys(liq_hous_emifac_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq',\
    'goat_liq','potr_liq'])

##liquid storage emission factors
###NH3 emission factors
pig_liqstor_emifac = 0.11
dair_liqstor_emifac = 0.25
othcatl_liqstor_emifac = 0.25
shep_liqstor_emifac = 0.3
goat_liqstor_emifac = 0.3
potr_liqstor_emifac = 0.14

liq_stor_emifac_wdlt = [pig_liqstor_emifac,dair_liqstor_emifac,othcatl_liqstor_emifac,shep_liqstor_emifac,\
                           goat_liqstor_emifac,potr_liqstor_emifac]

liq_stor_emifac_wddt = dict(zip(Pj_path.Ani_name,liq_stor_emifac_wdlt))
liq_stor_emifac_wddt2 = Imp_func.replace_keys(liq_stor_emifac_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq',\
    'goat_liq','potr_liq'])

###N2 and NO emission factors
pig_liqstor_N2NOemifac =0.0031
dair_liqstor_N2NO_emifac =0.0031
othcatl_liqstor_N2NO_emifac =0.0031
shep_liqstor_N2NO_emifac =0.0031
goat_liqstor_N2NO_emifac =0.0031
potr_liqstor_N2NO_emifac =0.0031

liq_stor_N2NOemifac_wdlt = [pig_liqstor_N2NOemifac,dair_liqstor_N2NO_emifac,othcatl_liqstor_N2NO_emifac,\
                               shep_liqstor_N2NO_emifac,goat_liqstor_N2NO_emifac,potr_liqstor_N2NO_emifac]

liq_stor_N2NOemifac_wddt = dict(zip(Pj_path.Ani_name,liq_stor_N2NOemifac_wdlt))
liq_stor_N2NOemifac_wddt2 = Imp_func.replace_keys(liq_stor_N2NOemifac_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq',\
    'goat_liq','potr_liq'])

###N2O emission factors
pig_liqstor_N2O_emifac = 0
dair_liqstor_N2O_emifac = 0.01
othcatl_liqstor_N2O_emifac = 0.01
shep_liqstor_N2O_emifac = 0.02
goat_liqstor_N2O_emifac = 0.02
potr_liqstor_N2O_emifac = 0

liq_str_N2Oemifac_wdlt = [pig_liqstor_N2O_emifac,dair_liqstor_N2O_emifac,othcatl_liqstor_N2O_emifac,shep_liqstor_N2O_emifac,\
                          goat_liqstor_N2O_emifac,potr_liqstor_N2O_emifac]

liq_str_N2Oemifac_wddt = dict(zip(Pj_path.Ani_name,liq_str_N2Oemifac_wdlt))
liq_stor_N2Oemifac_wddt2 = Imp_func.replace_keys(liq_str_N2Oemifac_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq',\
    'goat_liq','potr_liq'])

##liquid APPLICATION emission factors
#pig_liqapp_emifac = 0.35 #eea 2019 data
pig_liqapp_emifac = 0.18
# dair_liqapp_emifac = 0.55 #eea 2019 data
# othcatl_liqapp_emifac = 0.55 #eea 2019 data
dair_liqapp_emifac = 0.25
othcatl_liqapp_emifac = 0.25
shep_liqapp_emifac = 0.9
goat_liqapp_emifac = 0.9
potr_liqapp_emifac = 0.69

liq_app_emifac_wdlt = [pig_liqapp_emifac,dair_liqapp_emifac,othcatl_liqapp_emifac,shep_liqapp_emifac,goat_liqapp_emifac,\
                       potr_liqapp_emifac]

liq_app_emifac_wddt = dict(zip(Pj_path.Ani_name,liq_app_emifac_wdlt))
liq_app_emifac_wddt2 = Imp_func.replace_keys(liq_app_emifac_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq',\
    'goat_liq','potr_liq'])

##directories for solid system animal numbers
Solid_aninum_wd = Imp_func.conv_df2dict(H86,'Anim_numb','Rev_sld_livestknumb')
Solid_aninum_wd2 = Imp_func.replace_keys(Solid_aninum_wd,['pig_sld','dair_sld','othcatl_sld','shep_sld',\
    'goat_sld','potr_sld'])

##solid housing emission factors
pig_solidhous_emifac = 0.235
dair_solidhous_emifac = 0.08
othcatl_solidhous_emifac = 0.08
shep_solidhous_emifac = 0.22
goat_solidhous_emifac = 0.22
potr_solidhous_emifac = 0.205

solid_hous_emifac_wdlt = [pig_solidhous_emifac,dair_solidhous_emifac,othcatl_solidhous_emifac,shep_solidhous_emifac,\
                           goat_solidhous_emifac,potr_solidhous_emifac]
solid_hous_emifac_wddt = dict(zip(Pj_path.Ani_name,solid_hous_emifac_wdlt))
solid_hous_emifac_wddt2 = Imp_func.replace_keys(solid_hous_emifac_wddt,['pig_sld','dair_sld','othcatl_sld','shep_sld',\
    'goat_sld','potr_sld'])

##solid storage emission factors
###NH3 emission factors
pig_solidstor_emifac = 0.29
dair_solidstor_emifac = 0.32
othcatl_solidstor_emifac = 0.32
shep_solidstor_emifac = 0.3
goat_solidstor_emifac = 0.3
potr_solidstor_emifac = 0.19

solid_stor_emifac_wdlt = [pig_solidstor_emifac,dair_solidstor_emifac,othcatl_solidstor_emifac,shep_solidstor_emifac,\
                           goat_solidstor_emifac,potr_solidstor_emifac]

solid_stor_emifac_wddt = dict(zip(Pj_path.Ani_name,solid_stor_emifac_wdlt))
solid_stor_emifac_wddt2 = Imp_func.replace_keys(solid_stor_emifac_wddt,['pig_sld','dair_sld','othcatl_sld','shep_sld',\
    'goat_sld','potr_sld'])

###N2 and NO emission factors
pig_solidstor_N2NOemifac =0.31
dair_solidstor_N2NO_emifac =0.31
othcatl_solidstor_N2NO_emifac =0.31
shep_solidstor_N2NO_emifac =0.31
goat_solidstor_N2NO_emifac =0.31
potr_solidstor_N2NO_emifac =0.31

solid_stor_N2NOemifac_wdlt = [pig_solidstor_N2NOemifac,dair_solidstor_N2NO_emifac,othcatl_solidstor_N2NO_emifac,\
                               shep_solidstor_N2NO_emifac,goat_solidstor_N2NO_emifac,potr_solidstor_N2NO_emifac]

solid_stor_N2NOemifac_wddt = dict(zip(Pj_path.Ani_name,solid_stor_N2NOemifac_wdlt))
solid_stor_N2NOemifac_wddt2 = Imp_func.replace_keys(solid_stor_N2NOemifac_wddt,['pig_sld','dair_sld','othcatl_sld','shep_sld',\
    'goat_sld','potr_sld'])

###N2O emission factors
pig_solidstor_N2O_emifac = 0.01
dair_solidstor_N2O_emifac = 0.02
othcatl_solidstor_N2O_emifac = 0.02
shep_solidstor_N2O_emifac = 0.02
goat_solidstor_N2O_emifac = 0.02
potr_solidstor_N2O_emifac = 0

solid_str_N2Oemifac_wdlt = [pig_solidstor_N2O_emifac,dair_solidstor_N2O_emifac,othcatl_solidstor_N2O_emifac,shep_solidstor_N2O_emifac,\
                          goat_solidstor_N2O_emifac,potr_solidstor_N2O_emifac]

solid_str_N2Oemifac_wddt = dict(zip(Pj_path.Ani_name,solid_str_N2Oemifac_wdlt))
solid_str_N2Oemifac_wddt2 = Imp_func.replace_keys(solid_str_N2Oemifac_wddt,['pig_sld','dair_sld','othcatl_sld','shep_sld',\
    'goat_sld','potr_sld'])


##solid APPLICATION emission factors
pig_solidapp_emifac = 0.45
dair_solidapp_emifac = 0.68
othcatl_solidapp_emifac = 0.68
shep_solidapp_emifac = 0.9
goat_solidapp_emifac = 0.9
potr_solidapp_emifac = 0.43

solid_app_emifac_wdlt = [pig_solidapp_emifac,dair_solidapp_emifac,othcatl_solidapp_emifac,shep_solidapp_emifac,goat_solidapp_emifac,\
                       potr_solidapp_emifac]

solid_app_emifac_wddt = dict(zip(Pj_path.Ani_name,solid_app_emifac_wdlt))
solid_app_emifac_wddt2 = Imp_func.replace_keys(solid_app_emifac_wddt,['pig_sld','dair_sld','othcatl_sld','shep_sld',\
    'goat_sld','potr_sld'])


##directories of applied manure N
manrN_app_wd_ori = Imp_func.glob.glob(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Manur_app/*.tif',recursive = False)

manrN_name = ['liq_pig','liq_dair','liq_othcatl','liq_shep','liq_goat','liq_potr',\
                  'solid_pig','solid_dair','solid_othcatl','solid_shep','solid_goat','solid_potr']

manrN_app_mapwddt =  Imp_func.dict_name_path(manrN_name,manrN_app_wd_ori)
manrN_app_mapwd = list(manrN_app_mapwddt.values())


#%%
#------------------------------------------------processing module---------------------------------------------
##calculating emissions for liquid sytems
#OUTPUT_DATA
Excre_fac = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Excre_fac')

for i in Liq_aninum_wd:
    Imp_func.cali_fig_filter(Liq_aninum_wd[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,Excre_fac,\
        'FID_1','Name_abbre',Excre_fac.columns.tolist()[list(Liq_aninum_wd.keys()).index(i)+1],\
        0.0833333333333333,Pj_path.output_prj_wd+r'/Manure_excr/liq_' + i + '_clip.tif')

Anim_manrexcr_wddt = Imp_func.dict_name_path(Pj_path.Ani_name,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'/Manure_excr/liq_*_clip.tif',recursive=False))

for i in Anim_manrexcr_wddt:
    liq_manrN = Imp_func.tidy_zero(Anim_manrexcr_wddt[i])
    livstk_TAN = livstk_TAN_wddt[i]
    liq_hous_emifac = liq_hous_emifac_wddt[i]
    ### housing emissions
    liq_livstk_housemi = liq_manrN * livstk_TAN * liq_hous_emifac
    ### storage emissions
    liq_livstk_stoemi = liq_manrN * livstk_TAN * (1 - liq_hous_emifac) * liq_stor_emifac_wddt[i]
    liq_livstk_N2NON2Ostoemi = liq_manrN * livstk_TAN * (1 - liq_hous_emifac) *\
                               (liq_str_N2Oemifac_wddt[i] + liq_stor_N2NOemifac_wddt[i])
    ### applied TAN                           
    liq_livstk_appTAN = liq_manrN  * livstk_TAN *  (1 - liq_hous_emifac) * \
        (1-liq_stor_emifac_wddt[i] - liq_str_N2Oemifac_wddt[i] - liq_stor_N2NOemifac_wddt[i]) 
    #(this TAN data is for calculating emissions by crop)
    ### application N flow
    liq_livstk_appN = liq_manrN * livstk_TAN  * (1 - liq_hous_emifac) * \
        (1-liq_stor_emifac_wddt[i] - liq_str_N2Oemifac_wddt[i] - liq_stor_N2NOemifac_wddt[i]) +\
        liq_manrN * (1-livstk_TAN) *(1-liq_str_N2Oemifac_wddt[i] - liq_stor_N2NOemifac_wddt[i])
    #(Note: since the result of first part is TAN but not N, we have to convert it back to N, and since
    # the part of non-TAN nitrogen hasn't been emitted, we need to add them when accounting nitrogen)
    ### Get the ratio of applied TAN and applied N
    Ratio_TAN_N = liq_livstk_appTAN/liq_livstk_appN
    ### application emissions
    liq_livstk_appemi = liq_manrN * livstk_TAN * (1 - liq_hous_emifac) * \
                        (1-liq_stor_emifac_wddt[i] - liq_str_N2Oemifac_wddt[i] - liq_stor_N2NOemifac_wddt[i]) * \
                        liq_app_emifac_wddt[i]
    
    #OUTPUT_FILE
    ###outputing and cutting maps
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manur_emi_housing_storage_orig appli/Manur_housing_emi/liq_' + i + '_housemi_clip.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',liq_livstk_housemi)

    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manur_emi_housing_storage_orig appli/Manur_stora_emi/liq_' + i + '_storemi_clip.tif', \
        Pj_path.Exam_new_wd,'EPSG:4326',liq_livstk_stoemi)

    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manur_emi_housing_storage_orig appli/Manur_appli_emi/liq_' + i + '_appemi_clip.tif',\
       Pj_path.Exam_new_wd,'EPSG:4326',liq_livstk_appemi)
    
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Ratio_TAN/liq_' + i +'_RatioTAN.tif',Pj_path.Exam_new_wd, 'EPSG:4326',Ratio_TAN_N)
    
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manur_app/liq_' + i + '_Marapp_clip.tif',Pj_path.Exam_new_wd,\
        'EPSG:4326',liq_livstk_appN)
    
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manr_appTAN/liq_' + i + '_MarappTAN_clip.tif',Pj_path.Exam_new_wd,'EPSG:4326',\
        liq_livstk_appTAN)

#%%
## calculating emissions for solid sytems
#OUTPUT_DATA
for i in Solid_aninum_wd:
    Imp_func.cali_fig_filter(Solid_aninum_wd[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,Excre_fac,\
    'FID_1','Name_abbre',Excre_fac.columns.tolist()[list(Solid_aninum_wd.keys()).index(i)+1],\
    0.0833333333333333,Pj_path.output_prj_wd+r'/Manure_excr/solid_' + i + '_clip.tif')

Anim_manrexcrsld_wddt = Imp_func.dict_name_path( list(Solid_aninum_wd.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'/Manure_excr/solid_*_clip.tif',recursive=False))


for i in Solid_aninum_wd:
    solid_manrN = Imp_func.tidy_zero(Anim_manrexcrsld_wddt[i])
    livstk_TAN = livstk_TAN_wddt[i]
    solid_hous_emifac = solid_hous_emifac_wddt[i]
    ### housing emissions
    solid_livstk_housemi = solid_manrN  * livstk_TAN * solid_hous_emifac
    ### storage emissions
    solid_livstk_stoemi = solid_manrN  * livstk_TAN * (1 - solid_hous_emifac) * solid_stor_emifac_wddt[i]
    solid_livstk_N2NON2Ostoemi = solid_manrN  * livstk_TAN * (1 - solid_hous_emifac) *\
                               (solid_str_N2Oemifac_wddt[i] + solid_stor_N2NOemifac_wddt[i])
    ### Application TAN
    solid_livstk_appTAN = solid_manrN  * livstk_TAN * (1 - solid_hous_emifac) * \
                        (1-solid_stor_emifac_wddt[i] - solid_str_N2Oemifac_wddt[i] - solid_stor_N2NOemifac_wddt[i])
    #(this TAN data is for calculating emissions by crop)
    ### application emissions
    solid_livstk_appemi = solid_manrN * livstk_TAN * (1 - solid_hous_emifac) * \
                        (1-solid_stor_emifac_wddt[i] - solid_str_N2Oemifac_wddt[i] - solid_stor_N2NOemifac_wddt[i]) * \
                        solid_app_emifac_wddt[i]
    
    solid_livstk_appN = solid_manrN * livstk_TAN *  (1 - solid_hous_emifac) * \
                        (1-solid_stor_emifac_wddt[i] - solid_str_N2Oemifac_wddt[i] - solid_stor_N2NOemifac_wddt[i]) +\
                        solid_manrN * (1-livstk_TAN) * (1-solid_str_N2Oemifac_wddt[i] - solid_stor_N2NOemifac_wddt[i])
 
    #(Note: since (Note: since the result of first part is TAN but not N, we have to convert it back to N, and since
    # the part of non-TAN nitrogen hasn't been emitted, we need to add them when accounting nitrogen)
    ### The ratio of applied TAN to applied N
    Ratio_TAN_N = solid_livstk_appTAN/solid_livstk_appN
    
    #OUTPUT_FILE
    ###outputing and cutting maps
    
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manur_emi_housing_storage_orig appli/Manur_housing_emi/solid_' + i + '_housemi_clip.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',solid_livstk_housemi)
    
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manur_emi_housing_storage_orig appli/Manur_stora_emi/solid_' + i + '_storemi_clip.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',solid_livstk_stoemi)

    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manur_emi_housing_storage_orig appli/Manur_appli_emi/solid_' + i + '_appemi_clip.tif', \
        Pj_path.Exam_new_wd,'EPSG:4326', solid_livstk_appemi)

    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manr_appTAN/solid_' + i + '_MarappTAN_clip.tif',Pj_path.Exam_new_wd,\
        'EPSG:4326',solid_livstk_appTAN)
    
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Manur_app/solid_' + i + '_Marapp_clip.tif',Pj_path.Exam_new_wd,\
        'EPSG:4326',solid_livstk_appN)
    
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd + '/Ratio_TAN/solid_' + i + '_RatioTAN.tif',Pj_path.Exam_new_wd, \
        'EPSG:4326',Ratio_TAN_N)

#%%
#----------------------------------------------------output_module----------------------------------------------------
#OUTPUT_DATA
## summarize the manure N excreted in house
Anim_Liqmanrexcr_wddt2 = Imp_func.replace_keys(Anim_manrexcr_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq',\
    'goat_liq','potr_liq'])
Anim_Sldmanrexcr_wddt2 = Imp_func.replace_keys(Anim_manrexcrsld_wddt,['pig_sld','dair_sld','othcatl_sld','shep_sld',\
    'goat_sld','potr_sld'])

Ani_excr_for_summary_excel = {**Anim_Liqmanrexcr_wddt2,**Anim_Sldmanrexcr_wddt2}

# SUMMARY
Imp_func.zonal_summary(list(Ani_excr_for_summary_excel.keys()),list(Ani_excr_for_summary_excel.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999, Pj_path.output_prj_excel_wd+r'test_output/Manur_excr_N.xlsx')


#%%
#OUTPUT_DATA
## summarizing the manure N emitted in house
### construct the list of maps
manrN_hous_wd_ori = Imp_func.glob.glob(Pj_path.output_prj_wd + '/Manur_emi_housing_storage_orig appli/Manur_housing_emi/*.tif',\
    recursive = False)
manrN_hous_mapwddt =  Imp_func.dict_name_path(manrN_name,manrN_hous_wd_ori)


#SUMMARY
### execute the summary function
Imp_func.zonal_summary(list(manrN_hous_mapwddt.keys()),list(manrN_hous_mapwddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd+r'test_output/Manur_hous_N.xlsx')

#%%
#SUMMARY
## summarizing the manure N emitted in the storage stage
### construct the list of maps
Stormap_patten = Pj_path.output_prj_wd + r'/Manur_emi_housing_storage_orig appli/Manur_stora_emi/*.tif'
manrN_stor_wd_ori = [file for file in Imp_func.glob.glob(Stormap_patten, recursive=False) if 'N2NON2O' not in file]

#manrN_storN2NON2O_wd_ori = [file for file in Imp_func.glob.glob(Stormap_patten, recursive=False) if 'N2NON2O' in file]
# len(manrN_storN2NON2O_wd_ori)

manrN_stor_mapwddt =  Imp_func.dict_name_path(manrN_name,manrN_stor_wd_ori)
#manrN_storN2NON2O_mapwddt = Imp_func.dict_name_path(manrN_name,manrN_storN2NON2O_wd_ori)

manrN_stor_mapwd = list(manrN_stor_mapwddt.values())
#manrN_storN2NON2O_mapwd = list(manrN_storN2NON2O_mapwddt.values())

### execute the summary function
Imp_func.zonal_summary(manrN_name,manrN_stor_mapwd,Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd+r'test_output/Manur_stor_NH3_N.xlsx')
'''Imp_func.zonal_summary(manrN_name,manrN_storN2NON2O_mapwd,Pj_path.EFTA_UK_wd,32,'sum',\
    r'E:/Code/Res_prj/Paper_PhD/Air_pollution/B_Output/test_output/Manur_stor_N2NON2O_N.xlsx')'''


# %%
#SUMMARY
## summarizing the manure N applied to land
Imp_func.zonal_summary(manrN_name,manrN_app_mapwd,Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd+r'test_output/Manur_app_N.xlsx')


#%%
## summarizing the manure N emitted in the application stage
#OUTPUT_DATA
### construct the list of maps
manrN_appliemi_wd_ori = Imp_func.glob.glob(Pj_path.output_prj_wd + '/Manur_emi_housing_storage_orig appli/Manur_appli_emi/*.tif',\
    recursive = False)

manrN_appliemi_mapwddt =  Imp_func.dict_name_path(manrN_name,manrN_appliemi_wd_ori)
# len(manrN_hous_mapwddt)
manrN_appliemi_mapwd = list(manrN_appliemi_mapwddt.values())

#SUMMARY
### execute the summary function
Imp_func.zonal_summary(manrN_name,manrN_appliemi_mapwd,Pj_path.EFTA_UK_wd,32,'sum',-999,\
    r'E:/Code/Res_prj/Paper_PhD/Air_pollution/B_Output/test_output/Manur_appli_NH3_N.xlsx')

#Nice! we passed the manure chain N check

#%%
#OUTPUT_DATA
#Export animal-based pathways

Ani_num = {**Liq_aninum_wd2,**Solid_aninum_wd2}
Ani_manr_df = Imp_func.conv_dict2df(Ani_num,'Ani_manr_type','Ani_num')


Ani_excr = {**Anim_Liqmanrexcr_wddt2,**Anim_Sldmanrexcr_wddt2}
Ani_manr_df = Imp_func.join_dict2df(Ani_manr_df,Ani_excr,'Ani_manr_type','Manr_excr')
Hous_emi_fac = {**liq_hous_emifac_wddt2,**solid_hous_emifac_wddt2}
Ani_manr_df = Imp_func.join_dict2df(Ani_manr_df,Hous_emi_fac,'Ani_manr_type','Hous_Emifac')
Stor_emi_fac = {**liq_stor_emifac_wddt2,**solid_stor_emifac_wddt2}
Ani_manr_df = Imp_func.join_dict2df(Ani_manr_df,Stor_emi_fac,'Ani_manr_type','Stor_Emifac')
App_emi_fac = {**liq_app_emifac_wddt2,**solid_app_emifac_wddt2}
Ani_manr_df = Imp_func.join_dict2df(Ani_manr_df,App_emi_fac,'Ani_manr_type','App_Emifac')


Hous_emi_wddt = Imp_func.dict_name_path(manrN_name,\
    Imp_func.glob.glob(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Manur_emi_housing_storage_orig appli/Manur_housing_emi/*.tif',recursive=False))
Hous_emi_wddt2 = Imp_func.replace_keys(Hous_emi_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq','goat_liq','potr_liq',\
    'pig_sld','dair_sld','othcatl_sld','shep_sld','goat_sld','potr_sld'])
Stor_emi_wddt = Imp_func.dict_name_path(manrN_name,\
    Imp_func.glob.glob(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Manur_emi_housing_storage_orig appli/Manur_stora_emi/*_storemi_clip.tif',recursive=False))
Stor_emi_wddt2 = Imp_func.replace_keys(Stor_emi_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq','goat_liq','potr_liq',\
    'pig_sld','dair_sld','othcatl_sld','shep_sld','goat_sld','potr_sld'])
Ani_manr_df = Imp_func.join_dict2df(Ani_manr_df,Hous_emi_wddt2,'Ani_manr_type','Hous_emi_wddt')
Ani_manr_df = Imp_func.join_dict2df(Ani_manr_df,Stor_emi_wddt2,'Ani_manr_type','Stor_emi_wddt')


App_Sld_N_wddt = Imp_func.dict_name_path(manrN_name,\
    Imp_func.glob.glob(Pj_path.output_prj_wd + '/Manur_app/solid_*_Marapp_clip.tif',recursive=False))
App_Sld_N_wddt2 = Imp_func.replace_keys(App_Sld_N_wddt,['pig_sld','dair_sld','othcatl_sld','shep_sld',\
    'goat_sld','potr_sld'])
App_Liq_N_wddt = Imp_func.dict_name_path(manrN_name,\
    Imp_func.glob.glob(Pj_path.output_prj_wd + '/Manur_app/liq_*_Marapp_clip.tif',recursive=False))
App_Liq_N_wddt2 = Imp_func.replace_keys(App_Liq_N_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq','goat_liq','potr_liq'])
App_N_wddt = {**App_Liq_N_wddt2,**App_Sld_N_wddt2}


App_TAN_wddt = Imp_func.dict_name_path(manrN_name,\
    Imp_func.glob.glob(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Manr_appTAN/*.tif',recursive = False))
App_TAN_wddt2 = Imp_func.replace_keys(App_TAN_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq','goat_liq','potr_liq',\
    'pig_sld','dair_sld','othcatl_sld','shep_sld','goat_sld','potr_sld'])
Ratio_TAN_wddt = Imp_func.dict_name_path(manrN_name,\
    Imp_func.glob.glob(r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/Ratio_TAN/*.tif',recursive = False))
Ratio_TAN_wddt2 = Imp_func.replace_keys(Ratio_TAN_wddt,['pig_liq','dair_liq','othcatl_liq','shep_liq','goat_liq','potr_liq',\
    'pig_sld','dair_sld','othcatl_sld','shep_sld','goat_sld','potr_sld'])
manrN_appliemi_mapwddt2 = Imp_func.replace_keys(manrN_appliemi_mapwddt,['pig_liq','dair_liq','othcatl_liq','shep_liq','goat_liq','potr_liq',\
    'pig_sld','dair_sld','othcatl_sld','shep_sld','goat_sld','potr_sld'])

Manr_byani_Appdf = Imp_func.conv_dict2df(App_N_wddt,'Ani_manr_type','App_manr_N')
Manr_byani_Appdf = Imp_func.join_dict2df(Manr_byani_Appdf,App_TAN_wddt2,'Ani_manr_type','App_manr_TAN')
Manr_byani_Appdf = Imp_func.join_dict2df(Manr_byani_Appdf,Ratio_TAN_wddt2,'Ani_manr_type','Ratio_TAN')
Manr_byani_Appdf = Imp_func.join_dict2df(Manr_byani_Appdf,manrN_appliemi_mapwddt2,'Ani_manr_type','App_manr_emi')

#OUTPUT_FILE
H89_dict = {'Manr_mana_df':Ani_manr_df,\
    'Manr_app_df':Manr_byani_Appdf}

Imp_func.save_plk(r'../B_Output/H89.pkl',H89_dict)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
