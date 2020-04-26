import os
os.sys.path.append('..')
os.sys.path.append("C:\\Users\\mplitt\\MightyMorphingPhotonRangers")
# import MightyMorphingPhotonRangers as mmpr
import preprocessing as pp
import numpy as np
from run_single_session import sbx_run_pipeline



if __name__ == '__main__':
    mice = ['4343705.1','4343705.2','4343705.3']
    # mice = ['4139266.3']
    df = pp.load_session_db(twop_dir = "G:\\My Drive\\2P_Data\\Syt3KO")
    df = df[df['RewardCount']>20]
    df = df[df['Imaging']==1]
    df = df.sort_values(['MouseName','DateTime','SessionNumber'])

    for mouse in mice:
        df_mouse = df[df['MouseName'].str.match(mouse)]
        print(mouse,df_mouse['scanmat'])
        f= []
        for i in range(df_mouse.shape[0]):
            print(df_mouse['scanmat'].iloc[i])
            #f.append(df_mouse['scanmat'].iloc[i][:-4])
            #try:
            sbx_run_pipeline(df_mouse['scanmat'].iloc[i][:-4],h5_output="E:\\")
            #except:
            #    pass
