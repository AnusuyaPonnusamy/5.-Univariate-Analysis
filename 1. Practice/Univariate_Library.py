class Univariate():
    def QuanQual(dataset):
        f_Quan=[]
        f_Qual=[]
        for columnName in dataset.columns:
            if(dataset[columnName].dtype=='O'):
                f_Qual.append(columnName)
            else:
                f_Quan.append(columnName)
        return f_Quan,f_Qual

def MCT_MLT(dataset,quan):
    df_MCT=pd.DataFrame(index=["Mean", "Median", "Mode","Q1:25%", "Q2:50%", "Q3:75%", "99%", "Q4:100%", "IQR","1.5_Rule", "Lesser", "Greater", "Min", "Max", "kurtosis", "skew","Var","Std"], columns=quan)
    for columnName in quan:
        df_MCT[columnName]["Mean"]=dataset[columnName].mean()
        df_MCT[columnName]["Median"]=dataset[columnName].median()
        df_MCT[columnName]["Mode"]=dataset[columnName].mode()[0] 
        df_MCT[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
        df_MCT[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
        df_MCT[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
        df_MCT[columnName]["99%"]=np.percentile(dataset[columnName],99)
        df_MCT[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
        df_MCT[columnName]["IQR"]=df_MCT[columnName]["Q3:75%"]-df_MCT[columnName]["Q1:25%"]
        df_MCT[columnName]["1.5_Rule"]=1.5*df_MCT[columnName]["IQR"]
        df_MCT[columnName]["Lesser"]=df_MCT[columnName]["Q1:25%"] - df_MCT[columnName]["1.5_Rule"]
        df_MCT[columnName]["Greater"]=df_MCT[columnName]["Q3:75%"] + df_MCT[columnName]["1.5_Rule"]
        df_MCT[columnName]["Min"]=dataset[columnName].min()
        df_MCT[columnName]["Max"]=dataset[columnName].max()
        df_MCT[columnName]["kurtosis"]=dataset[columnName].kurtosis()
        df_MCT[columnName]["skew"]=dataset[columnName].skew()
        df_MCT[columnName]["Std"]=dataset[columnName].std()
        df_MCT[columnName]["Var"]=dataset[columnName].var()
    return df_MCT

    def frequency_table(columnName,dataset):
        df_frequency=pd.DataFrame(columns=["Unique_Values","Frequency", "Relative_Frequency","Cumulative_Frequency"])
        df_frequency["Unique_Values"]=dataset[columnName].value_counts().index
        df_frequency["Frequency"]=dataset[columnName].value_counts().values
        df_frequency["Relative_Frequency"]=(df_frequency["Frequency"] / 103)
        df_frequency["Cumulative_Frequency"]=df_frequency["Relative_Frequency"].cumsum()
        return df_frequency

    def outlier_identifier(columnName, quan):
        lesser=[]
        greater=[]
        for columnName in quan:
            if(df_MCT[columnName]["Min"]<df_MCT[columnName]["Lesser"]):
                lesser.append(columnName)
            if(df_MCT[columnName]["Max"]>df_MCT[columnName]["Greater"]):
                greater.append(columnName)
        return lesser, greater

    def outlier_replacer(columnName, dataset):
        for columnName in lesser:
            dataset[columnName][dataset[columnName]<df_MCT[columnName]["Lesser"]]=df_MCT[columnName]["Lesser"]
        for columnName in greater:
            dataset[columnName][dataset[columnName]>df_MCT[columnName]["Greater"]]=df_MCT[columnName]["Greater"]
        return df_MCT