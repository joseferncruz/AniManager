
"""
###############################################################################
Ani Manager - quickfix for managing animals in the lab
###############################################################################
"""

__author__ = 'Jose Oliveira da Cruz'
__email__ = 'jose.cruz@nyu.edu'
__version__ = '0.1.0'
###############################################################################

# Import modules
import pandas as pd
import numpy as np
import os
import time


##############################################################################
def create_new_animal_record(
    import_info
):
    """Create a new animal record as a DataFrame.

    Parameters
    ----------
    import_info : dict
        Information used to generate a DataFrame.

    Returns
    -------
    DataFrame.
        If the animal_list is empty, it it returns
        an empty DataFrame with the column names.

    """
    column_labels = [

        'project', 'pi', 'user', 'species', 'strain', 'animal_id',
        'sex', 'date_of_birth', 'date_of_arrival',
        'age_at_arrival_weeks', 'location_id', 'date_of_sacrifice',
    ]
    # Create the shape of the dataframe.
    animal_record = pd.DataFrame(index=np.arange(len(import_info.get('animal_list'))),
                                 columns=column_labels,
                                 )
    # Sort the animal_id_list
    animal_list_sorted = sorted(import_info.get('animal_list'))

    # Loop through every animal in the list and add it to the dataframe.
    for animal in range(len(animal_list_sorted)):
        animal_record.iloc[animal, 5] = animal_list_sorted[animal]
        animal_record['project'] = import_info.get('project')
        animal_record['pi'] = import_info.get('principal_investigator')
        animal_record['user'] = import_info.get('user')
        animal_record['species'] = import_info.get('species')
        animal_record['strain'] = import_info.get('strain')
        animal_record['age_at_arrival_weeks'] = import_info.get('age_at_arrival_weeks')
        animal_record['sex'] = import_info.get('sex')
        animal_record['date_of_birth'] = import_info.get('date_of_birth')
        animal_record['date_of_arrival'] = import_info.get('date_of_arrival')
        animal_record['location_id'] = import_info.get('location_id')
        animal_record['date_of_sacrifice'] = np.nan

    return animal_record

##############################################################################


def merge_with_main_record(
    new_animal_record,
    animal_record_to_update,
    output_dir,
    save_output=False,
):
    """Merge a new import with the main record.

    Parameters
    ----------
    new_animal_record : DataFrame
        Dataframe to merge with the main record.

    animal_record_to_update : dataframe
        Main record Dataframe to be updated.

    output_dir : str
        Absolute path to the main_record directory.

    save_output : bool, optional
        Saves the DataFrame at the output_dir.

    Returns
    -------
    merged_records : dataframe
        Dataframe with all animals and respective information in a panel
    """
    # Merge records.
    merged_records = pd.concat([animal_record_to_update,
                                new_animal_record])
    # Save file.
    if save_output:
        # Attribute a specific timestamp.
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
    """Save a .csv or .xls file with the a new record at a specific location.

    Parameters
    ----------
    animal_record : dataframe
        DataFrame with the record to be saved.

    save_dir : str
        Filepath where the file is intended to be stored.

    is_new_main_record : bool, optional
        If True it creates a new directory main_record and stores a copy
        of the new import at that location.

    save_csv: bool, optional
        Save file as .csv at the save_dir directory.

    save_excel: bool, optional
        Save file as .xls at the save_dir directory.

    """
    # If this is the first import, create the main_import dir and save a copy
    # of the import at that location.
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

    # Create a new individual_updates directory if there is none.
    save_dir = os.path.join(save_dir, 'individual_updates')
    if not os.path.isdir(save_dir):  # If directory is not found, create it.
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
    """Get the latest main record from the main_record directory.

    Parameters
    ----------
    main_record_dir : str
        Absolute path to the main_record directory.

    Returns
    -------
    main_record_filepath : str
        Absolute path to the latest main_record file found at the directory.
    main_record : DataFrame
        DataFrame with the latest main_record file content.
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
    """Fetch information from the main_record.

    Parameters
    ----------
    animal_id_list : list of int
        List with the specific animal identifiers as integers.

    main_record : DataFrame
        Dataframe with the main record to fetch information.

    user : str, optional
        Used to label the output file.

    experiment_number : str, optional
        Used to label the output file.

    output_path : str, optional
        The Absolute path to the directory where the file is to be stored.

    Returns
    -------
    record_to_return : DataFrame
        Dataframe with the fetched information.
    """
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
    """Update an animal record.

    Parameters
    ----------
    animal_record : DataFrame
        DataFrame with the latest animal record.

    animal_id_list : list
        List with the specific animal_id numbers to modify.

    column_to_update : str
        Name of the column to update.

    value_to_add : str
        Value to be added to the DataFrame.

    Returns
    -------
    animal_record : DataFrame
        Updated animal record.
    """
    assert isinstance(animal_id_list, list), \
        'animal_id_list must be a list of integers'
    assert isinstance(value_to_add, (str, int, float)), \
        'value_to_add must be a single string, integer or float'

    # Create a copy of the dataframe
    animal_record = animal_record.copy()

    # Extract row indexer used to subset the data
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
    """Save main record at a specific location.

    Parameters
    ----------
    main_record : DataFrame
        DataFrame to be saved at the main_record_dir directory.

    main_record_dir : str
        Absolute path to the directory containing the main_record.

    base_name : str, optional
        Saves the main_record with a new basename. This file won't be used as
        a main record because it has a new base name.'

    """
    assert isinstance(base_name, (str, object)), \
        'base_name must be a string finishing with .csv extension'

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

###############################################################################
