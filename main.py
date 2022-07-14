import os
from telnetlib import STATUS
import pandas as pd
from flask import Flask, render_template, request, send_file
from helper import date_checker1, get_pic, get_geo_info, get_camera_info,  out_dir, date_checker
from merge import merger
from shutil import rmtree




app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap():
    try:
        if request.method == 'POST':

            dirpath = "./static"
            for filename in os.listdir(dirpath):
                filepath = os.path.join(dirpath, filename)
                try:
                    rmtree(filepath)
                    print("gabage removing")
                except OSError:
                    os.remove(filepath)
                    print("gabage removing")

            try:
                search_keyword = request.form['search_keyword']
                min_date = request.form['min_date']
                max_date = request.form['max_date']

                date_status = date_checker1(min_date, max_date)
                if date_status == True:
                    date_status2 = date_checker(min_date, max_date)
                    
                    if date_status2 == True:
                        get_pic(search_keyword,min_date=min_date,max_date=max_date)
                        df_pic = pd.read_csv(out_dir +'/'+search_keyword+'_id.csv',sep=',')
                        get_camera_info(search_keyword, df_pic)
                        get_geo_info(search_keyword, df_pic)
                        merger(search_keyword)
                        return send_file("static"+"/"+search_keyword+"_Merged.csv", attachment_filename=search_keyword+"_Merged.csv")

                

                    else:
                        return "Please re-check the date (min date should be greater than max date / two dates should not be the same date)" 

                else:
                    return "Please select valid date"           
                
                
            except Exception as e:
                return ("Unxpected error ::", e)
    except:
        return "Please Input a valid search keyword"    

           



    

