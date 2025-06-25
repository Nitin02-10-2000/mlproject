import sys
import os
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.utils import save_object
@dataclass
class DataTransformerConfig:
    preprocessr_obj_file=os.path.join('artifect',"processor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformerConfig()
    def get_data_transformer_object(self): 
        try:
            numerical_columns=["writing_score","reading_score"]
            categorical_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
                "race_ethnicity" ]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                    ] 
                )
            logging.info("numerical columns standard scaling completed")
            logging.info("categorical columns encoding completed")
            processor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )
            return processor
    
        except Exception as e:
            raise CustomException(e,sys) 
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("read train and test data completed")
            logging.info("obtaining preprocessing object")
            preprocessing_obj=self.get_data_transformer_object()
            target_column_name="math_score"
            numerical_columns=["writing_score","reading_score"]
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            logging.info("applying preprocessing object on training and testing dataframe")
            input_feature_train_df_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_df_arr=preprocessing_obj.transform(input_feature_test_df)
            train_arr=np.c_[
                input_feature_train_df_arr,np.array(target_feature_train_df) 
            ]
            test_arr=np.c_[
                input_feature_test_df_arr,np.array(target_feature_test_df)
            ]
            logging.info( "saved preprocessing obj")
            save_object(
                file_path=self.data_transformation_config.preprocessr_obj_file,
                obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessr_obj_file,
            )
        except Exception as e:
            raise CustomException(e,sys) 