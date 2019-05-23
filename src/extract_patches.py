import numpy as np

'''
Takes in a N by N numpy array of a single cell and outputs the patches for that cell
Params:
full_cell: the N by N numpy array of the entire cell to be split into patches
patch_size: the size of each patch, for higher res cells increase this parameter appropiately
date: the date this cell was collected
cell_id: the id of the cell from the MODI database

Returns:
patch_list: returns as a numpy array of length Num_patches by patch_size by patch_size
metadata_list: returns as a numpy array of length num_patches containing tuples of metadata for each cell
'''
def extract_patches_single_cell(full_cell, patch_size, date, cell_id):
    if full_cell.shape[0] % patch_size != 0:
        raise ValueError('Please use an evenly divisible patch size (check x dimension of cell)')
    elif full_cell.shape[1] % patch_size != 0:
        raise ValueError('Please use an evenly divisible patch size (check y dimension of cell)')
    number_patches_x = full_cell.shape[0]//patch_size
    number_patches_y = full_cell.shape[1]//patch_size
    patch_list = []
    metadata_list = []
    for patch_xid in range(number_patches_x):
        for patch_yid in range(number_patches_y):
            cur_patch = \
            full_cell[patch_xid * number_patches_x: (patch_xid + 1) * patch_size, patch_yid * number: (patch_yid + 1) * patch_size ]
#            if not(is_mostly_water(cur_patch)): handled elsewhere
            patch_list.append(cur_patch)
            metadata_list.append((date, cell_id, patch_xid, patch_yid))
    return np.array(patch_list), np.array(metadata_list)

'''
filters out patches which are mostly water by using the low-res image only.
'''
def filter_water(low_res, high_res, metadata_list):
    if low_res.shape != high_res.shape:
        raise ValueError('Low and high res patch arrays do not have the same shape')
    idxs_mostly_land = np.array([i for i in range(low_res.shape[0]) if is_mostly_water(low_res[i])])
    filtered_low_res = low_res[idxs_mostly_land]
    filtered_high_res = high_res[idxs_mostly_land]
    filtered_metadata_list = metadata_list[idxs_mostly_land]
    return filtered_low_res, filtered_high_res, filtered_metadata_list

    
'''
TODO: Set threshold appropiately
'''
def is_mostly_water(patch, percent_threshold=50., water_threshold=-3000):
    tot_pixels = patch.shape[0] * patch.shape[1]
    land_pixels = np.sum(patch <= water_threshold)
    if land_pixels.shape[0]/tot_pixels * 100 >= percent_threshold:
        return False
    else: 
        return True

'''
makes patches for all cells and filters. Saves a block for each cell in output dir
'''
def make_patches_and_filter_all_cells(low_res_cells, high_res_cells, patch_size, low_res_amount, high_res_amount, output_dir, dates, cell_ids):

    high_res_factor = low_res_amount//high_res_amount
    for c, low_res_cell in enumerate(low_res_cells):
        low_res_patches, metadata_low = extract_patches_single_cell(low_res_cell, patch_size, dates[c], cell_ids[c])
        high_res_patches, metadata_high = extract_patches_single_cell(high_res_cells[c], high_res_factor * patch_size, dates[c], cell_ids[c])
        assert((metadata_low == metadata_high).all())
        low_res_patches, high_res_patches, metadata = filter_water(low_res_patches, high_res_patches, metadata_low)
        
        #Saving
        savename = cell_ids[c] + 'patch_size=' + str(patch_size) + 'date=' + str(dates[c])
        with open(os.path.join(output_dir, savename), 'wb') as f:
            pickle.dump((low_res_patches, high_res_patches, metadata), f)

'''
TODO: make function which aggregates the per cell patch data into larger chunks containing data 
from multiple cells
'''
def aggregate_chunks():
    pass    
        
         

