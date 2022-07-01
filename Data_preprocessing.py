#Version beta 1.0

#Author: Jiajun Pang


#Note: in current version, the data downloaded from the SurveyMonkey need to be preprocessed in advance.
#Questions with multiple choices need to be integrated before using this code. Moreover, it is better to
#make the data with the first row as the variable name and the responses right under the variable names.

#For instance: the struture below is required:

#     column1 column2  column3
#Row1    x1      x2      x3
#Row2    1       3       Vehicle
#Row3    2       4       Walk
#Row4    3       5       Bicycle




import pandas as pd


class data_conversion:

    def __init__(self, file):
        self.path = file                                 #return the path of the dataset
        self.len = 0                                     #return the number of observation
        self.col = []                                    #return the columns that need conversion
        self.special_dict_category = {}                  #return the columns that have special request
        self.df = pd.DataFrame()                         #return the dataset
        self.dict = {}
        self.dictionary = pd.DataFrame()
        self.df_converted = pd.DataFrame()

        

    def read_data(self, file_type, sheet_name = "Sheet1"):
        if file_type == "csv":
            path = self.path
            self.df = pd.read_csv(path)

        
        if file_type == "Excel" or file_type == "excel":
            self.df = pd.read_excel(self.path, sheet_name= sheet_name)
        
        column_name = list(self.df.keys())
        self.col = column_name
        self.len = len(self.df)
    
    def special_categoryies_pair(self, categorical_colum_name, dict_category):
        self.special_dict_category.update({categorical_colum_name: dict_category})
        self.dict.update({categorical_colum_name: dict_category})
        
    def remove_special_column(self, column_name):
        del self.special_dict_category[column_name]

    def skip_column(self, column_name):
        for col in column_name:
            col = self.col.remove(col)

    def pair(self, values):
        convert_dict = {}
        i = 0
        for j in values:
            i += 1
            convert_dict[j] = i

        return convert_dict
    def integrate(self, data_convert):
        keys = data_convert.keys()
        for key in keys:
            self.df[key] = data_convert[key]
        
        return self.df

    def data_conversion(self):
        data_convert = {}
        special_col = self.special_dict_category.keys()
        
        for key in self.col:
            
            data_convert.update({key:[]})
            if key in special_col:
                for value in self.df[key]:
                    if value in self.special_dict_category[key].keys():
                        data_convert[key].append(self.special_dict_category[key][value])
                        self.dict.update({key:self.special_dict_category[key]})
                    else:
                        data_convert[key].append(value)

            if key not in special_col:
                
                values = self.df[key].unique()
                convert_dict = self.pair(values)
                self.dict.update({key:convert_dict})

                for value in self.df[key]:
                    data_convert[key].append(convert_dict[value])


        
        data_convert = pd.DataFrame(data_convert)
        dictionary = self.edit_dict()
        data_convert2 = self.integrate(data_convert)
        # sort the dictionary

        sequence = {"Seq": []}
        for value in dictionary["variable"]:
            number = int(value[1:])
            sequence["Seq"].append(int(number))
        

        dictionary["Seq"] = sequence["Seq"]
        #dictionary["Seq"].astype(float)
        dictionary.sort_values("Seq")
        self.df_converted = data_convert2
        self.dictionary = dictionary
        return self.df_converted, self.dictionary
    
    def edit_dict(self):
        dict = {}
        for key in self.dict:
            description = str()
            i = 0
            for key_i in self.dict[key].keys():
                value = self.dict[key][key_i]
                if i < len(self.dict[key]) - 1:
                    description += "{value}:{mean},".format(value = value, mean = key_i)
                else: 
                    description += "{value}:{mean}".format(value = value, mean = key_i)
                i += 1

            dict[key] = description

        index = []
        for i in range(len(dict)):
            index.append(i)

        dict4 = {"variable": dict.keys(), "description": dict.values()}
        pd_dict4 = pd.DataFrame(dict4)

        return pd_dict4

    def write(self, path, file_name = 'data_processed.xlsx', data_sheet = 'processed_data', dict_sheet ='dictionary'  ):       
        data.dictionary = data.dictionary.sort_values('Seq')
        data.dictionary = data.dictionary.drop(columns ="Seq")
        with pd.ExcelWriter(path + '/'+ file_name) as writer:
            self.df_converted.to_excel(writer, sheet_name = data_sheet)
            self.dictionary.to_excel(writer, sheet_name = dict_sheet)
    





##########################################Below is the application##########################
# define the path of the dataset
file = "C:/Users/pangj/Box/Jiajun Personal/Statistical Research/Project 4 Survey of winter road information system/Survey/MTURK Result Review/Data processing/Data_raw/All_data_valid_raw.xlsx"
sheet = "Truncated_Raw_data"
#load the data
data = data_conversion(file)
df = data_conversion.read_data(data, file_type = "Excel", sheet_name=sheet)
            
#Customize the question response dictionary
Binary_dict = {"Yes": 1, "No": 0}

Likert_trip_dict = {"Definitely will cancel my trip": 0, 
                    "Somewhat likely": 1,
                    "Very likely": 2, 
                    "Won't cancel my trip": 3}

Frequece_likert_dict = {"Never":0,
                        "Rarely":1,
                        "Sometimes":2,
                        "Usually":3,
                        "Always":4}

Viglence_likert_dict = {"Not at all":0,
                        "A little bit nervous/vigilant":1,
                        "Nervous/vigilant":2,
                        "Very nervous/vigilant":3,
                        "I never experienced this situation":4
                        }
Income_likert_dict = {"Under $15,000":1,
                      "Between $15,000 and $29,999":2,
                      "Between $30,000 and $49,999":3,
                      "Between $50,000 and $74,999":4,
                      "Between $75,000 and $99,999":5,
                      "Between $100,000 and $150,000":6,
                      "Over $150,000":7
                      }

Speed_limit_dict = {"Indifferent":0,
                    "Up to 45 mph":1,
                    "46 mph to 60 mph":2,
                    "61 mph to 75 mph":3,
                    "Higher than 75 mph":4}
  
#specify the questions using customized dictionary
categorical_column = {
    "x10": Binary_dict,
    "x11": Binary_dict, 
    "x12": Binary_dict, 
    "x23": Likert_trip_dict, 
    "x25": Likert_trip_dict, 
    "x27": Likert_trip_dict, 
    "x29": Likert_trip_dict, 
    "x31": Likert_trip_dict, 
    "x33": Likert_trip_dict, 
    "x35": Likert_trip_dict, 
    "x37": Likert_trip_dict, 
    "x39": Likert_trip_dict, 
    "x41": Likert_trip_dict, 
    "x43": Likert_trip_dict, 
    "x45": Likert_trip_dict, 
    "x47": Likert_trip_dict, 
    "x49": Likert_trip_dict, 
    "x51": Likert_trip_dict, 
    "x53": Likert_trip_dict, 
    "x55": Likert_trip_dict, 
    "x57": Likert_trip_dict, 
    "x59": Likert_trip_dict, 
    "x61": Likert_trip_dict, 
    "x63": Likert_trip_dict, 
    "x65": Likert_trip_dict, 
    "x67": Likert_trip_dict, 
    "x69": Likert_trip_dict, 
    "x75": Frequece_likert_dict, 
    "x76": Frequece_likert_dict, 
    "x77": Binary_dict,
    "x88": Binary_dict,
    "x91": Binary_dict,
    "x92": Frequece_likert_dict,
    "x93": Frequece_likert_dict,
    "x96": Viglence_likert_dict,
    "x97": Viglence_likert_dict,
    "x98": Binary_dict,
    "x99": Speed_limit_dict,
    "x109": Income_likert_dict
}
#### The code below is to find which columns don't need the data conversion ####
col_remove = []
for key in data.df.keys():
    values = data.df[key].unique()
    if len(values) > 7:
        col_remove.append(key)

list_1 = ["x17","x79", "x82", "x86","x108", "x111"]
for i in range(len(list_1)):
    col_remove.remove(list_1[i] ) 

list_2 = ["x87", "x95", "x114", "x115", "x116"]
for i in range(len(list_2)):
    col_remove.append(list_2[i])

list_3 = []
for i in range(24, 72, 2):
    list_3.append("x{number}".format(number = i))

for i in range(len(list_3)):
    col_remove.append(list_3[i])


for key in categorical_column.keys():
    response_dict = categorical_column[key]
    data.special_categoryies_pair(key,response_dict)

data.skip_column(col_remove)

#data conversion
data_converted, dictionary = data.data_conversion()

#Save the data and dictionary into excel
save_path = "C:/Users/pangj/Box/Jiajun Personal/Statistical Research/Project 4 Survey of winter road information system/Survey/MTURK Result Review/Data processing/Processed_data"
data.write(save_path)



