import pandas as pd
import numpy as np

def loadCSV(path):
    print("============ LOADING DF FROM CSV ======================================")
    df = pd.read_csv(path, index_col=0)
    print("DF loaded.")
    print()
    return df

def printDescribe(df):
    print("============ DESCRIBE DF ======================================")
    print(df.describe())
    print()
    return

def printInfo(df):
    print("============ INFO DF ========================================")
    print(df.info())
    print()
    return

def loadSets(set_gen, set_ciu, set_edu, set_hij):
    print("Loading sets...")
    set_gen = set(df["genero"].tolist())
    set_ciu = set(df["ciudad"].tolist())
    set_edu = set(df["niv_edu"].tolist())
    set_hij = set(df["hijos"].tolist())    
    return set_gen, set_ciu, set_edu, set_hij

def printSets(set_gen, set_ciu, set_edu, set_hij):
    print("============ SETS FROM DF ======================================")
    print("Set Genero: " + str(set_gen))
    print("Set Ciudad: " + str(set_ciu))
    print("Set Educación: " + str(set_edu))
    print("Set Hijos: " + str(set_hij))
    print()
    return

def remove_negative_values(df, column):
    df[column] = df[column].apply(lambda x: np.nan if x < 0 else x)    
    return df

def replace_negative_values_with_absolutes(df, column):
    df[column] = df[column].apply(lambda x: np.abs(x) if x < 0 else x)
    return df

def remove_outliers_using_zscore(df, column, treshold, use_rounded_mean=True):
    print("Removing outliers from column " + column + " -----------")
    
    column_mean = df[column].mean()
    column_rounded_mean = np.round(column_mean, 0)
    column_std = df[column].std()

    print("Mean: " + str(column_mean))
    print("Rounded Mean: " + str(column_rounded_mean))
    print("Use Rounded Mean: " + str(use_rounded_mean))
    print("Std: " + str(column_std))
    print("-------------------------------------------------")
    print()

    df[column] = df[column].mask(((df[column] - column_mean) / column_std).abs() > treshold, column_rounded_mean if use_rounded_mean else column_mean)

    return df

def map_column_values(df, column, dictionary):
    df[column] = df[column].replace(dictionary)
    return df

def fill_na_with_value(df, column, value):
    df[column] = df[column].fillna(value)
    return df

def saveDf(df, fileName):
    df.to_csv(fileName, sep=',')
    print("Guardando dataset resultante.")
    return df

def preprocess_data(df):
    educacion_mappings = {
        "Bachelors": "Bachelor",
        "mastre": "Master",
        "pHd": "PhD",
        "no education": "n/e",
        None: "n/e"
    }

    sex_mappings = {
        "m": "M",
        "f": "F",
        None: "n/e"
    }
    
    return (
        df
        .pipe(remove_negative_values, "edad")
        .pipe(remove_negative_values, "ingresos")
        .pipe(replace_negative_values_with_absolutes, "altura")
        .pipe(replace_negative_values_with_absolutes, "hijos")

        .pipe(remove_outliers_using_zscore, "edad", 2) 
        .pipe(remove_outliers_using_zscore, "ingresos", 2) 
        .pipe(remove_outliers_using_zscore, "altura", 2, False)        
        ##It's not necesary apply this method to hijos column
        #.pipe(remove_outliers_using_zscore, "hijos", 2) 

        #.pipe(fill_na_with_value, "hijos", df["hijos"].median())        
    )

set_gen = set()
set_ciu = set()
set_edu = set()
set_hij = set()
df = loadCSV("dataset_1b.csv")

set_gen, set_ciu, set_edu, set_hij = loadSets(set_gen, set_ciu, set_edu, set_hij)
printSets(set_gen, set_ciu, set_edu, set_hij)
printDescribe(df)
printInfo(df)

print("============ PREPROCESSING DF ======================================")
preprocess_data(df)
print("============ DF PREPROCESSED =======================================")

set_gen, set_ciu, set_edu, set_hij = loadSets(set_gen, set_ciu, set_edu, set_hij)
printSets(set_gen, set_ciu, set_edu, set_hij)
printDescribe(df)
printInfo(df)

saveDf(df, 'dataset_1b_result.csv')

exit(0)

remove_outliers_using_zscore(df, "edad", 3)
remove_outliers_using_zscore(df, "ingresos", 3)
remove_outliers_using_zscore(df, "hijos", 3)

printDescribe(df)
printInfo(df)   