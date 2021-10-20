import os
import pandas as pd
attendance_contents = open("attendance.txt", "r")
i = 0
presentees = []
for lines in attendance_contents.readlines() :
    if i % 2 != 0 :
        length = len(lines)
        for j in range(length) :
            if lines[j] == "2" :
                presentees.append(lines[j : j + 9])
                break
    i += 1

ref_df = pd.read_csv('reference.csv')
ref_df['Attendance'] = 0
all_students = ref_df['RollNo.']
for i in range(len(presentees)) :
    for j in range(len(all_students)) :
        if int(presentees[i]) == all_students[j] :
            ref_df.at[j, 'Attendance'] = 1
            break
    continue
final_df = ref_df[[ 'S.No.',
                    'RollNo.',
                    'Name',
                    'Attendance']]
final_df.to_csv('final_reference.csv', index = None)







    