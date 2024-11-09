'''
This script aims for getting grazing days and grazing ratios from GAINS model
This script doesn't need to run along the main data processing stream
'''


#%%
#Necessary packages
import Z_Important_functions as Imp_func
import Z_Proj_paths as Pj_path

# %%
## read all csv files
#OUTPUT_DATA
GAINS_livestk_parawd = Imp_func.glob.glob(Pj_path.Input_prj_wd+\
    'Air_pollution_database/Database_collection/GAINS/Parameters_baseline/*.csv',recursive=False)
GAINS_livestk_para_wddt = Imp_func.dict_name_path(Pj_path.Country_name_abbr,GAINS_livestk_parawd)

GAINS_para_dfdt = {}
for i in GAINS_livestk_para_wddt:
    GAINS_para_dfdt[i] = Imp_func.pd.read_csv(GAINS_livestk_para_wddt[i], error_bad_lines=False)

## create a new dataframe and extract needed data
Grazing_day_df=Imp_func.pd.DataFrame(GAINS_para_dfdt['AT'].iloc[7:16,0]).reset_index(drop=True)
for i in GAINS_livestk_para_wddt:
    Grazing_day_to_add = GAINS_para_dfdt[i].iloc[:, 0:2]
    Grazing_day_to_add.columns=['Housing periods, N-excretion, N volatilization rates and LSU factors']+\
        [i]
    Grazing_day_df=Imp_func.pd.merge(Grazing_day_df,Grazing_day_to_add,how='inner',\
        on='Housing periods, N-excretion, N volatilization rates and LSU factors')

## create a new dataframe and calculate the ratios
Grazing_ratio = Imp_func.pd.DataFrame(Grazing_day_df['Housing periods, N-excretion, N volatilization rates and LSU factors'])
for i in Grazing_day_df.columns[1:]:
    Grazing_ratio[i]=(365-Imp_func.pd.to_numeric(Grazing_day_df[i]))/365
'''### revise first rows for dairy cattle
Grazing_ratio.loc[0] = Grazing_ratio.loc[0].apply(lambda x: x * 0.8 if isinstance(x, (int, float)) else x)
Grazing_ratio.loc[1] = Grazing_ratio.loc[1].apply(lambda x: x * 0.8 if isinstance(x, (int, float)) else x)'''

#%%
## Export the ratio dataframe
# SUMMARY
Grazing_ratio.to_excel(Pj_path.output_prj_excel_wd + 'test_output/Grazing_ratios.xlsx')
