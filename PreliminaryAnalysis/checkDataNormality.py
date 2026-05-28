from preliminaryAnalysis import data
from scipy.stats import shapiro
from pprint import pprint
data_asArray = list(data.items())
p_value_list = []
for key in data.keys() :
     row_values = data[key]
     p_value_list.append(float(shapiro(row_values).pvalue))
     
pprint(p_value_list)
for el in p_value_list :
    if float(el) <= 0.05 :
        print (True)

