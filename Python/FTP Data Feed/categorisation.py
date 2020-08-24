import numpy as np
import pandas as pd
import csv
import os
import pymongo
import re


def findCat(category, name, gender):
    outcome = ()
    assignedcat = ''
    
    
    ##LOAD IN categories.csv in DF
    cats = pd.read_csv('categories.csv', sep = ",",header=None,error_bad_lines=False,low_memory=False)
    cats.columns = [
                "srchterm",
                "voscat",
                "vossubcat",
                "gender"
                ]


    if gender == 'female' or gender == 'Female' or gender == "Women's" or gender == 'Women' or gender == "women's":
        if name is not None or name is not None:
            for index, row in cats.iterrows():
                ##ASSIGN category variables from cats DF
                searchtermtemp = row["srchterm"]
                voscat = row["voscat"]
                voscubcat = row["vossubcat"]
                gender = row["gender"]
                        
                if gender == 'female':
                    searchterm = (r'\b' + searchtermtemp + r'\b')
                    if re.search(searchterm, name, re.I):
                        category = (voscat,voscubcat)
                        assignedcat = category
                    else:
                        pass
                else:
                    pass     
        ##No assignment has been made therefore error has occured, log for investigation
        if  assignedcat == '':
            outcome = ''
                
    elif gender == 'male' or gender == 'Male' or gender == "Men's" or gender == 'Men' or gender == "men's":
        if name is not None or name is not None:
            for index, row in cats.iterrows():
                ##ASSIGN category variables from cats DF
                searchtermtemp = row["srchterm"]
                voscat = row["voscat"]
                voscubcat = row["vossubcat"]
                gender = row["gender"]
                        
                if gender == 'male':
                    searchterm = (r'\b' + searchtermtemp + r'\b')
                    if re.search(searchterm, name, re.I):
                        category = (voscat,voscubcat)
                        assignedcat = category
                    else:
                        pass
                else:
                    pass 
        ##No assignment has been made therefore error has occured, log for investigation        
        if  assignedcat == '':
            outcome = ''
                
    else:
        print('Gender Error in Categorisation')
        outcome = 'Error'
        
    

    ######IF THE OUTCOME OF NAME SEARCHTERM IS BLANK THEN TRY CATEGORY ON SEARCHTERM
    if assignedcat == '':
        if category is not None:
            if gender == 'female' or gender == 'Female' or gender == "Women's" or gender == 'Women' or gender == "women's":
                for index, row in cats.iterrows():
                    ##ASSIGN category variables from cats DF
                    searchtermtemp = row["srchterm"]
                    voscat = row["voscat"]
                    voscubcat = row["vossubcat"]
                    gender = row["gender"]    
                    if gender == 'female':
                        searchterm = (r'\b' + searchtermtemp + r'\b')
                        if re.search(searchterm, str(category), re.I):
                            category = (voscat,voscubcat)
                            assignedcat = category
                        else:
                            pass
                    else:
                        pass    
                ##No assignment has been made therefore error has occured, log for investigation
                if  assignedcat == '':
                    outcome = ''
                        
            elif gender == 'male' or gender == 'Male' or gender == "Men's" or gender == 'Men' or gender == "men's":
                    for index, row in cats.iterrows():
                        ##ASSIGN category variables from cats DF
                        searchtermtemp = row["srchterm"]
                        voscat = row["voscat"]
                        voscubcat = row["vossubcat"]
                        gender = row["gender"]      
                        if gender == 'male':
                            searchterm = (r'\b' + searchtermtemp + r'\b')
                            if re.search(searchterm, str(category), re.I):
                                category = (voscat,voscubcat)
                                assignedcat = category
                            else:
                                pass
                        else:
                            pass 
                            
                            
    ##Handle products that dont match any searchterm, this will return 'Error' which will log output of error products in the return methods
    if assignedcat is None or assignedcat == '':
        outcome = 'Error'
    else:
        outcome = assignedcat 
    
    
    return outcome
    
