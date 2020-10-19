
import pandas as pd
import json

'''
{"root": {"exit_status": 0, 
		  "message": "", 
		  "data": {"days": [{"day": "22/01/2020", 
		  					"data": {"data": 555.0, 
		  							"deaths": 17.0, 
		  							"forecast": 1874.2731475019, 
		  							"delta_data": 99.0, 
		  							"delta_forecast": 172.86696545566633
		  							}
		  					}, 
		  					{"day": "23/01/2020", 
		  					"data": {"data": 654.0, 
		  							"deaths": 18.0, 
		  							"forecast": 2047.1401129575663, 
		  							"delta_data": 99.0, 
		  							"delta_forecast": 172.86696545566633
		  							}
		  					}],
		  		   "total_cases_until_today": 1345048.0, 
		  		   "total_cases_in_30days": 19751993.49211943, 
		  		   "active_cases_today": 101488.0, 
		  		   "active_cases_in_30days": 1666992.1276092455, 
		  		   "peak": {"day": "05/05/2020", "data": 1666992.1276092455}, 
		  		   "country": "World"
		  		   }
		  }
}
'''

class Output():
    
    @staticmethod
    def add_peak(dtf):
        data_max = dtf["delta_data"].max()
        forecast_max = dtf["delta_forecast"].max()
        if data_max >= forecast_max:
            peak = dtf[dtf["delta_data"]==data_max].index[0]
            return peak, data_max
        else:
            peak = dtf[dtf["delta_forecast"]==forecast_max].index[0]
            return peak, forecast_max
                
    
    def create_output(self, dtf, country):
        dtf.index = dtf.index.strftime("%d/%m/%Y")
        self.dic = {}
        
        ## main data
        self.dic["days"] = [{"day":k, "data":v} for k,v in dtf.fillna("").to_dict("index").items()]
        
        ## total cases
        self.dic["total_cases_until_today"] = dtf["data"].max()
        self.dic["total_cases_in_30days"] = dtf["forecast"].max()
        
        ## active cases
        self.dic["active_cases_today"] = dtf["delta_data"].max()
        self.dic["active_cases_in_30days"] = dtf["delta_forecast"].max()
        
        ## peak
        peak_day, peak_data = self.add_peak(dtf)
        self.dic["peak"] = {"day":peak_day,"data":peak_data}
        
        ## add country
        self.dic["country"] =  country
        
    