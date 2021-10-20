from flask import Flask, render_template, request, redirect, url_for, session
import os 
import codecs
import pandas as pd
import numpy as np
app = Flask(__name__, template_folder= 'template' , static_folder='static')

UPLOAD_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def upload() :
    file1 = request.files['file1']
    file1.save(os.path.join(app.config['UPLOAD_FOLDER'], 'proxy_attendance.txt'))

@app.route("/", methods = ['GET', 'POST'])
def home() :
    if request.method == 'POST' :
        attendance_contents = open("./static/output/proxy_attendance.txt", "r")
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

        first_name = []
        last_name=[]
        names_dict = {'first_name' : 'last_name'}
        for i in range(len(names)) :
            names[i] = names[i].split(' ')
            first_name.append(names[i][0])
            last_name.append(names[i][1])

        ref_df = pd.read_csv('C:\\Users\\''Mitika Bhadada''\\Desktop\\''ML assignment''\\Ques5\\static\\output\\reference.csv',error_bad_lines=False, encoding = 'latin1')
        roll_num = np.array(roll_num)
        ref_df['Attendance'] = 0
        all_students = ref_df['RollNo.']

        for i in range(len(roll_num)) :
            for j in range(len(all_students)) :
                if roll_num[i] == all_students[j] :
                    ref_df.at[j, 'Attendance'] = 1
                    break
            continue

        for i in range(len(presentees)) :

            for j in range(1, len(all_students)) :
                stud = ref_df.at[j, 'Name'].split(' ')
                if len(stud) >= 2 :
                    if first_name[i].upper() in stud and last_name[i].upper() in stud :
                        if roll_num[i] != ref_df.at[j, 'RollNo.'] :
                            for k in range(1, len(all_students)) :
                                if roll_num[i] == ref_df.at[k, 'RollNo.'] :
                                    ref_df.at[k, 'Attendance'] = 0
                                    break
                else :
                    if first_name[i].upper() in stud or last_name[i].upper() in stud :
                        if roll_num[i] != ref_df.at[j, 'RollNo.'] :
                            for k in range(1, len(all_students)) :
                                if roll_num[i] == ref_df.at[k, 'RollNo.'] :
                                    ref_df.at[k, 'Attendance'] = 0
                                    break
            continue
        final_df = ref_df[[ 'S.No.',
                    'RollNo.',
                    'Name',
                    'Attendance']]
        final_df.to_csv('./static/output/results.csv', index = None)
    return render_template('home.html')
app.run(debug=True)
