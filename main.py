import sys

import shutil
from pandas import read_csv
import os.path
from shutil import copyfile

import api.retrain as retrain
import api.label_image as label
from tools.RecoverableError import RecoverableError

current_dir = '{}'.format( os.getcwd() )
csv_filename = 'decor.csv'
categories_dir = 'patterns'
output_dir = 'output'
bottlenecks_dir = 'bottlenecks'
summaries_dir = 'summaries'
categories = ['country', 'decor', 'type']

def logger(msg):
    print(msg)

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
        for item in dataset[category].unique():
            item = get_nonspace_category_name(item)
            path_to_create = os.path.join(current_dir, categories_dir,category, item)
            if not os.path.exists(path_to_create):
                os.makedirs(path_to_create)

def put_images_in_proper_category_dirs(dataset):
    for data_row in dataset.iterrows():
        for category in categories:
            #copy jpg files instead of png for this moments
            file = data_row[1].file.replace('png', 'jpg')
            copyfile(os.path.join(current_dir, 'resources', 'decor', file),
                     os.path.join(current_dir, categories_dir, category, get_nonspace_category_name(data_row[1][category]), file))

def prepare_dataset():
    logger('preparing dataset')
    path = os.path.join(current_dir, 'resources', csv_filename)
    logger('reading csv data')
    dataset = read_csv_data(path)
    logger('done')
    create_categories_directories(dataset)
    logger('created categories directories successfully')
    put_images_in_proper_category_dirs(dataset)
    logger('copied files to proper locations')


def main_loop():
    while True:
        commands = [[1,'Training'], [2,'Test labeling'], [3,'Clear all'], [4, 'Exit']]
        mode = input(''.join(['{} - {}\n'.format(index, command) for [index, command] in commands]) + '\n')
        try:
            if mode == '1':
                prepare_dataset() #prepares dirs hierarchy and copies images to categories directories

                FLAGS, unparsed = retrain.runparser()
                for category in categories:
                    print('learning category {}'.format(category))
                    FLAGS.output_labels = os.path.join(current_dir, output_dir, category, 'trained_labels.txt')
                    FLAGS.output_graph = os.path.join(current_dir, output_dir, category, 'trained_graph.pb')
                    FLAGS.bottleneck_dir = os.path.join(current_dir, output_dir, category, bottlenecks_dir)
                    FLAGS.summaries_dir = os.path.join(current_dir, output_dir, category, summaries_dir)
                    FLAGS.image_dir = os.path.join(current_dir, categories_dir, category )
                    retrain.FLAGS = FLAGS
                    retrain.main([sys.argv[0]] + unparsed)
            elif mode == '2':
                filename = input('File to label [just name without an extension]\n')
                filename = os.path.join(current_dir, 'resources', 'decor', filename+'.jpg')
                if not os.path.exists(filename):
                    raise RecoverableError('File to label name is incorrect. [{}]'.format(filename))

                args = label.parse_arguments()
                most_plaussible_results = dict()
                for category in categories:
                    print('Category: {}'.format(category))
                    args.graph = os.path.join(current_dir, output_dir, category, 'trained_graph.pb')
                    args.labels = os.path.join(current_dir, output_dir, category, 'trained_labels.txt')
                    most_plaussible_results[category] = label.try_label(args, image_to_label=filename, display_all_results = True)
                print('{}\nThis image has been assigned to categories:\n{}\n{}\n'.
                      format('*'*20 ,
                             '\n'.join(['\t{} => {}, probability {}.'.format(cat, res[0], res[1]) for (cat,res) in most_plaussible_results.items()]),
                             '*' * 20))
            elif mode == '3':
                try:
                    shutil.rmtree(os.path.join(current_dir, 'patterns'))
                    shutil.rmtree(os.path.join(current_dir, output_dir))
                except FileNotFoundError:
                    pass
            elif mode == '4':
                break
            else:
                print('Command not recognized. Exiting.')
                break
        except RecoverableError as e:
            print(e)

if __name__ == "__main__" :
    main_loop()