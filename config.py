PIVOTS = {"IsAfricanAmerican": lambda x: x.attrs["IsAfricanAmerican"] == True,
          "Gender": lambda x: x.attrs["Gender"] == True,
          "OnHypertensionMedication": lambda x: x.attrs["OnHypertensionMedication"] == True,
          "HasDiabetes": lambda x: x.attrs["HasDiabetes"] == True,
          "IsSmoker": lambda x: x.attrs["IsSmoker"] == True,
          "Assessment": lambda x: x.attrs["Assessment"] == True,
          "Age": lambda x: 0 <= x.attrs["Age"] <= 64.57,
          "Systolic Blood Pressure": lambda x: 0 <= x.attrs["Systolic Blood Pressure"] <= 157.04,
          "Total Cholesterol": lambda x: 0 <= x.attrs["Total Cholesterol"] <= 177.78,
          "HDL cholesterol": lambda x: 0 <= x.attrs["HDL cholesterol"] <= 51.27,
         }
    
    
    
PIVOTS_O = {#"HDL cholesterol": lambda x: 0 <= x.attrs["HDL cholesterol"] <= 40,
            "Total Cholesterol": lambda x: 200 <= x.attrs["Total Cholesterol"] <= 300,
            #"Total Cholesterol_140_200": lambda x: 140 <= x.attrs["Total Cholesterol"] <= 200,
            "Systolic Blood Pressure": lambda x: 120 <= x.attrs["Systolic Blood Pressure"] <= 129,
            # "Systolic Blood Pressure_stage1": lambda x: 130 <= x.attrs["Systolic Blood Pressure"] <= 139,
            # "Systolic Blood Pressure_stage2": lambda x: 140 <= x.attrs["Systolic Blood Pressure"] <= 180,
            # "Systolic Blood Pressure_crisis": lambda x: 180 <= x.attrs["Systolic Blood Pressure"] <= 1000
            }