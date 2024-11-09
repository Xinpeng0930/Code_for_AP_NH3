'''
This script aims to iteratively rescale bottom-up grazing animals in MO systems, so that
bottom-up grazing animals are in line with that based on top-down NIR based grazing animals

This script can be run automatically. Total running time is 107s.
'''

#%%
#Necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
#----------------------------------------------------input_module----------------------------------------------------
#set directories
start_time = Imp_func.time.time()
##directories of animals from MO SYSTEMS
H82 = Imp_func.open_plk(r'../B_Output/H82.pkl')
MO_Graz_cali1 = Imp_func.conv_df2dict(H82,'Anim_name','MO_Graznumb_Cali1')
MO_Nongraz_cali2 = Imp_func.conv_df2dict(H82,'Anim_name','MO_Nongraznumb_Cali2')
## (directories of actual grazing animals in MO systems)
Shp_countr_wddt = Imp_func.dict_name_path(Pj_path.Country_name_abbr,Pj_path.Shpwd) #country shapefiles
G76 = Imp_func.open_plk(r'../B_Output/G76.pkl')
MO_Rumi_Oriwddt = G76['Rumi_MO']
Rumi_Ori_tot_wddt = Imp_func.filter_dict(G76['Anim_numb'],['dair','othcatl','shep','goat'])
Rumi_Ori_tot_wddt = Imp_func.sort_dict_by_order(Rumi_Ori_tot_wddt,['dair','othcatl','shep','goat'])

H81 = Imp_func.open_plk(r'../B_Output/H81.pkl')
PU_Graz_cali1_wddt = Imp_func.conv_df2dict(H81,'Anim_name','PU_Graznumb_Cali1')


##directories of output maps
output_MOgrazanim_bycoutr = Pj_path.output_prj_wd+ r'MOgraz_num_bycountr/'
output_MOgrazlimt_bycountr = Pj_path.output_prj_wd+ r'MOgraz_limt_bycountr/'


'''## directories of grazing time
Ratio_grztime_wd = r'E:/工作学习2/Online_work/1.Air_pollution/Air_polu_prj/grz_ratio_filled.tif'
Ratio_grz_wd =r'K:/Default_database/raster/Rt_realgrz.tif'
'''

#%%

#----------------------------------------------------processing_module----------------------------------------------------
#get basic information for iterations
##obtain the country-specific clipped grazing livestock number maps from MO systems 
#OUTPUT_INTE_FILE
for i in Pj_path.Country_name_abbr:
    for j in MO_Graz_cali1:
        Imp_func.clip_map(output_MOgrazanim_bycoutr + i + '_' + j + '_MOgraz.tif', \
            MO_Graz_cali1[j], Shp_countr_wddt[i])


##obtain the country-specific highest MO grazing livestock number maps
### get the grazing limiting number figures
#OUTPUT_DATA
Limt_graz_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Graz_limit_ratio')

#OUTPUT_INTE_FILE
for i in MO_Rumi_Oriwddt:
    Imp_func.cali_fig_filter(MO_Rumi_Oriwddt[i],Pj_path.Exam_new_wd,Pj_path.EFTA_UK_wd,\
        Limt_graz_df,'FID_1','Name_abbre',Limt_graz_df.columns.tolist()[list(MO_Rumi_Oriwddt.keys()).index(i)+1],\
        0.0833333333333333,Pj_path.output_prj_wd+r'Anim_Ruminant_Graz_MOlimit/'+i+'_MOGraz_Limt.tif')

#OUTPUT_DATA
MO_Rumi_Grazlimt_wddt = Imp_func.dict_name_path(list(MO_Rumi_Oriwddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Anim_Ruminant_Graz_MOlimit/*_MOGraz_Limt.tif'))


### split the figures
#OUTPUT_INTE_FILE
for i in Pj_path.Country_name_abbr:
    for j in MO_Rumi_Grazlimt_wddt:
        Imp_func.clip_map(output_MOgrazlimt_bycountr + i + '_' + j +'_MOgraz_limt.tif',\
            MO_Rumi_Grazlimt_wddt[j],Shp_countr_wddt[i])

#%%
## identify countries and livestock need to be iteratively rescaled
#OUTPUT_DATA
Iden_graz_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Graz_cali_leve')

Iden_result = []
for index, row in Iden_graz_df.iterrows():
    for col in Iden_graz_df.columns[1:]: # Skip the Name_abbre column
        if row[col] == 3:
            Iden_result.append((row["Name_abbre"],col,row[col]))

Iden_result_new = [f"{country}_{livestock}" for country, livestock, _ in Iden_result]

#%%
##summary the original and limiting livestock number need to be iteratively resacaled
#OUTPUT_DATA
Iter_countr_ani_actgraz_wddt = Imp_func.dict_name_path(Iden_result_new,\
    Imp_func.glob.glob(output_MOgrazanim_bycoutr + '*_MOgraz.tif'))

Iter_countr_ani_limtgraz_wddt = Imp_func.dict_name_path(Iden_result_new,\
    Imp_func.glob.glob(output_MOgrazlimt_bycountr + '*_MOgraz_limt.tif'))

Iter_target_value_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='Graz_cali_targ')
Iter_target_value = {}
for i, row in Iter_target_value_df.iterrows():
    for col in Iter_target_value_df.columns[1:]:
        Iter_target_value [f'{row["Name_abbre"]}_{col}'] = row[col]

Iter_target_value = Imp_func.filter_dict(Iter_target_value,Iden_result_new)

for i in Iter_countr_ani_actgraz_wddt:
    Actgraz_num = Imp_func.tidy_zero(Iter_countr_ani_actgraz_wddt[i])
    Actgraz_num_sum = Imp_func.np.nansum(Actgraz_num)
    Limitgraz_num = Imp_func.tidy_zero(Iter_countr_ani_limtgraz_wddt[i])
    Limitgraz_num_sum = Imp_func.np.nansum(Limitgraz_num)
    print(f"{i},actnumb: {Actgraz_num_sum}, limtnumb: {Limitgraz_num_sum}, targnumb:{Iter_target_value[i]}")

#%%
## We get revised grazing animals based on iterations
# OUTPUT_FILE
Iter_list = list(Iter_countr_ani_actgraz_wddt.keys())
Iter_list = Imp_func.del_elemt_list(Iter_list,[11,12,28])

for s in Iter_list:
    ## Iterating and getting rescaling factors

    ###get national first iteration value
    Realgrz_numb = Imp_func.tidy_zero(Iter_countr_ani_actgraz_wddt[s]) #get the acture grazing number
    Limtgrz_numb = Imp_func.tidy_zero(Iter_countr_ani_limtgraz_wddt[s]) # get the limit grazing number
    Ratio_Real_Limt = Realgrz_numb / Limtgrz_numb #see if real grazing animals are alrealy higher than that in limit layers
    Skip_grids = Imp_func.np.where((Ratio_Real_Limt >= 0.999)|Imp_func.np.isnan(Ratio_Real_Limt)) # we set gap at 0.99 but not for avoiding getting into too small rescaling values 
    Iter_grids = Imp_func.np.where(Ratio_Real_Limt < 0.999)
    Ratio_Real_Limt[Imp_func.np.where((Ratio_Real_Limt >= 0.999)| Imp_func.np.isnan(Ratio_Real_Limt))] = 0 #if higher, set it to be zero
    Max_Ratio_Reallimt = Imp_func.np.nanmax(Ratio_Real_Limt) #indentify the grid nearest to the limit grids

    rescale_value_original = 1.00 / Max_Ratio_Reallimt #and get the rescaling factor


    ###get iterationa arrays
    Realgrz_numb_iter = [None] * 1000
    Judge_Animnumb = [0] *1000 #the first element is zero, but can't let all equal zero, otherwise our loop can's stop
    Rescale_value = [None] * 1000


    #we'd better keep all rounds at 5-10 rounds
    i = 0
    while Judge_Animnumb[i] < Iter_target_value[s]:
        Realgrz_numb_iter[i] = Realgrz_numb #get the inital real grazing number 
        Graz_aninum_iter_part1 = Imp_func.deepcopy(Realgrz_numb_iter[i]) 
        Graz_aninum_iter_part1[Skip_grids]=0
        #(part1 excluded grid already reached largest grazing ratio, so it is the iterating part now which will be rescaled)
        Graz_aninum_iter_part2 = Imp_func.deepcopy(Realgrz_numb_iter[i])
        Graz_aninum_iter_part2[Iter_grids] = 0
        # (part 2 exclude grid hadn't reached largest grazing ratio, so it is the constant part which already got highest grazing ratio)
        Rescale_value[i] = rescale_value_original
        Realgrz_numb = Graz_aninum_iter_part1 * Rescale_value[i] + Graz_aninum_iter_part2
        
        # (get the result of the first round iteration)
        Ratio_Real_Limt = Realgrz_numb / Limtgrz_numb #get new ratio_real_limit for the next round
        Skip_grids = Imp_func.np.where((Ratio_Real_Limt >= 0.999)|Imp_func.np.isnan(Ratio_Real_Limt)) #prepare the locations for the next round
        Iter_grids = Imp_func.np.where(Ratio_Real_Limt < 0.999) #prepare the locations for the next round
        Ratio_Real_Limt [Imp_func.np.where((Ratio_Real_Limt >= 0.999)| Imp_func.np.isnan(Ratio_Real_Limt))] = 0
        #(adjust new ratio_real_limit)
        Max_Ratio_Reallimt = Imp_func.np.nanmax(Ratio_Real_Limt) # indentify the maximum
        rescale_value_original = 1.00 / Max_Ratio_Reallimt # get the new rescale_value for the next round
        Judge_Animnumb[i+1] = Imp_func.np.nansum(Realgrz_numb)
        print(f"Judge value: {Judge_Animnumb[i+1]}, Target value: {Iter_target_value[s]}, Scaling factor: {Rescale_value[i]}, Round: {s}{i+1}")
        i= i + 1


    ## Last two-round revision
    Gap_lasttworound = Realgrz_numb - Realgrz_numb_iter[i-1]
    Gap_inden1 = Imp_func.deepcopy(Gap_lasttworound)
    Gap_inden1[Imp_func.np.where(Gap_inden1 > 0)] = 1 # indentifying matrix for changing grids in the last two rounds
    Gap_inden2 = Imp_func.deepcopy(Gap_inden1)
    Gap_inden2 = 1-Gap_inden2 # indentifying matrix for non-changing grids in the last two rounds


    Chang_Graznumb = Gap_inden1 * Realgrz_numb_iter[i-1] #Changed part in the last two rounds 
    Non_chang_Graznumb = Gap_inden2 * Realgrz_numb_iter[i-1] # Non-changed part in the last two rounds
    Rescale_value_final = (Iter_target_value[s] - Imp_func.np.nansum(Non_chang_Graznumb))/Imp_func.np.nansum(Chang_Graznumb)
    Final_graz_numb = Non_chang_Graznumb + Chang_Graznumb * Rescale_value_final #get rescaling factor and apply

    Last_round_sum = Imp_func.np.nansum(Realgrz_numb)
    Last_sec_round_sum = Imp_func.np.nansum(Realgrz_numb_iter[i-1])
    Final_sum = Imp_func.np.nansum(Final_graz_numb)
    print(f"Last_round value: {Last_round_sum}, Last secround value:{Last_sec_round_sum},Final value:{Final_sum}")

    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Graz_Iter_numb/'+s+ '_Iter.tif',\
        Iter_countr_ani_actgraz_wddt[s],'EPSG:4326',Final_graz_numb)

#%%
## We get revised grazing animals based on back calculations
# OUTPUT_FILE
for s in ['EL_shep','EL_goat','HR_goat']:
    Limt_livstk_numb = Imp_func.tidy_zero(Iter_countr_ani_limtgraz_wddt[s])
    Limt_livstk_numb_sum = Imp_func.np.nansum(Limt_livstk_numb)
    Target_numb_sum = Iter_target_value[s]
    Rescale_fac = Target_numb_sum / Limt_livstk_numb_sum
    Final_livstk_numb = Limt_livstk_numb * Rescale_fac 

    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Graz_Iter_numb/'+s+ '_Iter.tif',\
        Iter_countr_ani_actgraz_wddt[s],'EPSG:4326',Final_livstk_numb)

# %%
## Mosaic all sliced maps to get the whole maps
### Sort all sliced maps
# OUTPUT_FILE
Iter_sliced_maps = Imp_func.glob.glob(Pj_path.output_prj_wd+'Graz_Iter_numb/*_Iter.tif',recursive=False)
Pre_rescal_sliced_maps = Imp_func.glob.glob(output_MOgrazanim_bycoutr + '*_MOgraz.tif')
Pre_rescal_sliced_maps = [path for path in Pre_rescal_sliced_maps
    if not any(item in path for item in Iden_result_new)]
All_rev_sliced_maps_wdlt = Iter_sliced_maps + Pre_rescal_sliced_maps

### get sliced maps by animal type
for livstk in MO_Graz_cali1:
    Rev_sliced_livstk_wdlt = [path for path in All_rev_sliced_maps_wdlt 
    if (livstk in path)]
    Imp_func.mosaic_map(Rev_sliced_livstk_wdlt,Pj_path.output_prj_wd+'Rev_final_grazMO/' +livstk+'_Rev_final_grazMO.tif',\
    'EPSG:4326')

#%%
#----------------------------------------------------output_module----------------------------------------------------
## Summarize the number of revised grazing animals
# SUMMARY
Rev_grazMO_wddt = Imp_func.dict_name_path(list(MO_Graz_cali1.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Rev_final_grazMO/*_Rev_final_grazMO.tif',recursive=False))

Imp_func.zonal_summary(list(Rev_grazMO_wddt.keys()),list(Rev_grazMO_wddt.values()),Pj_path.EFTA_UK_wd,\
    32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/Ruminant_GrazingMO_Revfinal.xlsx')
# we can add numbers in this sheet with grazing numbers in PU_grazing systems, then compare the sum with top-down grazing animals
# we passed the test because all animal specific grazing numbers are above 99% of top-down grazing numbers

## Summarize the livestock numbers in non-grazing systems in MO systems
# SUMMARY
###(we need to get how many numbers we increased in the revised MO grazing systems compared to previously calibrated MO grazing maps\
    # so we have MO_nongrazcali3 = MO_nongrazcali2 + MO_grazcali1 -Rev_final_grazMO)
for i in Rev_grazMO_wddt:
    MO_nongraz_cali3 = Imp_func.tidy_zero(MO_Nongraz_cali2[i]) + Imp_func.tidy_zero(MO_Graz_cali1[i])-\
        Imp_func.tidy_zero(Rev_grazMO_wddt[i]) 
    Imp_func.check_balance_ras(MO_nongraz_cali3,0.01,0) # passed the balance test, no grids with large negative values
    MO_nongraz_cali3[Imp_func.np.where(MO_nongraz_cali3<0)] = 0
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_Ruminant_Nongraz_MOCali3/'+i+'_Nongraz_MOCali3.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',MO_nongraz_cali3)

# SUMMARY
## Check the balance: MO_total(after adding non_graz from PUgrazing systems) =\
    # MO_nongraz_cali2 + MO_agrz_cali1 = MO_graz_rev + MO_nongraz_cali3
MO_Nongraz_cali3_wddt = Imp_func.dict_name_path(list(Rev_grazMO_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Anim_Ruminant_Nongraz_MOCali3/*_Nongraz_MOCali3.tif',recursive=False))    

Imp_func.zonal_summary(['MO_Nongraz_cali2_' + item for item in list(MO_Nongraz_cali2.keys())]+\
    ['MO_Graz_cali1_' + item for item in list(MO_Graz_cali1.keys())] + \
    ['MO_Nongraz_cali3_' + item for item in list(MO_Nongraz_cali3_wddt.keys())] +\
    ['MO_Graz_revfial_' + item for item in list(Rev_grazMO_wddt.keys())],\
    list(MO_Nongraz_cali2.values())+list(MO_Graz_cali1.values())+list(MO_Nongraz_cali3_wddt.values())+\
    list(Rev_grazMO_wddt.values()),Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd+'test_output/Chek_MOgraz_nongraz_lasttworound_adj.xlsx')
# We passed the test

## Check the balance: PU_cali + MO_graz_rev + MO_nongraz_cali3 = total animals
# SUMMARY
Imp_func.zonal_summary(['PU_graz_cali_' + item for item in list(PU_Graz_cali1_wddt.keys())]+\
    ['MO_Graz_revfial_' + item for item in list(Rev_grazMO_wddt.keys())] + \
    ['MO_Nongraz_cali3_' + item for item in list(MO_Nongraz_cali3_wddt.keys())]+\
    ['Tot_'+item for item in list(Rumi_Ori_tot_wddt.keys())],\
    list(PU_Graz_cali1_wddt.values())+list(Rev_grazMO_wddt.values())+list(MO_Nongraz_cali3_wddt.values())+\
    list(Rumi_Ori_tot_wddt.values()),Pj_path.EFTA_UK_wd,32,'sum',-999,\
    Pj_path.output_prj_excel_wd+ 'test_output/Chek_Totgraz_rev.xlsx')
#passed the test, the ratios between disaggregated data and total data are above 99%.

## Collect important exporting pathways
MOGraz_rev_df = Imp_func.conv_dict2df(Rev_grazMO_wddt,'Anim_name','Rev_grazMO_final')
MOGraz_rev_df = Imp_func.join_dict2df(MOGraz_rev_df,PU_Graz_cali1_wddt,'Anim_name','PU_graz_cali1')
MOGraz_rev_df = Imp_func.join_dict2df(MOGraz_rev_df,MO_Nongraz_cali3_wddt,'Anim_name','MO_Nongraz_cali3')

Imp_func.save_plk(r'../B_Output/H83.pkl',MOGraz_rev_df)
#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
