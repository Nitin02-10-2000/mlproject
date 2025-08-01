import os
import sys
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object,evaluate_model
from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
    )
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from dataclasses import dataclass
@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("spilt training and test input data") 
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models={
                "Random Forest":RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "XGBRegressor":XGBRegressor(),
                "CatBoosting Regressor":CatBoostRegressor(verbose=False),
                "AdaBoost Regressor":AdaBoostRegressor()
            }
            param={
                "Decision Tree":{
                    "ccp_alpha":[0.1,0.2,0.3],
                    "max_depth":[2,3,5,10,None]
                },
                "Random Forest":{
                    "criterion":["squared_error","absolute_error","poisson"],
                    "max_depth":[2,3,5,10,None],
                    "min_samples_leaf":[1,2,4],
                    "n_estimators":[100,200,500]
                },
                "Gradient Boosting":{
                    "learning_rate":[0.1,0.01,0.05,0.001],
                    "n_estimators":[100,200,500],
                    "subsample":[0.6,0.8,1.0]
                },
                "Linear Regression":{
                    "fit_intercept":[True,False]
                },
                "XGBRegressor":{
                    "learning_rate":[0.1,0.01,0.05,0.001],
                },
                "CatBoosting Regressor":{
                    "depth":[6,8,10],
                    "learning_rate":[0.01,0.05,0.1],
                    "iterations":[100,200,500]
                },
                "AdaBoost Regressor":{
                    "n_estimators":[100,200],
                    "learning_rate":[0.1,0.01,0.05,0.001]
                }
            }
            model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,param=param)
            best_model_score=max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted=best_model.predict(x_test)
            r2_square=r2_score(y_test,predicted)
            return r2_square
        except Exception as e:
            raise CustomException(e,sys)