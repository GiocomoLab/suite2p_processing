import os
os.sys.path.append('..')
os.sys.path.append("C:\\Users\\mplitt\\MightyMorphingPhotonRangers")
# import MightyMorphingPhotonRangers as mmpr
import preprocessing as pp
import numpy as np
import suite2p as s2p
# from run_single_session import sbx_run_pipeline

ops={'fs':15.4609,
    'sig_baseline':10,
    'win_baseline':300,
    'tau':2.,
    'baseline':'maximin'}
df = pp.load_session_db()
df = df[df['RewardCount']>20]
df = df[df['Imaging']==1]
df = df.sort_values(['MouseName','DateTime','SessionNumber'])

if __name__ == '__main__':
    mice = ['4139219.2', '4139219.3', '4139224.2', '4139224.3', '4139224.5',
     '4139251.1','4139251.2','4139260.1','4139260.2','4139261.2','4139266.3','4139265.4',
     '4139265.3','4139265.5']

    for mouse in mice:
        if mouse in {'4139266.3','4139265.4','4139265.3','4139265.5'}:
            ops['tau']=1
        else:
            ops['tau']=2
        df_mouse = df[df['MouseName'].str.match(mouse)]
        print(mouse,df_mouse['s2pfolder'])
        for i in range(df_mouse.shape[0]):
            sess = df_mouse.iloc[i]
            spks = s2p.dcnv.oasis(np.load(os.path.join(sess['s2pfolder'],'plane0','F.npy')),ops)
            np.save(os.path.join(sess['s2pfolder'],'plane0','S.npy'),spks)
