import os
import urllib
import filecmp
import datetime as dt
import pandas as pd

def get_files_from_dir(directory, sub_dir_start = len(os.path.dirname(os.getcwd()))):
    """ This function creates a list of file-paths to all files in a given directory.

    :param directory: (str) path to dictionary
    :param sub_dir_start: (int) the amount of letters at the beginning of path-string excluded from the print output. \
    (If the path is very long or for privacy issues if output is shared. Otherwise sub_dir_start = 0 might be set.)
    :return: a list of file-paths to all files in a given directory
    """
    if os.path.isdir(directory):
        (_, _, files) = next(os.walk(directory))
        file_paths = [os.path.join(directory, f) for f in files if f[0:7] != '.~lock.']
        file_paths.sort()
        return file_paths
    else:
        print(directory[sub_dir_start:], " is not a directory.")

def download_if_new(url,data_folder,n_th_last_file=0):
    """ Downloads a file from an url. If executed more often it compares the current file with the last local version, \
     and saves only new versions permanently. The path to the latest updated version is returned.

    :param url: (str) complete url of the file to be downloaded
    :param data_folder: (str) folder to save the file
    :return: (str)  path to the local version of the latest new version of the file
    """

    file_name = os.path.basename(url)
    file_path = os.path.join(data_folder,dt.datetime.now().strftime('%y%m%d %H%M%S')+'_'+file_name)
    file_paths = get_files_from_dir(data_folder)
    file_paths_relevant = [x for x in file_paths if x[-len(file_name):] == file_name]
    urllib.request.urlretrieve(url, file_path)
    if len(file_paths_relevant) > 0:
        identical = filecmp.cmp(file_paths_relevant[-1],file_path)
        if identical == True:
            os.remove(file_path)
            file_path = file_paths_relevant[-1]
            print(f'The-file {file_name} is not updated')
        else:
            print(f'The-file {file_name} is updated - the update file is added to the data-folder')
    else:
        print('The file is downloaded. No previous version existed in the data-folder.')
    if n_th_last_file > 0:
        file_path = file_paths_relevant[-n_th_last_file]
    return file_path

def pd_set_options():
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.float_format', '{:.4f}'.format)