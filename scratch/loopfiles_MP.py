import os
os.sys.path.append('..')
os.sys.path.append("C:\\Users\mplitt\MightyMorphingPhotonRangers")
# import MightyMorphingPhotonRangers as mmpr
import preprocessing as pp
import numpy as np
from run_single_session import sbx_run_pipeline


# mice = ['4139190.1', '4139190.3','4139212.2','4139212.4','4139219.2','4139219.3','4139224.2','4139224.3','4139224.5']
if __name__ == '__main__':
    df = pp.load_session_db()
    df = df[df['RewardCount']>20]
    df = df[df['Imaging']==1]
    df = df.sort_values(['MouseName','DateTime','SessionNumber'])

    f= []
    for i in range(df.shape[0]):
        f.append(df['scanmat'].iloc[i][:-4])

    sbx_run_pipeline(f,h5_output="E:\\")
