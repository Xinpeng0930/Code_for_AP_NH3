#%%
'''
This script aims to get equivalent grazing animals based on GLPS and GLW4.0
Total running time:92s
'''
#%%
#Necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

#%%
#set directory
start_time = Imp_func.time.time()
#----------------------------------------------------input_module----------------------------------------------------
##livestock maps
G75dt= Imp_func.open_plk(r'../B_Output/G75.pkl') #file with animal number pathways
Anim_numb_wddt = Imp_func.conv_df2dict(G75dt,'Anim_type','Numb_after_cali')

##livestock system map
GLPS_ruminant_wd = r'J:/A.数据/global livestock system/2_GlobalRuminantLPS_GIS/glps_gleam_61113_10km.tif'

##grazing day ratio map
Graz_ratio_wd = Pj_path.output_prj_wd + 'Graz_ratio/grz_ratio_filled.tif'

##output directories
Name_ruminant = ['dair','othcatl','shep','goat']

'''
Name_livestock_tot = ['Pig','Dair','Oth_cattle','Potr','Sheep','Goat']
'''
#%%
#----------------------------------------------------processing_module----------------------------------------------------
## extract GLPS in Europe
#OUTPUT_INTE_FILE
Imp_func.clip_map(Pj_path.output_prj_wd + 'Anim_SYS/EFTA_UK_GLPS.tif',\
    GLPS_ruminant_wd,Pj_path.EFTA_UK_wd)


#%%
### copy an array for extracting grazing system
#### filter grazing systems
#OUTPUT_DATA
EFTA_GLPS_array = Imp_func.rasterio.open(Pj_path.output_prj_wd + 'Anim_SYS/EFTA_UK_GLPS.tif').read(1)
EFTA_Gras_array = Imp_func.deepcopy(EFTA_GLPS_array); EFTA_Mix_array = Imp_func.deepcopy(EFTA_GLPS_array); \
    EFTA_Othe_array=Imp_func.deepcopy(EFTA_GLPS_array) #(here we must use deep copy to ensure the code doesn't wrongly use the same array in the for loop)

EFTA_GLPS_array_dt = {'Graz':EFTA_Gras_array,'Mix':EFTA_Mix_array,'Othe':EFTA_Othe_array}

#%%
#OUTPUT_INTE_FILE
for i in EFTA_GLPS_array_dt:
    if i == 'Graz':
        EFTA_GLPS_array_dt[i][Imp_func.np.where((EFTA_GLPS_array_dt[i]>0)& (EFTA_GLPS_array_dt[i]<=4))] = 1
        EFTA_GLPS_array_dt[i][Imp_func.np.where(EFTA_GLPS_array_dt[i]>4)] = 0
    elif i == 'Mix':
        EFTA_GLPS_array_dt[i][Imp_func.np.where((EFTA_GLPS_array_dt[i]<= 4) | (EFTA_GLPS_array_dt[i]>12))] = 0
        EFTA_GLPS_array_dt[i][Imp_func.np.where((EFTA_GLPS_array_dt[i]>4) & (EFTA_GLPS_array_dt[i] <= 12))] = 1
    elif i =='Othe':
        EFTA_GLPS_array_dt[i][Imp_func.np.where((EFTA_GLPS_array_dt[i]< 13) | (EFTA_GLPS_array_dt[i]>= 16))] = 0
        EFTA_GLPS_array_dt[i][Imp_func.np.where((EFTA_GLPS_array_dt[i]>= 13) & (EFTA_GLPS_array_dt[i] < 16))] = 1
    Imp_func.output_ras(Pj_path.output_prj_wd + 'Anim_SYS/EFTA_UK_'+i+'.tif',Pj_path.Exam_new_wd,'EPSG:4326',EFTA_GLPS_array_dt[i])

#%%
## Extract dairy cattle from total cattle
#OUTPUT_DATA
Dair_extr_df = Imp_func.pd.read_excel(Pj_path.Fac_tab_wd,sheet_name='dair_extr_fac')

#%%
#OUTPUT_FILE
for i in ['dair','othcatl']:
    Imp_func.cali_fig_filter(Anim_numb_wddt['catl'],Pj_path.Exam_new_wd,Pj_path.EFTA_NUT2_wd,\
        Dair_extr_df,'NUTS_ID','NUTS2_ID',\
        Dair_extr_df.columns.tolist()[['dair','othcatl'].index(i)+8],0.0833333333333333,\
        Pj_path.output_prj_wd+r'Anim_numb_cali/cattle/'+i+'_numbcali.tif')
#(it's important to pair the i and the column number in the calibration dataframe)

#OUTPUT_DATA
Anim_numb_new_wddt = Imp_func.del_keys_dict(Anim_numb_wddt,['catl'])
Anim_numb_new_wddt.update({'dair':Pj_path.output_prj_wd+r'Anim_numb_cali/cattle/dair_numbcali.tif',\
    'othcatl':Pj_path.output_prj_wd+r'Anim_numb_cali/cattle/othcatl_numbcali.tif'}) 

#%%
## extract specific animals in specific systems
### extract livestock maps to ensure them have the same extents as GLPS
#OUTPUT_DATA
EFTA_GLPS_wddt = Imp_func.dict_name_path(['Graz','Mix','Oth'],\
    Imp_func.glob.glob(Pj_path.output_prj_wd + 'Anim_SYS/EFTA_UK_*.tif',recursive=False))

#OUTPUT_FILE
for i in Name_ruminant:
    for j in EFTA_GLPS_wddt:
        ### exacute the multiplition
        EFTA_livestock_GLP = Imp_func.tidy_zero(Anim_numb_new_wddt[i]) * \
            Imp_func.tidy_zero(EFTA_GLPS_wddt[j])
        Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_SYS_individual/'+i+'_'+j+'numb.tif',\
            Pj_path.Exam_new_wd,'EPSG:4326',EFTA_livestock_GLP)

# OUTPUT_DATA
EFTA_GLPS_livestock_wddt = {}
for i in Name_ruminant:
    for j in EFTA_GLPS_wddt:
        key_livestk_GLPS = i+'_'+j
        EFTA_GLPS_livestock_wddt[key_livestk_GLPS]=Imp_func.np.nan

EFTA_GLPS_livestock_wddt=Imp_func.dict_name_path(list(EFTA_GLPS_livestock_wddt.keys()),\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Anim_SYS_individual/*.tif',recursive=False))


#%%
### make the grazing days data the same resolution as other maps
# OUTPUT_INTE_FILE
Imp_func.gdal.Warp(Pj_path.output_prj_wd+r'Graz_ratio/grz_ratio_resap_ini.tif', \
                Graz_ratio_wd,dstSRS='EPSG:4326', xRes=0.08333333333333331483,yRes=0.08333333333333331483,\
                resampleAlg=Imp_func.gdal.GRA_Bilinear) # for ratios, we all use bilinear method
#(Since it doesn't have the same shape as other maps, we need to cut the map to align it with others)
Imp_func.clip_map(Pj_path.output_prj_wd+r'Graz_ratio/grz_ratio_resap.tif',\
    Pj_path.output_prj_wd+r'Graz_ratio/grz_ratio_resap_ini.tif',Pj_path.EFTA_UK_wd)

Graz_ratio_resp_wd = Pj_path.output_prj_wd+r'Graz_ratio/grz_ratio_resap.tif'
#%%
### calculate equivalent grazing livestock
#### define data input pathways
#OUTPUT_DATA
EFTA_Livestock_MO_wddt={}
EFTA_Livestock_MO_wddt = Imp_func.two_layer_dict(Name_ruminant,['Mix','Oth'],EFTA_Livestock_MO_wddt)

for i in EFTA_Livestock_MO_wddt:
    for j in EFTA_Livestock_MO_wddt[i]:
        GLPS_Livestock_key = list(EFTA_GLPS_livestock_wddt.keys())
        Match_key = i+'_'+ j
        for q in GLPS_Livestock_key:
            if Match_key in q:
                EFTA_Livestock_MO_wddt[i][j] =EFTA_GLPS_livestock_wddt[q]
#%%    
#### get the ruminants in mixed and other systems
#OUTPUT_INTE_FILE
for i in EFTA_Livestock_MO_wddt:
    Ruminant_MO_numb = Imp_func.aggregate(list(EFTA_Livestock_MO_wddt[i].values()))
    Imp_func.output_ras_filtered(Pj_path.output_prj_wd+r'Anim_Ruminant_Numb_MO/'+i+'_MO.tif',\
        Pj_path.Exam_new_wd,'EPSG:4326',Ruminant_MO_numb)

#%%
#### get the equivalent grazing animals
##### get the animals in MO and pure grazing(PGraz) systems
# OUTPUT_DATA
MO_Ruminant_wddt = Imp_func.dict_name_path(Name_ruminant,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+r'Anim_Ruminant_Numb_MO/*_MO.tif',recursive=False))

PGraz_Ruminant_wddt = {}
for i in EFTA_GLPS_livestock_wddt:
    if 'Graz' in i:
        PGraz_Ruminant_wddt[i] = EFTA_GLPS_livestock_wddt[i]

PGraz_Ruminant_wddt=Imp_func.replace_keys(PGraz_Ruminant_wddt,['dair','othcatl','shep','goat'])

##### execuate the multiplication
# OUTPUT_FILE
for i in MO_Ruminant_wddt:
     Equvalent_grazing_numb = Imp_func.tidy_zero(MO_Ruminant_wddt[i]) * Imp_func.tidy_zero(Graz_ratio_resp_wd) * 0.65 + Imp_func.tidy_zero(PGraz_Ruminant_wddt[i])
     MO_grazing_numb = Imp_func.tidy_zero(MO_Ruminant_wddt[i]) * Imp_func.tidy_zero(Graz_ratio_resp_wd) * 0.65
     MO_nongrazing_numb = Imp_func.tidy_zero(MO_Ruminant_wddt[i]) - MO_grazing_numb
     
     Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_Ruminant_Numb_EqvGraz/'+i+'_EqvGraz.tif',\
         Pj_path.Exam_new_wd,'EPSG:4326',Equvalent_grazing_numb)
     Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_Ruminant_Graz_MO/'+i+'_GrazMO.tif',\
         Pj_path.Exam_new_wd,'EPSG:4326',MO_grazing_numb)
     Imp_func.output_ras_filtered(Pj_path.output_prj_wd+'Anim_Ruminant_Nongraz_MO/'+i+'_NongrazMO.tif',\
         Pj_path.Exam_new_wd,'EPSG:4326',MO_nongrazing_numb)

# OUTPUT_DATA
EqvGraz_ruminant_wddt = Imp_func.dict_name_path(Name_ruminant,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Anim_Ruminant_Numb_EqvGraz/*_EqvGraz.tif',recursive=False))
Graz_ruminant_MOwddt = Imp_func.dict_name_path(Name_ruminant,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Anim_Ruminant_Graz_MO/*_GrazMO.tif',recursive=False))
Nongraz_ruminant_MOwddt = Imp_func.dict_name_path(Name_ruminant,\
    Imp_func.glob.glob(Pj_path.output_prj_wd+'Anim_Ruminant_Nongraz_MO/*_NongrazMO.tif',recursive=False))

#%%
#----------------------------------------------------output_module----------------------------------------------------
## Summarize the consistency bettween cattles
# SUMMARY
Imp_func.zonal_summary(list(Anim_numb_new_wddt.keys()),list(Anim_numb_new_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/AnimNUM_withDair.xlsx')
#(could compare the sum of dairy and non-dairy cattle with cattle in AniNUM_cali file)
#(we passed the test)

## Summarize animal numbers in livestock systems
# SUMMARY
Imp_func.zonal_summary(list(EFTA_GLPS_livestock_wddt.keys()),list(EFTA_GLPS_livestock_wddt.values()),\
    Pj_path.EFTA_UK_wd,32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/Ruminant_livstksys.xlsx')
#(we compared with AnimNUM_withDair. Data passed the check)

## Summarize ruminants numbers in MO systems
# SUMMARY
Imp_func.zonal_summary(list(MO_Ruminant_wddt.keys()) + [item + 'MOGraz' for item in list(Graz_ruminant_MOwddt.keys())] +\
    [item + 'MO_NonGraz' for item in list(Nongraz_ruminant_MOwddt.keys())], list(MO_Ruminant_wddt.values()) + \
    list(Graz_ruminant_MOwddt.values()) + list(Nongraz_ruminant_MOwddt.values()) ,Pj_path.EFTA_UK_wd,\
    32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/Ruminant_livstkMO.xlsx')
#(passed the check, could also compare with Runinant_livstksys)

## Summarize the number of equivalent grazing animals by livestock
# SUMMARY
Imp_func.zonal_summary(list(EqvGraz_ruminant_wddt.keys()),list(EqvGraz_ruminant_wddt.values()),Pj_path.EFTA_UK_wd,\
    32,'sum',-999,Pj_path.output_prj_excel_wd+'test_output/Ruminant_EquvGraznumb.xlsx')

## Summarize the number of grazing animals
# SUMMARY
EFTA_PUgraz_livestock_wddt = Imp_func.filter_dict(EFTA_GLPS_livestock_wddt,['dair_Graz','othcatl_Graz',\
    'shep_Graz','goat_Graz'])

Imp_func.zonal_summary(
    list(EqvGraz_ruminant_wddt.keys()) + [item + '_MOgraz' for item in list(Graz_ruminant_MOwddt.keys())] +\
    [item+'_PUgraz' for item in list(EFTA_PUgraz_livestock_wddt.keys())],\
    list(EqvGraz_ruminant_wddt.values()) + list(Graz_ruminant_MOwddt.values()) +\
    list(EFTA_PUgraz_livestock_wddt.values()),Pj_path.EFTA_UK_wd,32,'sum',-999,\
        Pj_path.output_prj_excel_wd+'test_output/Ruminant_PUMOgraz.xlsx')
#passed the check


## Summarize important pathways
# SUMMARY
EFTA_PUgraz_livestock_forcombwddt =  Imp_func.replace_keys(EFTA_PUgraz_livestock_wddt,['dair','othcatl','shep','goat'])

Rumi_byGraz_df = Imp_func.conv_dict2df(Graz_ruminant_MOwddt,'Anim_name','Graz_MO')
Rumi_byGraz_df = Imp_func.join_dict2df(Rumi_byGraz_df,Nongraz_ruminant_MOwddt,'Anim_name','Nongraz_MO')
Rumi_byGraz_df = Imp_func.join_dict2df(Rumi_byGraz_df,EFTA_PUgraz_livestock_forcombwddt,'Anim_name','Graz_PU')

G76 = {'GLPS_bytype':EFTA_GLPS_wddt,'Anim_numb':Anim_numb_new_wddt,\
    'GLP_Anim':EFTA_GLPS_livestock_wddt,'Rumi_MO':MO_Ruminant_wddt,\
    'Rumi_Equvgraz':EqvGraz_ruminant_wddt,'Rumi_byGraz':Rumi_byGraz_df}

Imp_func.save_plk(r'../B_Output/G76.pkl',G76)


#----------------------------record time spending---------------------------------
end_time = Imp_func.time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")