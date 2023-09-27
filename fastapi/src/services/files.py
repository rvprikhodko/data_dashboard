import csv
from io import StringIO
from typing import BinaryIO
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from fastapi import HTTPException, status

from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor, GradientBoostingRegressor

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, classification_report

from sklearn.metrics import mean_absolute_error, mean_squared_error


fuel_consumption = []
not_classifiable = ['Unnamed: 0', 'YEAR', 'ENGINE SIZE', 'CYLINDERS',
                    'FUEL CONSUMPTION', 'HWY (L/100 km)', 'COMB (L/100 km)', 'COMB (mpg)', 'EMISSIONS']


class FilesService:

    @staticmethod
    def data_preprocessing(file: BinaryIO):
        df = pd.read_csv(file, encoding='utf-8')
        cat_features = ['MAKE', 'MODEL', 'VEHICLE CLASS', 'TRANSMISSION', 'FUEL']
        prefixes = ['ma', 'mo', 'vc', 'tr', 'fl']
        fuel_consumption.append(pd.get_dummies(columns=cat_features, data=df, prefix=prefixes))
        fuel_consumption.append(df)

    @staticmethod
    def preprocessed_download():
        output = StringIO()
        fuel_consumption[0].to_csv(output)
        output.seek(0)
        return output

    @staticmethod
    def return_df():
        return fuel_consumption[1].to_dict()

    @staticmethod
    def df_columns():
        fuel_consumption.append(list(fuel_consumption[0].columns))
        return fuel_consumption[2]

    @staticmethod
    def regression_ridge(column_name: str):
        if column_name not in list(fuel_consumption[0].columns):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Несуществующий столбец')
        y_fuel_regression = fuel_consumption[0][column_name]
        X_fuel_regression = fuel_consumption[0].drop(columns=[column_name])

        X_fuel_regression_train, X_fuel_regression_test, \
        y_fuel_regression_train, y_fuel_regression_test = train_test_split(
            X_fuel_regression,
            y_fuel_regression,
            test_size=0.2)

        ridge = Ridge().fit(X_fuel_regression_train, y_fuel_regression_train)

        # print(ridge.score(X_fuel_regression_test, y_fuel_regression_test))
        # print(mean_absolute_error(y_fuel_regression_test, ridge.predict(X_fuel_regression_test)))
        # print(mean_squared_error(y_fuel_regression_test, ridge.predict(X_fuel_regression_test)))

        to_return = {
            'score': ridge.score(X_fuel_regression_test, y_fuel_regression_test),
            'mean_absolute_error': mean_absolute_error(y_fuel_regression_test, ridge.predict(X_fuel_regression_test)),
            'mean_squared_error': mean_squared_error(y_fuel_regression_test, ridge.predict(X_fuel_regression_test))
        }

        return to_return

    @staticmethod
    def regression_decisiontree(column_name: str):
        if column_name not in list(fuel_consumption[0].columns):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Несуществующий столбец')
        y_fuel_regression = fuel_consumption[0][column_name]
        X_fuel_regression = fuel_consumption[0].drop(columns=[column_name])

        X_fuel_regression_train, X_fuel_regression_test, \
        y_fuel_regression_train, y_fuel_regression_test = train_test_split(
            X_fuel_regression,
            y_fuel_regression,
            test_size=0.2)

        dt = DecisionTreeRegressor().fit(X_fuel_regression_train, y_fuel_regression_train)
        to_return = {
            'score': dt.score(X_fuel_regression_test, y_fuel_regression_test),
            'mean_absolute_error': mean_absolute_error(y_fuel_regression_test, dt.predict(X_fuel_regression_test)),
            'mean_squared_error': mean_squared_error(y_fuel_regression_test, dt.predict(X_fuel_regression_test))
        }

        return to_return

    @staticmethod
    def regression_bag(column_name: str):
        if column_name not in list(fuel_consumption[0].columns):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Несуществующий столбец')
        y_fuel_regression = fuel_consumption[0][column_name]
        X_fuel_regression = fuel_consumption[0].drop(columns=[column_name])

        X_fuel_regression_train, X_fuel_regression_test, \
        y_fuel_regression_train, y_fuel_regression_test = train_test_split(
            X_fuel_regression,
            y_fuel_regression,
            test_size=0.2)

        bag = BaggingRegressor().fit(X_fuel_regression_train, y_fuel_regression_train)
        to_return = {
            'score': bag.score(X_fuel_regression_test, y_fuel_regression_test),
            'mean_absolute_error': mean_absolute_error(y_fuel_regression_test, bag.predict(X_fuel_regression_test)),
            'mean_squared_error': mean_squared_error(y_fuel_regression_test, bag.predict(X_fuel_regression_test))
        }

        return to_return

    @staticmethod
    def classification_knn(column_name: str):
        if column_name not in list(fuel_consumption[0].columns):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Несуществующий столбец')
        if column_name in not_classifiable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Столбец не пригоден к классификации')
        y_fuel_classification = fuel_consumption[0][column_name]
        X_fuel_classification = fuel_consumption[0].drop(columns=[column_name])

        X_fuel_classification_train, X_fuel_classification_test, \
        y_fuel_classification_train, y_fuel_classification_test = train_test_split(
            X_fuel_classification,
            y_fuel_classification,
            stratify=y_fuel_classification,
            test_size=0.2)

        knn = KNeighborsClassifier(n_neighbors=9).fit(X_fuel_classification_train, y_fuel_classification_train)

        return classification_report(y_fuel_classification_test, knn.predict(X_fuel_classification_test))

    @staticmethod
    def classification_log_reg(column_name: str):
        if column_name not in list(fuel_consumption[0].columns):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Несуществующий столбец')
        if column_name in not_classifiable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Столбец не пригоден к классификации')
        y_fuel_classification = fuel_consumption[0][column_name]
        X_fuel_classification = fuel_consumption[0].drop(columns=[column_name])

        X_fuel_classification_train, X_fuel_classification_test, \
        y_fuel_classification_train, y_fuel_classification_test = train_test_split(
            X_fuel_classification,
            y_fuel_classification,
            stratify=y_fuel_classification,
            test_size=0.2)

        lr = LogisticRegression().fit(X_fuel_classification_train, y_fuel_classification_train)

        return classification_report(y_fuel_classification_test, lr.predict(X_fuel_classification_test))

    @staticmethod
    def classification_dt(column_name: str):
        if column_name not in list(fuel_consumption[0].columns):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Несуществующий столбец')
        if column_name in not_classifiable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Столбец не пригоден к классификации')
        y_fuel_classification = fuel_consumption[0][column_name]
        X_fuel_classification = fuel_consumption[0].drop(columns=[column_name])

        X_fuel_classification_train, X_fuel_classification_test, \
        y_fuel_classification_train, y_fuel_classification_test = train_test_split(
            X_fuel_classification,
            y_fuel_classification,
            stratify=y_fuel_classification,
            test_size=0.2)

        dt = DecisionTreeClassifier().fit(X_fuel_classification_train, y_fuel_classification_test)

        return classification_report(y_fuel_classification_test, dt.predict(X_fuel_classification_test))

