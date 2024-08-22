import pandas as pd
import numpy as np

set_gen = set()
set_edu = set()
set_ciu = set()

def printDescribe():
    print("============ DESCRIBE DF ======================================")
    print(df.describe())
    print()
    return

def printInfo():
    print("============ INFO DF ========================================")
    print(df.info())
    print()
    return

def loadSets():
    set_gen = set(df["genero"].tolist())
    set_edu = set(df["niv_edu"].tolist())
    set_ciu = set(df["ciudad"].tolist())
    return set_gen, set_edu, set_ciu

def printSets():
    print("============ SETS FROM DF ======================================")
    print("Set Genero: " + str(set_gen))
    print("Set Educación: " + str(set_edu))
    print("Set Ciudad: " + str(set_ciu))
    print()
    return

def saveDf():
    df.to_csv('dataset_2.csv', sep=',')
    print("Guardando dataset en dataset_2.csv")
    return 

df = pd.read_csv('dataset_1.csv', index_col=0)

printDescribe()
printInfo()
set_gen, set_edu, set_ciu = loadSets()
printSets()

#1. Tratamiento de valores negativos
df["edad"] = df["edad"].apply(lambda x: np.nan if x < 0 else x)
df["ingresos"] = df["ingresos"].apply(lambda x: np.nan if x < 0 else x)
df["hijos"] = df["hijos"].apply(lambda x: np.nan if x < 0 else x)

printDescribe()
printInfo()

#2. Imputar valores faltantes
#df["edad"] = df["edad"].fillna(df["edad"].median())
#df["ingresos"] = df["ingresos"].fillna(df["ingresos"].median())
#df["hijos"] = df["hijos"].fillna(df["hijos"].median())
for column in ["edad","ingresos","hijos"]:
    print("Inputando valores faltantes en la columna " + column)
    median_value = df[column].median()
    print("Inputando Mediana: " + str(median_value) + " a columna " + column)
    #df[column] = df[column].fillna(median_value)
    df.fillna({column: median_value}, inplace=True)
    print("")

for column in ["genero", "ciudad"]:
    print("Inputando valores faltantes en la columna " + column)
    mode_value = df[column].mode()[0]
    print("Inputando Moda: " + str(mode_value) + " a columna " + column)
    df.fillna({column: mode_value}, inplace=True)
    print("")

printDescribe()
printInfo()

#3. Mapeo de valores
educacion_mappings = {
    "Bachelors": "Bachelor",
    "mastre": "Master",
    "pHd": "PhD",
    "no education": "n/e",
    None: "n/e"
}

print("Aplicando mapeo de valores a la columna 'niv_edu'")
#df["niv_edu"] = df["niv_edu"].map(educacion_mappings)
df["niv_edu"] = df["niv_edu"].replace(educacion_mappings)
#df["niv_edu"] = df["niv_edu"].fillna("none")
print("")

printDescribe()
printInfo()
set_gen, set_edu, set_ciu = loadSets()
printSets()

#4. Casteo de valores
print("Casteando 'edad' a tipo entero")
df["edad"] = df["edad"].astype(int)
print("Casteando 'hijos' a tipo entero")
df["hijos"] = df["hijos"].astype(int)
print("Casteando 'ingresos' a tipo float")
df["ingresos"] = df["ingresos"].astype(float)
print("Casteando 'altura' a tipo float")
df["altura"] = df["altura"].astype(float)
print("")

printDescribe()
printInfo()

saveDf()