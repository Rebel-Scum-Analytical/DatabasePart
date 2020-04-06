import json
import plotly
import plotly.graph_objects as go
import datetime as dt
import pandas as pd
import decimal

data_macro_rda = {\
"female": {"Water": {"13": "2.1","30": "2.7","50": "2.7","70": "2.7","unit": "(L/d)", "18": "2.3","100": "2.7"},\
"Carbohydrate": {"13": "130","30": "130","50": "130","70": "130","unit": "(g/d)","18": "130","100": "130"},\
"Fiber": {"13": "26","30": "25","50": "25","70": "21","unit": "(g/d)","18": "26","100": "21"},\
"Protein": {"13": "34","30": "46","50": "46","70": "46","unit": "(g/d)","18": "46","100": "46"}},\
"Male": {"Water": {"13": "2.4","50": "3.7","70": "3.7","100": "3.7","unit": "(L/d)","18": "3.3","30": "3.7" },\
"Carbohydrate": {"13": "130","50": "130","70": "130","100": "130","unit": "(g/d)","18": "130","30": "130"},\
"Fiber": {"13": "31","50": "38","70": "30","100": "30","unit": "(g/d)","18": "38","30": "38"},\
"Protein": {"13": "34","50": "56","70": "56","100": "56","unit": "(g/d)","18": "52","30": "56"}}}

data_mineral_rda = {
"female": {"Calcium": {"13": "1300","30": "1000","50": "1000","70": "1200","unit": "(mg/d)","18": "1300","100": "1200" },\
"Copper": {"13": "700","30": "900","50": "900","70": "900","unit": "(micro_g/d)","18": "890","100": "900"},\
"Iron": {"13": "8","30": "18","50": "18","70": "8","unit": "(mg/d)","18": "15","100": "8"},\
"Magnesium": {"13": "240","30": "310","50": "320","70": "320","unit": "(mg/d)","18": "360","100": "320"},\
"Manganese": {"13": "1.6","30": "1.8","50": "1.8","70": "1.8","unit": "(mg/d)","18": "1.6","100": "1.8"},\
"Phosphorus": {"13": "1250","30": "700","50": "700","70": "700","unit": "(mg/d)","18": "1250","100": "700"},\
"Selenium": {"13": "40","30": "55","50": "55","70": "55","unit": "(micro_g/d)","18": "55","100": "55"},\
"Zinc": {"13": "8","30": "8","50": "8","70": "8","unit": "(mg/d)","18": "9","100": "8"},\
"Potassium": {"13": "4.5","30": "4.7","50": "4.7","70": "4.7","unit": "(g/d)","18": "4.7","100": "4.7"},\
"Sodium": {"13": "1.5","30": "1.5","50": "1.5","70": "1.3","unit": "(g/d)","18": "1.5","100": "1.2"}},\
"Male": {"Calcium": {"13": "1300","50": "1000","70": "1000","100": "1200","unit": "(mg/d)","18": "1300","30": "1000"},\
"Copper": {"13": "700","50": "900","70": "900","100": "900","unit": "(micro_g/d)","18": "890","30": "900"},\
"Iron": {"13": "8","50": "8","70": "8","100": "8","unit": "(mg/d)","18": "11","30": "8"},\
"Magnesium": {"13": "240","50": "420","70": "420","100": "420","unit": "(mg/d)","18": "410","30": "400"},\
"Manganese": {"13": "1.9","50": "2.3","70": "2.3","100": "2.3","unit": "(mg/d)","18": "2.2","30": "2.3"},\
"Phosphorus": {"13": "1250","50": "700","70": "700","100": "700","unit": "(mg/d)","18": "1250","30": "700"},\
"Selenium": {"13": "40","50": "55","70": "55","100": "55","unit": "(micro_g/d)","18": "55","30": "55"},\
"Zinc": {"13": "8","50": "11","70": "11","100": "11","unit": "(mg/d)","18": "11","30": "11"},\
"Potassium": {"13": "4.5","50": "4.7","70": "4.7","100": "4.7","unit": "(g/d)","18": "4.7","30": "4.7"},\
"Sodium": {"13": "1.5","50": "1.5","70": "1.3","100": "1.2","unit": "(g/d)","18": "1.5","30": "1.5"}}}

data_vitamin_rda = {
"female": {"Vitamin_A": {"13": "600","30": "700","50": "700","70": "700","unit": "micro_g/d","18": "700","100": "700"},\
"Vitamin_C": {"13": "45","30": "75","50": "75","70": "75","unit": "mg/d","18": "65","100": "75"},\
"Vitamin_D": {"13": "15","30": "15","50": "15","70": "15","unit": "micro_g/d","18": "15","100": "20"    },\
"Vitamin_E": {"13": "11","30": "15","50": "15","70": "15","unit": "mg/d","18": "15","100": "15"    },\
"Vitamin_K": {"13": "60","30": "90","50": "90","70": "90","unit": "micro_g/d","18": "75","100": "90"    },\
"Thiamine_VB1": {"13": "0.9","30": "1.1","50": "1.1","70": "1.1","unit": "mg/d","18": "1","100": "1.1"    },\
"Riboflavin_VB2" : {"13": "0.9","30": "1.1","50": "1.1","70": "1.1","unit": "mg/d","18": "1","100": "1.1"    },\
"Niacin_VB3": {"13": "12","30": "14","50": "14","70": "14","unit": "mg/d","18": "14","100": "14"    },\
"Pyridoxine_VB6": {"13": "1","30": "1.3","50": "1.3","70": "1.5","unit": "mg/d","18": "1.2","100": "1.5"},\
"Folate_VB9": {"13": "300","30": "400","50": "400","70": "400","unit": "micro_g/d","18": "400","100": "400"},\
"Cobalamin_VB12": {"13": "1.8","30": "2.4","50": "2.4","70": "2.4","unit": "micro_g/d","18": "2.4","100": "2.4"    },\
"Pantothenic_Acid_VB5": {"13": "4","30": "5","50": "5","70": "5","unit": "mg/d","18": "5","100": "5"    },\
"Choline": {"13": "375","30": "425","50": "425","70": "425","unit": "mg/d","18": "400","100": "425"    }  },\
"Male": {    "Vitamin_A": {"13": "600","50": "900","70": "900","100": "900","unit": "micro_g/d","18": "900","30": "900"    },\
"Vitamin_C": {"13": "45","50": "90","70": "90","100": "90","unit": "mg/d","18": "75","30": "90"    },\
"Vitamin_D": {"13": "15","50": "15","70": "15","100": "20","unit": "micro_g/d","18": "15","30": "15"    },\
"Vitamin_E": {"13": "11","50": "15","70": "15","100": "15","unit": "mg/d","18": "15","30": "15"    },\
"Vitamin_K": {"13": "60","50": "120","70": "120","100": "120","unit": "micro_g/d","18": "75","30": "120"    },\
"Thiamine_VB1": {"13": "0.9","50": "1.2","70": "1.2","100": "1.2","unit": "mg/d","18": "1.2","30": "1.2"    },\
"Riboflavin_VB2": {"13": "0.9","50": "1.3","70": "1.3","100": "1.3","unit": "mg/d","18": "1.3","30": "1.3"    },\
"Niacin_VB3": {"13": "12","50": "16","70": "16","100": "16","unit": "mg/d","18": "16","30": "16"    },\
"Pyridoxine_VB6": {"13": "1","50": "1.3","70": "1.7","100": "1.7","unit": "mg/d","18": "1.3","30": "1.3"    },\
"Folate_VB9": {"13": "300","50": "400","70": "400","100": "400","unit": "micro_g/d","18": "400","30": "400"    },\
"Cobalamin_VB12": {"13": "1.8","50": "2.4","70": "2.4","100": "2.4","unit": "micro_g/d","18": "2.4","30": "2.4"    },\
"Pantothenic_Acid_VB5": {"13": "4","50": "5","70": "5","100": "5","unit": "mg/d","18": "5","30": "5"    },\
"Choline": {"13": "375","50": "550","70": "550","100": "550","unit": "mg/d","18": "550","30": "550"    }}}


def createJson(daily_stats):
# kilocalorie values generally reflect industry practices 
# of calculating kilocalories as 4, 4, or 9 kilocalories per gram of protein, carbohydrate, and fat, respectively
#pg #14 sr28_doc.pdf
    user_data = {\
    "calories":{"total":daily_stats.cal,\
        "proteins":(daily_stats.protein)*4, \
        "carbohydrates":(daily_stats.carbs)*4,\
        "fats":(daily_stats.fats)*9 } ,\
    "macronutrients":{"Water":(daily_stats.water)/1000,\
        "Carbohydrate": daily_stats.carbs, \
        "Fiber": daily_stats.fiber,\
        "Protein": daily_stats.protein},\
    "minerals":{ "Calcium": daily_stats.calcium, \
        "Copper": (daily_stats.copper)*1000 ,  \
        "Iron": daily_stats.iron,\
        "Magnesium":  daily_stats.magnesium,\
        "Manganese": daily_stats.manganese,   \
        "Phosphorus": daily_stats.phosphorus,\
        "Selenium": daily_stats.selenium,\
        "Zinc": daily_stats.zinc,\
        "Potassium": (daily_stats.potassium)/1000,\
        "Sodium": (daily_stats.sodium)/1000,      \
        },\
    "vitamins": {"Vitamin_C": daily_stats.vitamin_C,\
        "Cobalamin_VB12":daily_stats.vitamin_B12,\
        "Thiamine_VB1":daily_stats.thiamin,\
        "Riboflavin_VB2":daily_stats.riboflavin,\
        "Niacin_VB3":daily_stats.niacin,\
        "Pantothenic_Acid_VB5":daily_stats.panto_acid_VB5,\
        "Pyridoxine_VB6":daily_stats.vitamin_B6,\
        "Folate_VB9": daily_stats.folate,\
        "Vitamin_D":daily_stats.vitamin_D,\
        "Vitamin_K":daily_stats.vitamin_K,\
        "Vitamin_E":daily_stats.vitamin_E,\
        "Vitamin_A":daily_stats.vitamin_A,\
        "Choline":daily_stats.choline\
        }\
    }
    return user_data

def creatUserPersonalJson(user_info):
    user_personal_data = {\
    "height": user_info.height,\
    "weight": user_info.weight,\
    "gender": list(user_info.gender)[0],\
    "date_of_birth":user_info.dob,\
    "physical_activity_level":list(user_info.phy)[0]\
    }
    return user_personal_data


def creatplotdata(user_info):
    userdata_nutrition_data = user_info["userdata_nutrition_data"]
    user_personal_data = user_info["user_personal_data"]
    plot_type = user_info["plot_type"]
    y1 = []
    current_values = []
    y2 =[]
    temp = []
    query_data1={
    "age_key" :returnAgekey(user_personal_data["date_of_birth"]),
    "gender": user_personal_data["gender"]
    }
    query_data2={
    "age_key" :returnAgekey(user_personal_data["date_of_birth"]),
    "gender": user_personal_data["gender"],
    }
    query_data3={            
    "gender": user_personal_data["gender"],
    "age_key": "unit"
    }

    if(plot_type == "Micro Nutrients" or plot_type=="All"):
        y1 = []
        current_values = []
        y2 =[]
        temp = []

        y1.append(userdata_nutrition_data["minerals"].keys())
        y1.append(userdata_nutrition_data["vitamins"].keys())

        y1_1 = [i for item in y1 for i in item]
    
        for key, value in userdata_nutrition_data["minerals"].items(): 
            query_data1["nutrient"] = key
            query_data3["nutrient"] = key
            current_values.append((userdata_nutrition_data["minerals"][key])*100)
            temp.append(dri_micro_nutrient_minerals(query_data1))
            y2.append(f"Max value : {dri_micro_nutrient_minerals(query_data1)}, {dri_micro_nutrient_minerals(query_data3)}")


        for key, value in userdata_nutrition_data["vitamins"].items(): 
            query_data2["nutrient"] = key
            query_data3["nutrient"] = key
            current_values.append(userdata_nutrition_data["vitamins"][key]*100)
            temp.append(dri_micro_nutrient_vitamins(query_data2))
            y2.append(f" Max value : {dri_micro_nutrient_vitamins(query_data2)}, {dri_micro_nutrient_vitamins(query_data3)}")
        temp = [float(i) for item in temp for i in item]
        perc_s = [i / j for i, j in zip(current_values, temp)] 


        trace1 = [
            {
                "x":y1_1,
                "y":perc_s,
                "hoverinfo":y2,
                "type": 'bar',
                
            }
        ]
    if(plot_type == "Macro Nutrients" or plot_type=="All"):
        y1 = []
        current_values = []
        y2 =[]
        temp = []
        y1.append(userdata_nutrition_data["macronutrients"].keys())
        y1_1 = [i for item in y1 for i in item]
        query_data={
            "age_key" :returnAgekey(user_personal_data["date_of_birth"]),
            "gender": user_personal_data["gender"]
        }
        for key, value in userdata_nutrition_data["macronutrients"].items():
          
            query_data["nutrient"] = key
            query_data3["nutrient"] = key
            current_value = userdata_nutrition_data["macronutrients"][key]
            current_values.append(userdata_nutrition_data["macronutrients"][key]*100)
            temp.append(dri_macro_nutrient(query_data))
            
            y2.append(f"   Current Value : {current_value},Max Value: {dri_macro_nutrient(query_data)} {dri_macro_nutrient(query_data3)}")
        temp = [float(item) for item in temp]
        
        perc_s = [i / j for i, j in zip(current_values, temp)] 
        trace2 = [
            {
                "x":y1_1,
                "y":perc_s,
                "hoverinfo":y2,
                "type": 'bar',
                
            }
        ]
    if(plot_type == "Calories" or plot_type=="All"):
        data = userdata_nutrition_data["calories"]
        total = data["total"]
        del data["total"]
        y1_1 = [item for item in data.keys()]
        current_values = [item for item in userdata_nutrition_data["calories"].values()]
        trace3 = [
            {
                "labels":y1_1,
                "values":current_values,
                
                "type": 'pie',
                
            }
        ]

    layout2=dict(
                title='Macro Nutrients'
            )
    layout1=dict(
            title='Micro Nutrients'
        )
    layout3=dict(
        title=f'Calories Distribution of {total} KCal'
    )    
    graphs = [ {"data" : trace2, "layout": layout2}, {"data" : trace1,"layout":layout1} ,{"data" : trace3,"layout": layout3 }]
   
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == "__main__":
    print(creatplotdata())

def calculateAge(dob):
   
    today =dt.date.today()
    user_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return user_age

def returnAgekey(dob):   
    today =dt.date.today()
    user_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if(user_age <= 13):
        age_key = "13"
    elif ((user_age>= 14) and (user_age<= 18)):    
        age_key = "18"
    elif((user_age>= 19) and (user_age<= 30)):    
        age_key = "30"
    elif((user_age>= 31) and (user_age<= 50)):    
        age_key = "50"    
    elif((user_age>= 51) and (user_age<= 70)):    
        age_key = "70"
    else: 
        age_key = "100"
    
    return age_key

def calcPhysicalMultiplier(PAL):
    switcher={
            'Sedentary':1.2,
            'Lightly_active':1.375,
            'moderately_active':1.55,
            'very_active':1.725,
            'extra_active':1.9,               
            }
    return switcher.get(PAL,1.2)

def calculateCalories(user_personal_data):
    if(user_personal_data["gender"] == "Male"):
        bmr = (66 + 6.3*user_personal_data["weight"] + 12.9*user_personal_data["height"] -\
            6.8*calculateAge(user_personal_data["date_of_birth"]))    
    else:
        bmr = (655 + 4.3*user_personal_data["weight"] +\
            4.7*user_personal_data["height"] -\
            4.7*calculateAge(user_personal_data["date_of_birth"]))    
    return(bmr*calcPhysicalMultiplier(user_personal_data["physical_activity_level"]))
    

def dri_macro_nutrient(data):
    return data_macro_rda[data["gender"]][data["nutrient"]][data["age_key"]]


def dri_micro_nutrient_minerals(data):
    values = [] 
    values.append(data_mineral_rda[data["gender"]][data["nutrient"]][data["age_key"]])
    return values


def dri_micro_nutrient_vitamins(data):
    values = []   
    values.append(data_vitamin_rda[data["gender"]][data["nutrient"]][data["age_key"]])
    return values

