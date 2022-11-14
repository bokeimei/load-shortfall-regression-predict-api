"""

    Helper functions for the pretrained model to be used within our API.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.

    Importantly, you will need to modify this file by adding
    your own data preprocessing steps within the `_preprocess_data()`
    function.
    ----------------------------------------------------------------------

    Description: This file contains several functions used to abstract aspects
    of model interaction within the API. This includes loading a model from
    file, data preprocessing, and model prediction.  

"""

# Helper Dependencies
import numpy as np
import pandas as pd
import pickle
import json
from sklearn.preprocessing import StandardScaler

def _preprocess_data(data):
# create a function to use in cleaning the test data

#def engineer_data(filepath):
    # Read csv file into dataframe 
    df = pd.read_csv(data)
    
     # create new features
    df['Year']  = df['time'].astype('datetime64').dt.year
    df['Month_of_year']  = df['time'].astype('datetime64').dt.month
    df['Week_of_year'] = df['time'].astype('datetime64').dt.weekofyear
    df['Day_of_year']  = df['time'].astype('datetime64').dt.dayofyear
    df['Day_of_month']  = df['time'].astype('datetime64').dt.day
    df['Day_of_week'] = df['time'].astype('datetime64').dt.dayofweek
    df['Hour_of_week'] = ((df['time'].astype('datetime64').dt.dayofweek) * 24 + 24) - (24 - df['time'].astype('datetime64').dt.hour)
    df['Hour_of_day']  = df['time'].astype('datetime64').dt.hour
    
    #Filling missing values
    df['Valencia_pressure'].fillna(df['Valencia_pressure'].mean(), inplace = True)
    
    #converting Valencia_wind_deg and Seville_pressure from object to numeric
    df['Valencia_wind_deg'] = df['Valencia_wind_deg'].str.extract('(\d+)').astype('float')
    df['Seville_pressure'] = df['Seville_pressure'].str.extract('(\d+)').astype('float')
    
    df.drop(columns=['Week_of_year', 'Valencia_temp_max', 'Bilbao_temp_min', 'Barcelona_temp_max', 
                 'Madrid_temp_min', 'Bilbao_temp_max', 'Day_of_year', 'Hour_of_week', 
                 'Unnamed: 0','time', 'Seville_temp_min', 'Madrid_temp_max', 'Valencia_temp', 
                 'Barcelona_temp', 'Seville_temp', 'Madrid_temp'], inplace=True)
    
    # Initialize StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    X_scaled = pd.DataFrame(X_scaled,columns=df.columns)
    
    return X_scaled
    """Private helper function to preprocess data for model prediction.

    NB: If you have utilised feature engineering/selection in order to create
    your final model you will need to define the code here.


    Parameters
    ----------
    data : str
        The data payload received within POST requests sent to our API.

    Returns
    -------
    Pandas DataFrame : <class 'pandas.core.frame.DataFrame'>
        The preprocessed data, ready to be used our model for prediction.
    """
    # Convert the json string to a python dictionary object
    feature_vector_dict = json.loads(data)
    # Load the dictionary as a Pandas DataFrame.
    feature_vector_df = pd.DataFrame.from_dict([feature_vector_dict])
    
    # ---------------------------------------------------------------
    # NOTE: You will need to swap the lines below for your own data
    # preprocessing methods.
    #
    # The code below is for demonstration purposes only. You will not
    # receive marks for submitting this code in an unchanged state.
    # ---------------------------------------------------------------

    # ----------- Replace this code with your own preprocessing steps --------
    
     # create new features
    feature_vector_df['Year']  = feature_vector_df['time'].astype('datetime64').dt.year
    feature_vector_df['Month_of_year']  = feature_vector_df['time'].astype('datetime64').dt.month
    feature_vector_df['Week_of_year'] = feature_vector_df['time'].astype('datetime64').dt.weekofyear
    feature_vector_df['Day_of_year']  = feature_vector_df['time'].astype('datetime64').dt.dayofyear
    feature_vector_df['Day_of_month']  = feature_vector_df['time'].astype('datetime64').dt.day
    feature_vector_df['Day_of_week'] = feature_vector_df['time'].astype('datetime64').dt.dayofweek
    feature_vector_df['Hour_of_week'] = ((feature_vector_df['time'].astype('datetime64').dt.dayofweek) * 24 + 24) - (24 - feature_vector_df['time'].astype('datetime64').dt.hour)
    feature_vector_df['Hour_of_day']  = feature_vector_df['time'].astype('datetime64').dt.hour
    
    #Filling missing values
    feature_vector_df['Valencia_pressure'].fillna(feature_vector_df['Valencia_pressure'].mean(), inplace = True)
    
    #converting Valencia_wind_deg and Seville_pressure from object to numeric
    feature_vector_df['Valencia_wind_deg'] = feature_vector_df['Valencia_wind_deg'].str.extract('(\d+)').astype('float')
    feature_vector_df['Seville_pressure'] = feature_vector_df['Seville_pressure'].str.extract('(\d+)').astype('float')
    
    feature_vector_df.drop(columns=['Week_of_year', 'Valencia_temp_max', 'Bilbao_temp_min', 'Barcelona_temp_max', 
                 'Madrid_temp_min', 'Bilbao_temp_max', 'Day_of_year', 'Hour_of_week', 
                 'Unnamed: 0','time', 'Seville_temp_min', 'Madrid_temp_max', 'Valencia_temp', 
                 'Barcelona_temp', 'Seville_temp', 'Madrid_temp'], inplace=True)
    feature_vector_df.fillna(0, inplace=True)             
    
    # Initialize StandardScaler
    scaler = StandardScaler()
    predict_vector = scaler.fit_transform(feature_vector_df)
    predict_vector = pd.DataFrame(predict_vector,columns=feature_vector_df.columns)

    # ---------------------------------------------------------------
    
    return predict_vector

def load_model(path_to_model:str):
    """Adapter function to load our pretrained model into memory.

    Parameters
    ----------
    path_to_model : str
        The relative path to the model weights/schema to load.
        Note that unless another file format is used, this needs to be a
        .pkl file.

    Returns
    -------
    <class: sklearn.estimator>
        The pretrained model loaded into memory.

    """
    return pickle.load(open(path_to_model, 'rb'))


""" You may use this section (above the make_prediction function) of the python script to implement 
    any auxiliary functions required to process your model's artifacts.
"""

def make_prediction(data, model):
    """Prepare request data for model prediction.

    Parameters
    ----------
    data : str
        The data payload received within POST requests sent to our API.
    model : <class: sklearn.estimator>
        An sklearn model object.

    Returns
    -------
    list
        A 1-D python list containing the model prediction.

    """
    # Data preprocessing.
    prep_data = _preprocess_data(data)
    # Perform prediction with model and preprocessed data.
    prediction = model.predict(prep_data)
    # Format as list for output standardisation.
    return prediction[0].tolist()
