#general
import pandas as pd
import numpy as np
import os
import plotly.express as px
from datetime import datetime
import csv
import itertools

#ml
import sklearn
from sklearn.model_selection import TimeSeriesSplit as tsp
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV as gscv
from sklearn.svm import NuSVC as nusvc


class RFC():

    def __init__ (self, y_col : str, df : object, run_optim : bool, data_folder : str, n_jobs : int = 2):

        #set base infromation
        self.y_col : str            = y_col
        self.df : object            = df
        self.run_optim : bool       = run_optim
        self.n_jobs : int           = n_jobs

        #fixed params
        self.n_folds : int          = 4
        self.random_state : int     = 42

        #set saving infos
        self.log_file : str         = os.path.join(data_folder, "optim_log.txt")
        self.result_file : str      = os.path.join(data_folder, "nusvc_results.csv")

        #run optim if asked
        if run_optim:
            self.__run_optim()
        else:
            self.__df_split()

        #read results file
        self.__get_results()

        return

    def __run_optim(self):

        self.__generate_param_list()
        self.__log(message = f"NuSVC optim started")
        self.__df_split()
        self.__normal_valid()
        self.__cross_valid()
        self.__log(message = f"NuSVC optim started")

        return

    def __generate_param_list(self):
        """list of dicts with the needed params"""

        #set values to optimze for with the model
        kernels     = ["linear", "rbf", "sigmoid"]
        nus         = [i / 10 for i in range(1,10)]
        degrees     = list(range(1,6))

        #create kernel dicts
        combinations = list(itertools.product(kernels, nus, [0])) + list(itertools.product(["poly"], nus, degrees))

        # Convert the tuples to dictionaries with keys 'nu', 'kernel', and 'degree'
        self.param_list  = [dict(kernel=kernel, nu=nu, degree=int(degree)) for (kernel, nu, degree) in combinations]

        return

    def __df_split(self):

        #remove zero value columns
        zeor_cols = []

        for index, value in df.sum().items():
                if value == 0:
                    zeor_cols.append(index)

        self.df.drop(labels = zeor_cols, axis = 1, inplace = True)

        #create x and y
        self.X = self.df.drop(labels = self.y_col, axis = 1)
        self.y = self.df[self.y_col]

        #instanciate time splitter
        self.cv = tsp(n_splits=self.n_folds)

        return

    def __normal_valid(self):

        print("Optimizing with without cross validaiton")

        self.__single_model_split_v2(valid_frac = 0.15)

        for param in self.param_list:
            print(f"Progress: {round((self.param_list.index(param) +1)/ len(self.param_list) * 100)}% \t{param}", end = "\r")


            #creat the model
            model = nusvc(
                **param,
                random_state = self.random_state,
            )

            #fit the model
            model.fit(self.X_train, self.y_train)

            #get modle scores
            train_score : float = model.score(self.X_train, self.y_train)
            valid_score : float = model.score(self.X_valid, self.y_valid)

            self.__save_result(n_folds = 0, params = param, test_score = valid_score, train_score = train_score)

    def __cross_valid(self):

        print("Optimizing with with cross validaiton")

        for param in self.param_list:
            print(f"Progress: {round((self.param_list.index(param) +1)/ len(self.param_list) * 100)}%\t{param}", end = "\r")

            model = nusvc(
                **param,
                random_state = self.random_state
            )

            result = cross_validate(
                estimator = model,
                X = self.X,
                y = self.y,
                cv = self.cv,
                return_train_score = True
            )

            train_score = round(np.mean(result["train_score"]),4)
            test_score = round(np.mean(result["test_score"]),4)

            self.__save_result(n_folds = self.n_folds, params = param, test_score = test_score, train_score = train_score)

        return

    def __save_result(self, n_folds, params, test_score, train_score):

        if os.path.isfile(self.result_file) is False:

            file = open(self.result_file, "w", newline='')
            writer = csv.writer(file)
            writer.writerow(["n_folds", "kernel", "degree", "nu", "test_score", "train_score"])
            file.close()

        file = open(self.result_file, "a", newline='')
        writer = csv.writer(file)
        writer.writerow([n_folds, params["kernel"], params["degree"], params["nu"], test_score, train_score])
        file.close()

        return

    def __log(self, message):

        #create log entry
        log_time : str = datetime.now()
        message = f"source_rfc,{log_time},{message}\n"

        #write log entry
        file_object = open(self.log_file, 'a')
        file_object.write(message)
        file_object.close()

        return

    def __get_results(self):

        self.results = pd.read_csv(self.result_file)

    def __single_model_confusion_matrix(self, test_df):

        #set labels
        self.conf_mat_labels = [0, 1]

        #test conf mat
        if test_df is not None:

            X_test = test_df.drop(labels = self.y_col, axis = 1)
            y_test = test_df[self.y_col]

            self.y_hat_test = self.model.predict(X_test)
            self.confussion_mat_test = sklearn.metrics.multilabel_confusion_matrix(y_test, self.y_hat_test, labels = self.conf_mat_labels)

        #train conf mat
        self.y_hat_train = self.model.predict(self.X_train)
        self.confussion_mat_train = sklearn.metrics.multilabel_confusion_matrix(self.y_train, self.y_hat_train, labels = self.conf_mat_labels)

        #valid conf mat
        self.y_hat_valid = self.model.predict(self.X_valid)
        self.confussion_mat_valid = sklearn.metrics.multilabel_confusion_matrix(self.y_valid, self.y_hat_valid, labels = self.conf_mat_labels)

        return

    def __single_model_score(self, test_df):

        if test_df is not None:
            X_test = test_df.drop(labels = self.y_col, axis = 1)
            y_test = test_df[self.y_col]
            test_score = self.model.score(X_test, y_test)

        else:
            test_score = None

        train_score : float = self.model.score(self.X_train, self.y_train)
        valid_score : float = self.model.score(self.X_valid, self.y_valid)

        self.single_model_scores = {
            "train_score" : train_score,
            "valid_score" : valid_score,
            "test_score" : test_score,
        }

        return

    def __single_model_split_v1(self, valid_frac):
        """[deprecated] use v2 instead"""
        #change this to a random selection of years

        index = round(self.df.shape[0] * valid_frac)

        self.X_train = self.X.iloc[index:]
        self.y_train = self.y.iloc[index:]

        self.X_valid = self.X.iloc[:index]
        self.y_valid = self.y.iloc[:index]

        return

    def __single_model_split_v2(self, valid_frac):

        years = list(set(self.df["year"].to_list()))
        years.sort()

        n_years = int(len(years) * valid_frac)
        n_years_half = ((n_years % 2) + n_years) / 2 #round to even numbers and split in half

        #get target year list
        valid_years = years[round(((len(years) - 1) / 2) - n_years_half) : round((len(years) / 2 ) -1 )] + years[int(-n_years_half):]
        train_years = [year for year in years if year not in valid_years]

        #generate valid and train dfs
        df_valid = self.df[self.df["year"].isin(valid_years)]
        df_train =self.df[self.df["year"].isin(train_years)]

        #generate x and y
        self.X_train = df_train.drop(labels = self.y_col, axis = 1)
        self.y_train = df_train[self.y_col]

        self.X_valid = df_valid.drop(labels = self.y_col, axis = 1)
        self.y_valid = df_valid[self.y_col]

        del df_valid, df_train, valid_years, train_years #free up memory

        return

    def create_model(self, param : dict , valid_frac : float = 0.15, test_df : object = None, params : dict = None):

        #split data
        self.__single_model_split_v2(valid_frac = valid_frac)

        #create and fit model
        self.model = nusvc(
            random_state = self.random_state,
            **param,
        )

        self.model.fit(X = self.X_train, y = self.y_train)

        #generate results
        self.__single_model_score(test_df)
        self.__single_model_confusion_matrix(test_df)

        return

    def run_grid_search(self, fixed_param : dict):

        #get fixed params
        

        #create grid
        param_grid : dict = {
            #"param_name" : [list of values]
        }

        #create esimator
        model = nusvc(
            random_state = self.random_state,
            **fixed_param,
        )

        grid_search = gscv(estimator = model, param_grid = param_grid, cv = self.cv)
        grid_search.fit(self.X, self.y)

        # Print the best parameters and score
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best score: {grid_search.best_score_}")

        return grid_search.best_params_

    def clean_results (self):
        """Remove all same guess anwsers form the results tabel"""

        self.__single_model_split_v2(valid_frac = 0.15)
        self.results[["train_score", "test_score"]] = self.results[["train_score", "test_score"]].round(2)

        #same_guess_prop_train = [self.y_train.describe()["mean"].round(2), 1 - self.y_train.describe()["mean"].round(2)]
        same_guess_prop_valid = [self.y_valid.describe()["mean"].round(2), 1 - self.y_valid.describe()["mean"].round(2)]

        #clean up results df
        self.results["same_guess"] = 0
        self.results.loc[self.results["test_score"].isin(same_guess_prop_valid), "same_guess"] = 1

        self.results = self.results.loc[self.results["same_guess"] != 1].sort_values(by = "test_score", axis = 0, ascending = False)

        print(same_guess_prop_valid)

        return
