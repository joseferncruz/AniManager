"""
################################################################################
Ani Manager - quickfix to manage animals in the lab
################################################################################
"""
__author__ = 'Jose Oliveira da Cruz'
__email__ = 'jose.cruz@nyu.edu'
__version__ = '0.3.0'
################################################################################

# Import modules
import pandas as pd
import numpy as np
import os
import time
import sys


##############################################################################
def create_new_animal_record(
    animal_list=[],
    project=None,
    principal_investigator=None,
    user=None,
    species=None,
    strain=None,
    age_at_arrival_weeks=None,
    sex=None,
    date_of_birth=None,
    date_of_arrival=None,
    location_id=None,
):
    """Create a new animal record as a DataFrame.

    Description

    Args:
        arg_1: description
        arg_2: description

    Returns:
        A pandas DataFrame with the information provided as arguments. If no
        information is provided, it it returns an empty DataFrame with the
        column names.

    """
    column_labels = ["project", "pi", "user", "species", "strain", "animal_id",
                     "sex", "date_of_birth", "date_of_arrival",
                     "age_at_arrival_weeks", "location_id",
                     "date_of_sacrifice",
                     ]
    # Create the shape of the dataframe.
    animal_record = pd.DataFrame(index=np.arange(len(animal_list)),
                                 columns=column_labels,
                                 )
    animal_list_sorted = sorted(animal_list)

    # Loop through every animal in the list and add it to the dataframe.
    for animal in range(len(animal_list_sorted)):
        animal_record.iloc[animal, 5] = animal_list_sorted[animal]
        animal_record["project"] = project
        animal_record["pi"] = principal_investigator
        animal_record["user"] = user
        animal_record["species"] = species
        animal_record["strain"] = strain
        animal_record["age_at_arrival_weeks"] = age_at_arrival_weeks
        animal_record["sex"] = sex
        animal_record["date_of_birth"] = date_of_birth
        animal_record["date_of_arrival"] = date_of_arrival
        animal_record["location_id"] = location_id
        animal_record["date_of_sacrifice"] = np.nan

    return animal_record

##############################################################################


def merge_main_record(
    new_animal_record,
    animal_record_to_update,
    output_dir,
    save_output=False,
):
    """Update an existing animal record.

    Parameters
    ----------
    new_animal_record : dataframe
        <description>

    animal_record_to_update : dataframe
        <description>

    save_path : str, optional

    Returns
    -------
    dataframe
        dataframe with all animals and respective information in a panel
    """
    # Merge records.
    merged_records = pd.concat([animal_record_to_update,
                                new_animal_record])
    # Save file.
    if save_output:
        file_name = 'main_record_{}.csv'.format(time.strftime('%Y%m%d_%H%M%S'))
        saving_path = os.path.join(output_dir, file_name)
        merged_records.to_csv(saving_path)
        print(f'File saved at: \n{saving_path}')

    return merged_records

##############################################################################


def save_new_animal_record(
    animal_record,
    save_dir,
    is_new_main_record=False,
    save_csv=False,
    save_excel=False,
):
    """Save animal record.

    Parameters
    ----------
    animal_record : dataframe
        DataFrame with the record to be saved.

    save_dir : str
        Filepath where the file is intended to be stored.

    save_csv: bool, optional
        Save file as .csv

    save_excel: bool, optional
        Save file as .xls




    """
    if is_new_main_record:
        print('This is a new main record.')
        main_record_dir = os.path.join(save_dir, 'main_record')
        if not os.path.isdir(main_record_dir):
            print(f'Main record directory not found. \
                  Creating directory main_record at \n {main_record_dir}')
            os.mkdir(main_record_dir)
        save_csv_path = os.path.join(main_record_dir,
                                     'main_record_{}.csv'.format(
                                             time.strftime("%Y%m%d_%H%M%S")
                                             )
                                     )
        animal_record.to_csv(save_csv_path)
        print(f'main record stored at \n{save_csv_path}')

    save_dir = os.path.join(save_dir, 'individual_updates')
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
        print(f'Directory not found. Creating directory individual_updates at \
               \n {save_dir}')

    if save_csv:
        save_csv_path = os.path.join(save_dir,
                                     'new_import_{}.csv'.format(
                                         time.strftime("%Y%m%d_%H%M%S")
                                         )
                                     )

        animal_record.to_csv(save_csv_path)
        print(f'File saved at: \n{save_csv_path}.')

    if save_excel:
        save_excel_path = os.path.join(save_dir,
                                       'new_import_{}.xls'.format(
                                           time.strftime("%Y%m%d_%H%M%S")
                                           )
                                       )
        animal_record.to_excel(save_excel_path)
        print(f'File saved at: \n{save_excel_path}.')

##############################################################################


def get_main_record(
    main_record_dir,
):
    """Get the latest main record from folder.

    Parameters
    ----------
    arg : dataframe
        <description>


    save_path : str, optional

    Returns
    -------


    """
    # Check directory
    latest_main_record = os.listdir(main_record_dir)[-1]

    # Verify if there are main_record_files
    if latest_main_record.startswith('main_record'):
        # Get the file path.
        main_record_filepath = os.path.join(main_record_dir,
                                            latest_main_record,
                                            )
        # Get the dataframe.
        main_record = pd.read_csv(main_record_filepath,
                                  index_col=0,
                                  parse_dates=['date_of_birth',
                                               'date_of_arrival',
                                               'date_of_sacrifice',
                                               ]
                                  )

        return (main_record_filepath, main_record)
    else:
        print('There is no main_record in this folder.')

##############################################################################


def fetch_from_main_record(
    animal_id_list,
    main_record,
    user='',
    experiment_number='',
    output_path=None,
):
    """DOC String."""
    # Get the dataframe
    record_to_return = main_record[main_record['animal_id'].isin(animal_id_list
                                                                 )
                                   ]

    # Specify the file name
    file_name = f'{user.upper()}_EXP{experiment_number}_animal_record.xls'

    if output_path is not None:
        # Save the file in the specific working directory
        record_to_return.to_excel(os.path.join(output_path, file_name))
        # Print success message
        message = f'Dataframe saved at: {os.path.join(output_path, file_name)}'
        print(message)

    return record_to_return

##############################################################################


def update_main_record(
    animal_record,
    animal_id_list,
    column_to_update,
    value_to_add,
):
    """Update an animal record."""
    assert isinstance(animal_id_list, list), \
        'animal_id_list must be a list of integers'
    assert isinstance(value_to_add, (str, int, float)), \
        'value_to_add must be a single string, integer or float'

    # Create a copy of the dataframe
    animal_record = animal_record.copy()

    # extract row indexer used to subset the data
    row_indexer = animal_record['animal_id'].isin(animal_id_list)

    # Replace the value at the column of interest
    animal_record.loc[row_indexer, column_to_update] = value_to_add

    return animal_record

###############################################################################


# Find the previous version of the record
def save_main_record(
    main_record,
    main_record_dir,
    base_name=None,
):
    """To be completed."""
    assert isinstance(base_name, (str, object)), \
        'base_name must finish with .csv extension'

    if base_name is None:
        file_name = 'main_record_{}.csv'.format(time.strftime('%Y%m%d_%H%M%S'))
        saving_path = os.path.join(main_record_dir, file_name)
        main_record.to_csv(saving_path)
        print(f'File saved at {saving_path}')
    else:
        file_name = '{}_{}.csv'.format(base_name,
                                       time.strftime('%Y%m%d_%H%M%S'))
        saving_path = os.path.join(main_record_dir, file_name)
        main_record.to_csv(saving_path)
        print(f'File saved at {saving_path}')

# LEGACY CODE # IGNORE
##############################################################################


def load_source_code_library(src_directory_path):
    """Load source code library."""
    if src_directory_path.endswith('src'):
        if True in [element.endswith('src') for element in sys.path]:
            print('Source code library is already loaded.')
        else:
            print('Source code library not found.\
                  \nAppending src_directory_path...')
            try:
                sys.path.append(src_directory_path)
                print('Source code library is loaded.')
            except 'LibraryNotFound':
                print('Error with given source code library pathway')
                src_directory_path = input('Insert a valid path \
                                           for the source code library: ')
    else:
        print('Error with pathway provided. Source folder not found.\
              Verify the folder and try again.')
