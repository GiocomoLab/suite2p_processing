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
        head,tail = os.path.split(f)
        s2pdir = os.path.join(head,'suite2p','plane0','stat.npy')
        if os.path.exists(s2pdir):
            return True
        else:
            return False

    # run for a single file
    def single_file(f):

        h5exists = check4h5(f)
        if not h5exists or h5_overwrite:
            h5fname = pp.sbx2h5(f)
        else:
            h5fname = f+'.h5'

        s2pexists = check4s2p(f)
        if s2p_overwrite:
            pass
        else:
            pass

        # set ops

        # set db

        # run suite2p

        # move registered binary over to save data folders

        # delete temporary files

        return None

    if isinstance(files,list) or isinstance(files,tuple):
        _=[single_file(file) for file in files]
    else:
        _=single_file(files)
