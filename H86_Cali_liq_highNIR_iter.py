'''
This script aims to carry out the iterative algorithm to calibrate liquid system livestock
This script can be run automatically. Running time is 62s.
'''
#%%
#Necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path
import shutil

#%%
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
Liq_actual_cali2_wddt = Imp_func.open_plk(r'../B_Output/H85.pkl')
Shp_countr_wddt = Imp_func.dict_name_path(Pj_path.Country_name_abbr,Pj_path.Shpwd) #country shapefiles
G76 = Imp_func.open_plk(r'../B_Output/G76.pkl')
H83 = Imp_func.open_plk(r'../B_Output/H83.pkl')
Monogastric_Anim = Imp_func.filter_dict(G76['Anim_numb'],['pig','potr'])
Non_grznum_wddt = Imp_func.conv_df2dict(H83,'Anim_name','MO_Nongraz_cali3')
Non_grznum_new_wddt={**Monogastric_Anim,**Non_grznum_wddt}
Non_grznum_new_wddt = Imp_func.sort_dict_by_order(Non_grznum_new_wddt,Pj_path.Ani_name)

#%%
#----------------------------------------------------processing_module----------------------------------------------------
#get basic information for iterations
##obtain the country-specific clipped liquid livestock number maps from MO-nongrazing systems 
#OUTPUT_INTE_FILE
for i in Pj_path.Country_name_abbr:
    for j in Liq_actual_cali2_wddt:
        Imp_func.clip_map(Pj_path.output_prj_wd+'Liq_livestknumb_BU_Cali2_bycoutr/' +\
            i + '_' + j + '_Liqnumb_cali2.tif', \
            Liq_actual_cali2_wddt[j], Shp_countr_wddt[i])


##obtain the country-specific highest liquid system livestock number maps
### get the liquid system limiting number figures
#OUTPUT_DATA
Limt_liqsyst_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Liq_limit_ratio')

#OUTPUT_INTE_FILE
for i in Non_grznum_new_wddt:
    Imp_func.cali_fig_filter(Non_grznum_new_wddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,\
        Limt_liqsyst_df,'FID_1','Name_abbre',Limt_liqsyst_df.columns.tolist()[list(Non_grznum_new_wddt.keys()).index(i)+3],\
        0.0833333333333333,Pj_path.output_prj_wd+r'Liq_livstk_limit/'+i+'_Liqnumb_Limt.tif')


#OUTPUT_DATA
Liq_numblimt_wddt = Imp_func.dict_name_path(list(Non_grznum_new_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Liq_livstk_limit/*_Liqnumb_Limt.tif'))


### split the figures
#OUTPUT_INTE_FILE
for i in Pj_path.Country_name_abbr:
    for j in Liq_numblimt_wddt:
        Imp_func.clip_map(Pj_path.output_prj_wd+'Liq_livstk_limit_bycountr/' + i + '_' + j +'_Liqnumb_limt.tif',\
        Liq_numblimt_wddt[j],Shp_countr_wddt[i])

#%%
## identify countries and livestock need to be iteratively rescaled
#OUTPUT_DATA
Iden_liq_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Liq_solid_cali_Leve')

Iden_result = []
for index, row in Iden_liq_df.iterrows():
    for col in Iden_liq_df.columns[1:]: # Skip the Name_abbre column
        if row[col] == 3:
            Iden_result.append((row["Name_abbre"],col,row[col]))

Iden_result_new = [f"{country}_{livestock}" for country, livestock, _ in Iden_result]

#%%
##summarize the original and limiting livestock number need to be iteratively resacaled
#OUTPUT_DATA
Iter_countr_ani_actliq_wddt = Imp_func.dict_name_path(Iden_result_new,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Liq_livestknumb_BU_Cali2_bycoutr/*_Liqnumb_cali2.tif',\
        recursive=False))

Iter_countr_ani_limtliq_wddt = Imp_func.dict_name_path(Iden_result_new,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Liq_livstk_limit_bycountr/*_Liqnumb_limt.tif',\
        recursive=False))

Iter_target_value_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Liq_cali_targ')
Iter_target_value = {}
for i, row in Iter_target_value_df.iterrows():
    for col in Iter_target_value_df.columns[3:]:
        Iter_target_value [f'{row["Name_abbre"]}_{col}'] = row[col]

Iter_target_value = Imp_func.filter_dict(Iter_target_value,Iden_result_new)

for i in Iter_countr_ani_actliq_wddt:
    Actliq_num = Imp_func.tidy_zero(Iter_countr_ani_actliq_wddt[i])
    Actliq_num_sum = Imp_func.np.nansum(Actliq_num)
    Limitliq_num = Imp_func.tidy_zero(Iter_countr_ani_limtliq_wddt[i])
    Limitliq_num_sum = Imp_func.np.nansum(Limitliq_num)
    print(f"{i},actnumb: {Actliq_num_sum}, limtnumb: {Limitliq_num_sum}, targnumb:{Iter_target_value[i]}")
# (this section is used to check the relationship between actual number, limit number, and target number. So that we can identify some errors\
    # and possible changes for limit liquid shares)

#%%
## We get revised liquid system animals based on iterations
# OUTPUT_FILE
Iter_list = list(Iter_countr_ani_actliq_wddt.keys())
#Iter_list.index('IT_pig')
Iter_list = Imp_func.del_elemt_list(Iter_list,[2])

for s in Iter_list:
    ## Iterating and getting rescaling factors

    ###get national first iteration value
    Realliq_numb = Imp_func.tidy_zero(Iter_countr_ani_actliq_wddt[s]) #get the acture liquid system animal number
    Limtliq_numb = Imp_func.tidy_zero(Iter_countr_ani_limtliq_wddt[s]) # get the limit grazing number
    Ratio_Real_Limt = Realliq_numb / Limtliq_numb #see if real grazing animals are alrealy higher than that in limit layers
    Skip_grids = Imp_func.np.where((Ratio_Real_Limt >= 0.999)|Imp_func.np.isnan(Ratio_Real_Limt)) # we set gap at 0.99 but not for avoiding getting into too small rescaling values 
    Iter_grids = Imp_func.np.where(Ratio_Real_Limt < 0.999)
    Ratio_Real_Limt[Imp_func.np.where((Ratio_Real_Limt >= 0.999)| Imp_func.np.isnan(Ratio_Real_Limt))] = 0 #if higher, set it to be zero
    Max_Ratio_Reallimt = Imp_func.np.nanmax(Ratio_Real_Limt) #indentify the grid nearest to the limit grids

    rescale_value_original = 1.00 / Max_Ratio_Reallimt #and get the rescaling factor


    ###get iterationa arrays
    Realliq_numb_iter = [None] * 1000
    Judge_Animnumb = [0] *1000 #the first element is zero, but can't let all equal zero, otherwise our loop can's stop
    Rescale_value = [None] * 1000


    #we'd better keep all rounds at 5-10 rounds
    i = 0
    while Judge_Animnumb[i] < Iter_target_value[s]:
        Realliq_numb_iter[i] = Realliq_numb #get the inital real grazing number 
        Liq_aninum_iter_part1 = Imp_func.deepcopy(Realliq_numb_iter[i]) 
        Liq_aninum_iter_part1[Skip_grids]=0
        #(part1 excluded grid already reached largest grazing ratio, so it is the iterating part now which will be rescaled)
        Liq_aninum_iter_part2 = Imp_func.deepcopy(Realliq_numb_iter[i])
        Liq_aninum_iter_part2[Iter_grids] = 0
        # (part 2 exclude grid hadn't reached largest grazing ratio, so it is the constant part which already got highest grazing ratio)
        Rescale_value[i] = rescale_value_original
        Realliq_numb = Liq_aninum_iter_part1 * Rescale_value[i] + Liq_aninum_iter_part2
        
        # (get the result of the first round iteration)
        Ratio_Real_Limt = Realliq_numb / Limtliq_numb #get new ratio_real_limit for the next round
        Skip_grids = Imp_func.np.where((Ratio_Real_Limt >= 0.999)|Imp_func.np.isnan(Ratio_Real_Limt)) #prepare the locations for the next round
        Iter_grids = Imp_func.np.where(Ratio_Real_Limt < 0.999) #prepare the locations for the next round
        Ratio_Real_Limt [Imp_func.np.where((Ratio_Real_Limt >= 0.999)| Imp_func.np.isnan(Ratio_Real_Limt))] = 0
        #(adjust new ratio_real_limit)
        Max_Ratio_Reallimt = Imp_func.np.nanmax(Ratio_Real_Limt) # indentify the maximum
        rescale_value_original = 1.00 / Max_Ratio_Reallimt # get the new rescale_value for the next round
        Judge_Animnumb[i+1] = Imp_func.np.nansum(Realliq_numb)
        print(f"Judge value: {Judge_Animnumb[i+1]}, Target value: {Iter_target_value[s]}, Scaling factor: {Rescale_value[i]}, Round: {s}{i+1}")
        i= i + 1


    ## Last two-round revision
    Gap_lasttworound = Realliq_numb - Realliq_numb_iter[i-1]
    Gap_inden1 = Imp_func.deepcopy(Gap_lasttworound)
    Gap_inden1[Imp_func.np.where(Gap_inden1 > 0)] = 1 # indentifying matrix for changing grids in the last two rounds
    Gap_inden2 = Imp_func.deepcopy(Gap_inden1)
    Gap_inden2 = 1-Gap_inden2 # indentifying matrix for non-changing grids in the last two rounds

    Chang_Liqnumb = Gap_inden1 * Realliq_numb_iter[i-1] #Changed part in the last two rounds 
    Non_chang_Liqnumb = Gap_inden2 * Realliq_numb_iter[i-1] # Non-changed part in the last two rounds
    Rescale_value_final = (Iter_target_value[s] - Imp_func.np.nansum(Non_chang_Liqnumb))/Imp_func.np.nansum(Chang_Liqnumb)
    Final_liq_numb = Non_chang_Liqnumb + Chang_Liqnumb * Rescale_value_final #get rescaling factor and apply

    Last_round_sum = Imp_func.np.nansum(Realliq_numb)
    Last_sec_round_sum = Imp_func.np.nansum(Realliq_numb_iter[i-1])
    Final_sum = Imp_func.np.nansum(Final_liq_numb)
    print(f"Last_round value: {Last_round_sum}, Last second value:{Last_sec_round_sum},Final value:{Final_sum}")

    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Liq_Iter_numb/'+s+ '_Iter.tif',\
        Iter_countr_ani_actliq_wddt[s],'EPSG:4326',Final_liq_numb)

#%%
## We get revised grazing animals based on back calculations
# OUTPUT_FILE
for s in ['IT_pig']:
    shutil.copy(Iter_countr_ani_limtliq_wddt[s],Pj_path.output_prj_wd+'Liq_Iter_numb/'+s+ '_Iter.tif')

# %%
## Mosaic all sliced maps to get the whole maps
### Sort all sliced maps
# OUTPUT_FILE
Iter_sliced_maps = Imp_func.glob.glob(Pj_path.output_prj_wd+'Liq_Iter_numb/*_Iter.tif',recursive=False)

Pre_rescal_sliced_maps = Imp_func.glob.glob(Pj_path.output_prj_wd+'Liq_livestknumb_BU_Cali2_bycoutr/*_Liqnumb_cali2.tif',
                                            recursive=False)
Pre_rescal_sliced_maps = [path for path in Pre_rescal_sliced_maps
    if not any(item in path for item in Iden_result_new)]
All_rev_sliced_maps_wdlt = Iter_sliced_maps + Pre_rescal_sliced_maps

### get sliced maps by animal type
for livstk in Non_grznum_new_wddt:
    Rev_sliced_livstk_wdlt = [path for path in All_rev_sliced_maps_wdlt 
    if (livstk in path)]
    Imp_func.mosaic_map(Rev_sliced_livstk_wdlt,Pj_path.output_prj_wd+'Rev_final_liq/' +livstk+'_Rev_final_Liq.tif',\
    'EPSG:4326')

#%%
#----------------------------------------------------output_module----------------------------------------------------
## Summarize whether the calibrated rasters the same as we expected in Topdown method
# SUMMARY
Rev_liq_livstknumb_wddt = Imp_func.dict_name_path(list(Non_grznum_new_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Rev_final_liq/*_Rev_final_Liq.tif',recursive=False))

Imp_func.zonal_summary(list(Rev_liq_livstknumb_wddt.keys()),list(Rev_liq_livstknumb_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/Liq_animnumb_revfinal.xlsx')
# we compared the data with top-down calculated liquid animals. We passed the test.


## Get the maps for solid systems and check if negative values exists. If there are all positive values, we pass the test
# SUMMARY
for i in Rev_liq_livstknumb_wddt:
    Sld_livstknumb = Imp_func.tidy_zero(Non_grznum_new_wddt[i])-Imp_func.tidy_zero(Rev_liq_livstknumb_wddt[i])
    Imp_func.check_balance_ras(Sld_livstknumb,0.01,0)
    Sld_livstknumb [Imp_func.np.where(Sld_livstknumb <0)] = 0
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Sld_Animnumb/'+i+'_sld_animnumb.tif',Pj_path.Exam_new_wd,\
        'EPSG:4326',Sld_livstknumb)
# very few grids are lower than 0, but it doesn't matter the results.

## Get new revised MO_nongraz maps
#SUMMARY
Rev_sld_livstknumb_wddt = Imp_func.dict_name_path(Pj_path.Ani_name,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Sld_Animnumb/*_sld_animnumb.tif',recursive=False))

for i in Rev_liq_livstknumb_wddt:
    Rev_nongraz_numb = Imp_func.tidy_zero(Rev_liq_livstknumb_wddt[i]) + \
        Imp_func.tidy_zero(Rev_sld_livstknumb_wddt[i])
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+r'Ani_nongraz_cali_final/'+i+'rev_nongraz.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',Rev_nongraz_numb)


## Summarize important pathways
# SUMMARY
Non_graz_numb_wddt = Imp_func.dict_name_path(Pj_path.Ani_name,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Ani_nongraz_cali_final/*.tif',recursive=False))

Non_graz_liqsld_df = Imp_func.conv_dict2df(Non_graz_numb_wddt ,'Anim_numb','Rev_nongraz_livestknumb')
Non_graz_liqsld_df = Imp_func.join_dict2df(Non_graz_liqsld_df,Rev_liq_livstknumb_wddt,'Anim_numb','Rev_liq_livestknumb')
Non_graz_liqsld_df = Imp_func.join_dict2df(Non_graz_liqsld_df,Rev_sld_livstknumb_wddt,'Anim_numb','Rev_sld_livestknumb')

Imp_func.save_plk(r'../B_Output/H86.pkl',Non_graz_liqsld_df)

#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")