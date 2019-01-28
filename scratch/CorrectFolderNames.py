import os
from glob import glob
os.sys.path.append('..')
os.sys.path.append("C:\\Users\mplitt\MightyMorphingPhotonRangers")
# import MightyMorphingPhotonRangers as mmpr
import preprocessing as pp
import numpy as np
from run_single_session import sbx_run_pipeline




if __name__ == '__main__':
    mice = ['4139219.2', '4139219.3', '4139224.2', '4139224.3', '4139224.5',
     '4139251.1','4139251.2','4139260.1','4139260.2','4139261.2']
    df = pp.load_session_db()
    df = df[df['RewardCount']>20]
    df = df[df['Imaging']==1]
    df = df.sort_values(['MouseName','DateTime','SessionNumber'])

    for mouse in mice:
        df_mouse = df[df['MouseName'].str.match(mouse)]
        print(mouse,df_mouse['scanmat'])

        for i in range(df_mouse.shape[0]):
            print(df_mouse['scanmat'].iloc[i])
            scandir, filename = os.path.split(df_mouse['scanmat'].iloc[i])
            #sbxfiles = glob(os.path.join(scandir,'*.sbx'))

            # check if s2p directory exists
            if os.path.exists(os.path.join(scandir,'suite2p')):

                # move suite2p directory into subfolder with first files name
                newdir = df_mouse['scanmat'].iloc[i][:-4]
                os.makedirs(newdir)
                os.rename(os.path.join(scandir,'suite2p'),os.path.join(newdir,'suite2p'))



            #f.append(df_mouse['scanmat'].iloc[i][:-4])

        #sbx_run_pipeline(f,h5_output="E:\\")
