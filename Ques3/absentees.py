import os
import pandas as pd
final_df = pd.read_csv('final_reference.csv')
attendance = final_df['Attendance']
length = len(attendance)
absentees = {}
for i in range(0, length) :
    if attendance[i] == 0 :
        absentees[final_df.at[i, 'Name']] =  final_df.at[i, 'RollNo.']
print("Names and roll numbers of absentees are : ")
for key, value in absentees.items() :
    print(key, ' : ', value)
    
