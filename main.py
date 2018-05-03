import sys
from pandas import read_csv
import os.path
from shutil import copyfile

import api.retrain as retrain
import tensorflow as tf
from tools.RecoverableError import RecoverableError

current_dir = '{}'.format( os.getcwd() )
csv_filename = 'decor.csv'
categories_dir = 'patterns'
categories = ['country', 'decor', 'type']

def read_csv_data(file):
    if not os.path.isfile(file):
        raise RecoverableError('File {} not found.'.format(file))
    return read_csv(file, sep=',', header=0)

def make_categories_dir():
    os.makedirs(os.path.join(current_dir, categories_dir))

def get_nonspace_category_name(category):
    return category.replace(' ', '_')

def create_categories_directories(dataset):
    if not os.path.exists(categories_dir):
        make_categories_dir()

    for category in categories:
        for country in dataset[category].unique():
            country = get_nonspace_category_name(country)
            path_to_create = os.path.join(current_dir, categories_dir, country)
            if not os.path.exists(path_to_create):
                os.makedirs(path_to_create)

def put_images_in_proper_category_dirs(dataset):
    for data_row in dataset.iterrows():
        for category in categories:
            file = data_row[1].file.replace('png', 'jpg')
            copyfile(os.path.join(current_dir, 'resources', 'decor', file),
                     os.path.join(current_dir, categories_dir, get_nonspace_category_name(data_row[1][category]), file))

def prepare_dataset():
    path = os.path.join(current_dir, 'resources', csv_filename)
    dataset = read_csv_data(path)
    create_categories_directories(dataset)
    put_images_in_proper_category_dirs(dataset)


if __name__ == "__main__" :
    FLAGS, unparsed = retrain.runparser()

    try:
        prepare_dataset()
        tf.app.run(main=retrain.main, argv=[sys.argv[0]] + unparsed)
    except RecoverableError as e:
        print(e)
