import os
import numpy as np
import scipy.io as spio
import h5py


def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''

    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''

    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict

def sbxread(filename,k=0,N=None):
    '''
    Input: filename should be full path excluding .sbx, starting index, batch size
    By default Loads whole file at once, make sure you have enough ram available to do this
    '''
 # Check if contains .sbx and if so just truncate
    if '.sbx' in filename:
        filename = filename[:-4]

    # Load info
    info = loadmat(filename + '.mat')['info']
    #print info.keys()

    # Defining number of channels/size factor
    if info['channels'] == 1:
        info['nChan'] = 2; factor = 1
    elif info['channels'] == 2:
        info['nChan'] = 1; factor = 2
    elif info['channels'] == 3:
        info['nChan'] = 1; factor = 2

     # Determine number of frames in whole file
    max_idx = os.path.getsize(filename + '.sbx')/info['recordsPerBuffer']/info['sz'][1]*factor/4-1

     # Paramters
    #k = 0; #First frame
    if N is None:
        N = max_idx; #Last frame
    else:
        N = min([N,max_idx-k])

    nSamples = info['sz'][1] * info['recordsPerBuffer'] * 2 * info['nChan']
    #print(nSamples,N)

    # Open File
    fo = open(filename + '.sbx')


    fo.seek(k*nSamples, 0)
    x = np.fromfile(fo, dtype = 'uint16',count = int(nSamples/2*N))
    x = np.int16((x.max()-x).astype(np.int32)/np.int32(2))
    x = x.reshape((info['nChan'], info['sz'][1], info['recordsPerBuffer'], int(N)), order = 'F')

    return x

def array2h5(arr,h5fname):

    f = h5py.File(h5fname,'w')
    dset = f.create_dataset("data",data=arr)
    f.close()
    #with h5py.File(h5fname,'w') as f:
    #    dset = f.create_dataset("data",data=arr)
    return


def sbx2h5(filename):
    data = sbxread(filename)
    data = np.transpose(data[0,:,:,:] ,axes=(2,1,0))
    h5name = filename+'.h5'
    array2h5(data,h5name)
    return h5name


def default_ops():
    ops = {
           # file paths
           'look_one_level_down': False, # whether to look in all subfolders when searching for tiffs
           'fast_disk': os.path.join("E:","s2ptmp"), # used to store temporary binary file, defaults to save_path0 (set to a string NOT a list)
           'save_path0': [], # stores results, defaults to first item in data_path
           'delete_bin': False, # whether to delete binary file after processing
           'h5py_key': 'data', # key in h5 where data array is stored (data should be time x pixels x pixels)
           # main settings
           'nplanes' : 1, # each tiff has these many planes in sequence
           'nchannels' : 1, # each tiff has these many channels per plane
           'functional_chan' : 1, # this channel is used to extract functional ROIs (1-based)
           'diameter':6, # this is the main parameter for cell detection, 2-dimensional if Y and X are different (e.g. [6 12])
           'tau':  1., # this is the main parameter for deconvolution
           'fs': 15.46,  # sampling rate (total across planes)
           # output settings
           'save_mat': False, # whether to save output as matlab files
           'combined': True, # combine multiple planes into a single result /single canvas for GUI
           # parallel settings
           'num_workers': 0, # 0 to select num_cores, -1 to disable parallelism, N to enforce value
           'num_workers_roi': -1, # 0 to select number of planes, -1 to disable parallelism, N to enforce value
           # registration settings
           'do_registration': True, # whether to register data
           'nimg_init': 500, # subsampled frames for finding reference image
           'batch_size': 200, # number of frames per batch
           'maxregshift': 0.1, # max allowed registration shift, as a fraction of frame max(width and height)
           'align_by_chan' : 1, # when multi-channel, you can align by non-functional channel (1-based)
           'reg_tif': False, # whether to save registered tiffs
           'subpixel' : 10, # precision of subpixel registration (1/subpixel steps)
           # cell detection settings
           'connected': True, # whether or not to keep ROIs fully connected (set to 0 for dendrites)
           'navg_frames_svd': 5000, # max number of binned frames for the SVD
           'nsvd_for_roi': 1000, # max number of SVD components to keep for ROI detection
           'max_iterations': 20, # maximum number of iterations to do cell detection
           'ratio_neuropil': 6., # ratio between neuropil basis size and cell radius
           'ratio_neuropil_to_cell': 3, # minimum ratio between neuropil radius and cell radius
           'tile_factor': 1., # use finer (>1) or coarser (<1) tiles for neuropil estimation during cell detection
           'threshold_scaling': 1., # adjust the automatically determined threshold by this scalar multiplier
           'max_overlap': 0.75, # cells with more overlap than this get removed during triage, before refinement
           'inner_neuropil_radius': 2, # number of pixels to keep between ROI and neuropil donut
           'outer_neuropil_radius': np.inf, # maximum neuropil radius
           'min_neuropil_pixels': 350, # minimum number of pixels in the neuropil
           # deconvolution settings
           'baseline': 'maximin', # baselining mode
           'win_baseline': 60., # window for maximin
           'sig_baseline': 10., # smoothing constant for gaussian filter
           'prctile_baseline': 8.,# optional (whether to use a percentile baseline)
           'neucoeff': .7,  # neuropil coefficient
           'allow_overlap': True,
           'xrange': np.array([0, 0]),
           'yrange': np.array([0, 0]),
         }
    return ops

def set_ops(d={}):
    ops = default_ops()
    for k,v in d.items():
        ops[k]=v
    return ops

def default_db():
    db = {
      'h5py': [], # a single h5 file path
      'h5py_key': 'data',
      'fast_disk': os.path.join("E:","s2ptmp"), # string which specifies where the binary file will be stored (should be an SSD)
    }
    return db

def set_db(h5fname,d={}):
    db = default_db()
    db['h5py']=h5fname
    for k,v in d:
        db[k]=v
    return db
