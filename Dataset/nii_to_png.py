import nibabel as nib
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

def read_nii(filepath):
    '''
    Reads .nii file and returns pixel array
    '''
    ct_scan = nib.load(filepath)
    array   = ct_scan.get_fdata()
    return(array)

def create_output_dir(base_path):
    '''
    creates directory as such:
    - base_path/png
      - images
      - masks
    :return:
    '''
    try:
        png_path = os.path.join(base_path, 'png')
        png_imgs = os.path.join(png_path, 'images')
        png_masks = os.path.join(png_path, 'masks')
        os.makedirs(png_path, exist_ok=True)
        os.makedirs(png_imgs, exist_ok=True)
        os.makedirs(png_masks, exist_ok=True)
        print("Directory '%s' created successfully" % png_path)
    except OSError as error:
        print("Directory '%s' can not be created")


def convert_to_png(base_path):
    nii_imgs = os.path.join(base_path, 'nii/images')
    nii_masks = os.path.join(base_path, 'nii/masks')
    create_output_dir(base_path)
    png_imgs = os.path.join(base_path, 'png/images')
    png_masks = os.path.join(base_path, 'png/masks')
    data = []
    for img_file in os.listdir(nii_imgs):
        case = img_file[4:-4]
        os.makedirs(os.path.join(png_imgs, 'Case_' + case), exist_ok=True)
        os.makedirs(os.path.join(png_masks, 'Case_' + case), exist_ok=True)
        mask_file = 'Img_' + case + '_Labels.nii'
        # slice the nii images
        img = read_nii(os.path.join(nii_imgs, img_file))
        mask = read_nii(os.path.join(nii_masks, mask_file))
        for slice in range(img.shape[0]):
            case_list = []
            slice_img = img_file[:-4] + '_Slice_' + str(slice) + '.png'
            slice_mask = mask_file[:-4] + '_Slice_' + str(slice) + '.png'
            plt.imsave(os.path.join(png_imgs, 'Case_'+case, slice_img), np.rot90(img[slice]), cmap='bone')
            plt.imsave(os.path.join(png_masks, 'Case_' + case, slice_mask), np.rot90(mask[slice]), cmap='bone')
            case_list.extend([case, slice,
                              os.path.join(nii_imgs, img_file),
                              os.path.join(nii_masks, mask_file),
                              os.path.join(png_imgs, 'Case_' + case, slice_img),
                              os.path.join(png_masks, 'Case_' + case, slice_mask)])
            data.append(case_list)
    df = pd.DataFrame(data, columns=['case', 'slice', 'image_path (nii)', 'mask_path (nii)', 'image_slices (png)', 'mask_slices (png)'])
    df.to_csv(os.path.join(base_path, 'dataset.csv'))

if __name__ == '__main__':
    base_path = '/path_to_base_directory'
    convert_to_png(base_path)
