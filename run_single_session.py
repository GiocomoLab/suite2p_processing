import suite2p
from suite2p.run_s2p import run_s2p
import preprocessing as pp
import os

def sbx_run_pipeline(files, h5_overwrite = False, s2p_overwrite=False,ops_d={},db_d={}):
    '''sbx filename stem or list of sbx filename stems
    overwrite h5 file if it exists
    overwrite s2p results
    ops to change
    db to change'''
    # check if h5 file exists
    def check4h5(f):
        if os.path.exists(f+'.h5'):
            return True
        else:
            return False
    # check if s2p results exist
    def check4s2p(f):
        pass

    # run for a single file
    def single_file(f):
        if h5_overwrite:
            pass
        else:
            pass

        if s2p_overwrite:
            pass
        else:
            pass

        # set ops

        # set db

        # run suite2p

        # copy registered binary over to save data folders

        return None

    if isinstance(files,list) or isinstance(files,tuple):
        _=[single_file(file) for file in files]
    else:
        single_file(files)
