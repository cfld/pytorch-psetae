#dates is a dictionary with ints 0 to num keys with yyyy-mm-dd values
#geometry is a dictionary with keys as names contained in numpy files of 'fields', with values (#pixels, _?_, _?_) maybe height and width?
#geomfeat is a dictionary (appears to perform almost as well for both cases)
#labels have a set of keys which contain labels in a given 'nomenclature'
#sizes has the number of pixels, but does not appear to be used

import numpy as np
import json
import os
from skimage import io
import pandas as pd
import pickle


def get_data(data_dir, save_dir, bands, dates, geos, field='train'):
    # Get the dimensions of the images
    im = np.array(io.imread(f'{data_dir}/00/{dates[0]}/0_{bands[0]}_{dates[0]}.tif'))
    r, c = im.shape

    # Iterate through the geographies
    for idx_geo, geo in enumerate(geos):

        # Get ids for the train or test fields for the geography
        train_test = np.array(pd.read_csv(f'{data_dir}/{geo}/FieldIds.csv')[field])
        train_test = train_test[~np.isnan(train_test)].astype(int)

        # Get locations in image of various fields w index
        field_ids = np.array(io.imread(f'{data_dir}/{geo}/{geo[-1]}_field_id.tif')).reshape(r * c, -1)

        # Get labels for the geography
        labels = np.array(io.imread(f'{data_dir}/{geo}/{geo[-1]}_label.tif')).reshape(r * c, -1)

        # Subset fields only those locations which belong in train/test set
        in_set = np.in1d(field_ids, train_test)

        # Find pixels from flat image which belong to train/test set
        points = np.where(in_set == True)[0]

        # Find pixels from flat image labels which belong to train/test
        labels = labels[points, :]

        # Find pixels from flat image field_ids only field ids which belong to train/test
        field_ids = field_ids[points, :]

        # Data should be the length of the train/test set (pixels containing farm in train/test set)
        data = np.zeros((labels.shape[0], len(dates), len(bands)))
        for idx_date, date in enumerate(dates):
            for idx_band, band in enumerate(bands):
                im = np.array(io.imread(f'{data_dir}/{geo}/{date}/{geo[-1]}_{band}_{date}.tif'))
                im_flat = im.reshape(r * c, )
                im_farms = im_flat[points,]
                data[:, idx_date, idx_band] = im_farms

        if idx_geo == 0:
            X = data
            Y = labels
        else:
            X = np.concatenate((X, data), axis=0)
            Y = np.concatenate((Y, labels), axis=0)
    X[np.where(X == np.nan)] = 0.

    print(np.where(X == np.nan))
    data_save_dir = os.path.join(save_dir, 'DATA')
    meta_save_dir = os.path.join(save_dir, 'META')
    if os.path.isdir(data_save_dir) == False:
        os.mkdir(data_save_dir)
    if os.path.isdir(meta_save_dir) == False:
        os.mkdir(meta_save_dir)
    label_dict = {}
    for field_id in np.unique(field_ids):
        #Get location
        loc = np.where(field_id == field_ids)[0]
        #Get label
        label_dict[int(field_id)] = int(Y[loc[0]][0])
        #Save np array
        X_f = np.transpose(X[loc, :, :], (1,2,0))
        np.save(os.path.join(data_save_dir, f'{field_id}.npy'), X_f)
    label_dict_ = {}
    label_dict_['label_44class'] = label_dict
    with open(os.path.join(meta_save_dir, 'labels.json'), 'w') as f:
        json.dump(label_dict_, f)

    meanstds = [np.mean(X, axis=0), np.std(X, axis=0)]
    with open(os.path.join(save_dir, 'CV4A-meanstd.pkl'), 'wb') as f:
        pickle.dump(meanstds, f)

if __name__ == '__main__':

    save_dir = '/Users/ezekielbarnett/Documents/canfield/st-forecast/ICLR_CropDetection/CV4A_psetae_data/'
    #save_dir = '/raid/users/ebarnett/CV4A_psetae_data/'
    cv4a_dir = '/Users/ezekielbarnett/Documents/canfield/st-forecast/ICLR_CropDetection/CV4A/'
    #cv4a_dir = '/raid/users/ebarnett/CV4A/'

    bands    = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B8A', 'B11', 'B12', 'CLD']
    geos     =  ['00', '02', '03', '01']

    # Make dates JSON
    if os.path.isdir(save_dir) == False:
        os.mkdir(save_dir)
    if os.path.isdir(os.path.join(save_dir, 'META')) == False:
        os.mkdir(os.path.join(save_dir, 'META'))

    dates = next(os.walk(f'{cv4a_dir}/00/'))[1]
    dates_dict = {}
    for i in range(len(dates)):
        dates_dict[i] = dates[i]

    with open(os.path.join(save_dir, 'META', 'dates.json'), 'w') as file:
        json.dump(dates_dict, file)

    get_data(cv4a_dir, os.path.join(save_dir), bands=bands, dates=dates, geos=geos, field='train')