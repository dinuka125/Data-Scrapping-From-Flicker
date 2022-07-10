import os
import pandas as pd
from flask import Flask, render_template, request, send_file
from app import get_pic, get_geo_info, get_camera_info,  out_dir
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
                get_pic(search_keyword)
                df_pic = pd.read_csv(out_dir +'/'+search_keyword+'_id.csv',sep=',')
                get_camera_info(search_keyword, df_pic)
                get_geo_info(search_keyword, df_pic)
                merger(search_keyword)
                return send_file("static"+"/"+search_keyword+"_Merged.csv", attachment_filename=search_keyword+"_Merged.csv")
                
            except:
                print("error")
                return ("Unxpected error")
    except:
        return "Please Input a valid search keyword"    

           



    

