import os
os.sys.path.append('..')
os.sys.path.append("C:\\Users\\mplitt\\MightyMorphingPhotonRangers")
# import MightyMorphingPhotonRangers as mmpr
import preprocessing as pp
import numpy as np
from run_single_session import sbx_run_pipeline



if __name__ == '__main__':
    mice = ['4139219.2', '4139219.3', '4139224.2', '4139224.3', '4139224.5',
     '4139251.1','4139251.2','4139260.1','4139260.2','4139261.2','4139266.3','4139265.4',
     '4139265.3','4139265.5', '4139261.1',
     '4222154.1','4222154.2','4222153.1','4222153.2','4222153.3',
     '4139278.2','4222174.1','4222174.0','4222175.0','4222157.2','4222157.3','4222157.4',
     '4222169.1','4222169.2','4222169.3','4222169.4',
     '4222168.1','4222168.2']
    # mice = ['4139266.3']
    df = pp.load_session_db()
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
