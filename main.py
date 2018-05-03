from pandas import read_csv
import os.path
from shutil import copyfile

from tools.RecoverableError import RecoverableError


def read_csv_data(file):
    if not os.path.isfile(file):
        raise RecoverableError('File {} not found.'.format(file))
    return read_csv(file, sep=',', header=0)

def make_categories_dir():
    os.makedirs(os.path.join(current_dir, categories_dir))

def create_categories_directories(dataset):
    if not os.path.exists(categories_dir):
        make_categories_dir()

    categories = ['country', 'decor']
    for category in categories:
        for country in dataset[category].unique():
            path_to_create = os.path.join(current_dir, categories_dir, country)
            if not os.path.exists(path_to_create):
                os.makedirs(path_to_create)

def put_images_in_proper_category_dirs(dataset):
    categories = ['country', 'decor']
    for data_row in dataset.iterrows():
        for category in categories:
            copyfile(os.path.join(current_dir, 'resources', 'decor', data_row[1].file),
                     os.path.join(current_dir, categories_dir, data_row[1][category], data_row[1].file))

current_dir = '{}'.format( os.getcwd() )
csv_filename = 'decor.csv'
categories_dir = 'patterns'

def main():
    path = os.path.join(current_dir, 'resources', csv_filename)
    dataset = read_csv_data(path)
    create_categories_directories(dataset)
    put_images_in_proper_category_dirs(dataset)

if __name__ == "__main__" :
    try:
        main()
    except RecoverableError as e:
        print(e)
