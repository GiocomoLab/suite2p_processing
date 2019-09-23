import suite2p
from suite2p.run_s2p import run_s2p
import s2p_preprocessing as pp
import os
import shutil

# check if h5 file exists
def check4h5(f):
    if os.path.exists(f+'.h5'):
        return True
    else:
        return False

# check if s2p results exist
def check4s2p(f):
    #head,tail = os.path.split(f)
    #s2pdir = os.path.join(head,'suite2p','plane0','stat.npy')
    s2pdir = os.path.join(f,'suite2p','plane0','stat.npy')
    if os.path.exists(s2pdir):
        return True
    else:
        return False

def sbx_run_pipeline(files, h5_overwrite = False, s2p_overwrite=False,keep_binary=True,
                    h5_output=None,ops_d={},db_d={},max_idx = None):
    '''files: sbx filename stem or list of sbx filename stems
    h5_overwrite: overwrite h5 file if it exists
    s2p_overwrite: overwrite s2p results
    keep_binary: keep registered binary to rerun s2p if needed
    ops_d: ops to change
    db_d: db settings to change'''




    # run for a single file
    def single_file(f):
        head,tail = os.path.split(f)

        s2pexists = check4s2p(f)
        if s2pexists:
            if s2p_overwrite:
                shutil.rmtree(os.path.join(head,'suite2p'))
            else:
                print("%s suite2p already done" % f)
                return None

        h5exists = check4h5(f)
        if not h5exists or h5_overwrite:
            if h5_output is None:
                h5fname = pp.sbx2h5(f,output_name = f+".h5",max_idx=max_idx)
            else:
                h5fname = pp.sbx2h5(f,output_name = os.path.join(h5_output,tail+".h5"),max_idx=max_idx)
        else:
            if h5_output is None:
                h5fname = f+'.h5'
            else:
                h5fname =  os.path.join(h5_output,tail+".h5")






        # set ops
        outpath = f
        try:
            os.makedirs(f)
        except:
            print("outpath not created")
        ops_d = {'save_path0':f}
        #ops_d['save_path0']=f
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
        if keep_binary:
            shutil.move(os.path.join(bindir,"plane0","data.bin"),os.path.join(outpath,"suite2p","data.bin"))
        # delete temporary files
        shutil.rmtree(bindir)

        return None

    if isinstance(files,list) or isinstance(files,tuple):
        _=[single_file(file) for file in files]
    else:
        _=single_file(files)
