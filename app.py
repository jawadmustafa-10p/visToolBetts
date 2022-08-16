from cgi import test
from tokenize import Name
import streamlit as st
import pandas as pd
import numpy as np
from m import TestData
import subprocess
import os
import json
from pymongo import MongoClient
cols = st.columns([2,1,2,4])


updated_job_values = {
    "baseSalaryLow": 80200,
    "baseSalaryHigh": 122000,
    "OTERangeHigh": 100030,
    "OTERangeLow": 8000123,
    "isRemote": False,
    "yearsOfRequiredExperience": "0-1 yrs",
    "averageDealSize":">250",
    "averageDealCycle":"12+",
    "quotaAttainment":"250K-500K",
    "newNewBusiness":"100",
    "customerSize":"SMB",
    "soldIntoDepartments":["Developers", "Brands", "HR"],
    "soldIntoLevels": ["VP", "Director","Staff"]
}
updated_cand_values = {

    "desiredBaseSalary": 100000,
    "desiredOTE":90000,
    "availableRemotely":"yes",
    "interestedCities": [],
     "workExperiencePositionDurations": [{}],
    "bookOfBusiness":"25",
    "annualQuota":"<250K",
    "soldIntoLevels": ["Director","Staff"],
     "annualPipelineQuota":"",
    "averageDealSize": ">250",
     "notableAccounts":"",
     "responsibilities":"",
     "monthlyQualifiedMeetingsQuota":"",
    "customerSize": "F1000",
     "annualTeamQuota": "",
    "candidateClientVerticals": ["Agriculture", "Advertising"],
    "soldIntoDepartments": ["Brands","HR"],
     "measuredBy":"",
    "quotaAttainmentScore": 120,
    "averageDealCycle": "1-3"
}

cols[0].write("Candidate Values")



cand_values_arr = []
for i in updated_cand_values.keys():
    cand_values_arr.append(cols[0].text_input(i, updated_cand_values[i],key="cand"+i))

count = 0
for j in updated_cand_values.keys():
    if j in ['desiredBaseSalary', 'desiredOTE', 'interestedCities', 'workExperiencePositionDurations', 'soldIntoLevels', 'candidateClientVerticals', 'soldIntoDepartments', 'quotaAttainmentScore']:
        updated_cand_values[j] = eval(cand_values_arr[count])
        count+=1
    else:
        updated_cand_values[j] = cand_values_arr[count]
        count+=1

# cols[1].json(updated_cand_values)
cols[2].write("Job Values")
job_values_arr = []
for i1 in updated_job_values.keys():
    job_values_arr.append(cols[2].text_input(i1, updated_job_values[i1],key="jobs"+i1))

count1 = 0
for j1 in updated_job_values.keys():
    if j1 in ['baseSalaryLow', 'baseSalaryHigh', 'OTERangeHigh', 'OTERangeLow', 'isRemote', 'soldIntoDepartments', 'soldIntoLevels']:
        updated_job_values[j1] = eval(job_values_arr[count1])
        count1+=1
    else:
        updated_job_values[j1] = job_values_arr[count1]
        count1+=1

# cols[3].json(updated_job_values)


testData_obj = TestData()

if cols[3].button('Submit input'):
     cols[3].write('Submitting updated values')
     testData_obj.update_job_values(updated_job_values)
     testData_obj.update_cand_values(updated_cand_values)
     cols[3].write("submitted")
else:
    cols[3].write('Waiting for submission')

if cols[3].button("Run Pipeline and generate Score"):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://jawad:betts@cluster0-shard-00-00.e4wxf.mongodb.net:27017,cluster0-shard-00-01.e4wxf.mongodb.net:27017,cluster0-shard-00-02.e4wxf.mongodb.net:27017/?ssl=true&replicaSet=atlas-enqd3d-shard-0&authSource=admin&retryWrites=true&w=majority"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    #db
    db = client.connectTest
    db["scores"].delete_many({})
    wd = os.getcwd()
    os.chdir("/home/jawad/betts/connect-recommendation-engine/ml")
    process2 = subprocess.Popen(["./run_ml_main.sh"],shell=True)
    cols[3].write("Started pipeline")
    cols[3].write("Wait...")
    process2.wait()
    cols[3].write("Completed Pipeline!")
    cols[3].write("Getting Scores")
    cols[3].write("Wait..")
    cursor = list(db["scores"].find({}))[0]
    for i in cursor.keys():
        cols[3].write(str(i) + " : " + str(cursor[i]))