class Constant():
    def __init__(self):

        self.static_variables = {
                "industry" : "Categorical", 
                "sector" : "Categorical", 
                "country" : "Categorical",
                "beta" : "Numerical",
                "marketCap" : "Numerical",
                "bookValue" : "Numerical",
                "dividendRate" : "Numerical",
                "dividendYield" : "Numerical",
                "fiveYearAvgDividendYield" : "Numerical",
                "debtToEquity": "Numerical"
            }

        self.feature_variables = {
            "Open" : "Numerical",
            "High" : "Numerical",
            "Low" : "Numerical",
            "Volume" : "Numerical",
            "Month"	 : "Categorical",
            "Day" : "Categorical",
            "Day of The Week"  : "Categorical",
            "Week of The Year" : "Categorical"
        }
        self.indicators = {
            'key' : 'values'
        }

        self.future_feature ={
            "Month"	 : "Categorical",
            "Day" : "Categorical",
            "Day of The Week"  : "Categorical",
            "Week of The Year" : "Categorical"
            }
        
        self.prediction_feature= {
            "Adjusted Close" : "Numerical",
        }

        self.columns_to_scale = ['Open',	'High',	'Low',	'Close',	'Adjusted Close',	'Volume']