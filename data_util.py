#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File reader/writer
@author: Akihiro Inui
ainui@jabra.com
"""

# Import libraries
import os
import requests
import datetime
import pandas as pd


class DataUtil:
    """
    # Functions for data manipulation
    """

    @staticmethod
    def excel2dataframe(input_file_path: str):
        """
        # Read excel file into pandas dataframe
        :param  input_file_path: input excel file
        :return pandas data frame
        """
        # Read excel and write out as csv file
        return pd.read_excel(input_file_path, index=False)

    @staticmethod
    def get_unique(input_dataframe, column_name: str):
        """
        # Get unique values in one column
        :param  input_dataframe: input pandas data frame
        :param  column_name: column name
        """
        unique_value = input_dataframe[column_name].unique()
        return unique_value

    @staticmethod
    def replace_comma(input_dataframe):
        """
        # Replace all commas in the data frame
        :param  input_dataframe: input pandas data frame
        :return input_dataframe: output pandas data frame without comma
        """

        # Replace comma for each column
        for column in input_dataframe.columns:
            input_dataframe[column] = input_dataframe[column].apply(
                lambda x: str(x.replace(",", " ")) if type(x) is str else x)
        return input_dataframe

    @staticmethod
    def replace_newline(input_dataframe):
        """
        # Replace all new lines in the data frame
        :param  input_dataframe: input pandas data frame
        :return input_dataframe: output pandas data frame without new line
        """
        # Replace comma for each column
        for column in input_dataframe.columns:
            input_dataframe[column] = input_dataframe[column].apply(
                lambda x: str(x.replace("\n", " ")) if type(x) is str else x)
            input_dataframe[column] = input_dataframe[column].apply(
                lambda x: str(x.replace("\r", " ")) if type(x) is str else x)
        return input_dataframe

    @staticmethod
    def dataframe2csv(input_dataframe, output_filename: str):
        """
        # Write data frame to csv file
        :param  input_dataframe: input pandas data frame
        :param  output_filename: output csv file name
        """
        input_dataframe.to_csv(output_filename, index=False)

    @staticmethod
    def get_time():
        """
        # Get current time and return as string
        :return : current time in string
        """
        time = str(datetime.datetime.now()).replace(":", "_")
        time = time.replace(".", "_")
        return time.replace(" ", "_")

    @staticmethod
    def is_downloadable(url):
        """
        Does the url contain a downloadable resource
        """
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True

    @staticmethod
    def download_data(url):
        """
        # Download file from the given url
        """
        # Check if the file is downloadable
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        file_name = os.path.basename(url)
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            with open(file_name, 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)

    @staticmethod
    def flatten_list(input_list: list) -> list:
        """
        # Flatten list elements in the input list
        :param  input_list: Input list to be flattened
        :return flat_list: Flattened list
        """
        # Prepare empty list to store elements
        flat_list = []

        # Add element one by one
        for feature in input_list:
            if type(feature) is list or tuple:
                for element in feature:
                    flat_list.append(element)
            else:
                flat_list.append(feature)
        return flat_list

    @staticmethod
    def factorize_label(input_dataframe, column_name: str, new_column_name: str):
        """
        # Factorize str label to num label
        :param  input_dataframe : input pandas data frame
        :param  column_name : column name to factorize
        :param  new_column_name: column to be created
        :return factorized_dataframe : data frame with factorized label
        :return label_list : list which stores label names
        """
        # Make a copy of the data frame
        factorized_dataframe = input_dataframe.copy()

        # Factorize string label
        factorized_column, unique_names = pd.factorize(factorized_dataframe[column_name])
        factorized_dataframe[new_column_name] = factorized_column

        return factorized_dataframe
