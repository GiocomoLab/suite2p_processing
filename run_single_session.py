import suite2p
from suite2p.run_s2p import run_s2p
import preprocessing as pp
import os
import shutil

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
        head,tail = os.path.split(f)
        if s2pexists:
            if s2p_overwrite:
                shutil.rmtree(os.path.join(head,'suite2p'))
                bindir = os.path.join(db['fast_disk'],'suite2p')
                try:
                    shutil.rmtree(bindir)
            else:
                print("%s suite2p already done" % f)
                return None


        # set ops
        ops = pp.set_ops(ops_d)

        # set db
        db = pp.set_db(h5fname,d=db_d)

        # run suite2p
        bindir = os.path.join(db['fast_disk'],'suite2p')
        try:
            shutil.rmtree(bindir)
        except:
            pass
        run_s2p(ops=ops,db=db)

        # move registered binary over to save data folders
        shutil.move(os.path.join(bindir,"plane0","data.bin"),os.path.join(head,"suite2p","data.bin"))
        # delete temporary files
        shutil.rmtree(bindir)

        return None

    if isinstance(files,list) or isinstance(files,tuple):
        _=[single_file(file) for file in files]
    else:
        _=single_file(files)
