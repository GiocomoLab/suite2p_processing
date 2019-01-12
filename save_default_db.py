import numpy as np
import os

db = {
      'h5py': [], # a single h5 file path
      'h5py_key': 'data',
      'look_one_level_down': False, # whether to look in ALL subfolders when searching for tiffs
      'data_path': [], # a list of folders with tiffs
                                             # (or folder of folders with tiffs if look_one_level_down is True, or subfolders is not empty)
      'subfolders': [], # choose subfolders of 'data_path' to look in (optional)
      'fast_disk': os.path.join("E:","s2ptmp"), # string which specifies where the binary file will be stored (should be an SSD)
    }


if __name__ == '__main__':
    np.save('default_db.npy',db)
