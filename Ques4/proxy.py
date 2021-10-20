import os
import pandas as pd
import numpy as np
attendance_contents = open("proxy_attendance.txt", "r")
i = 0
presentees = {}
names = []
roll_num = []

for lines in attendance_contents.readlines() :
    length = len(lines)
    if i % 2 == 0 :
        for j in range(length) :
            if "0" <= lines[j] <= "9" :
                names.append(lines[0 : j])
                break
    
    if i % 2 != 0 :
        for k in range(length) :
            if lines[k] == "2" :
                roll_num.append(int(lines[k : k + 9]))
                break
    i += 1
for name, roll in zip(names, roll_num) :
    presentees[name] = [roll]

proxy = []
presentees_names = names

first_name = []
last_name=[]
names_dict = {'first_name' : 'last_name'}
for i in range(len(names)) :
    names[i] = names[i].split(' ')
    first_name.append(names[i][0])
    last_name.append(names[i][1])

ref_df = pd.read_csv('final_reference.csv')
roll_num = np.array(roll_num)

all_students = ref_df['RollNo.']
for i in range(len(presentees)) :

    for j in range(1, len(all_students)) :
        stud = ref_df.at[j, 'Name'].split(' ')
        if len(stud) >= 2 :
            if first_name[i].upper() in stud and last_name[i].upper() in stud :
                if roll_num[i] != all_students[j] :
                    for k in range(1, len(all_students)) :
                        if roll_num[i] == all_students[k] :
                            
                            proxy.append([roll_num[i], ref_df.at[k, 'Name'], ref_df.at[j, 'Name']])
                            break
        else :
            if first_name[i].upper() in stud or last_name[i].upper() in stud :
                if roll_num[i] != ref_df.at[j, 'RollNo.'] :
                    for k in range(1, len(all_students)) :
                        if roll_num[i] == all_students[k] :
                            
                            proxy.append([roll_num[i], ref_df.at[k, 'Name'], ref_df.at[j, 'Name']])
                            break
    continue
print('Students who used someone for proxy')
print(['Roll No.', 'Name', 'Proxy done by'])
print(proxy)
