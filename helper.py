from multiprocessing.connection import wait
import flickrapi
from matplotlib.pyplot import get
import pandas as pd
from datetime import date


api_key ="35883a31753987d251ef52f0cc2dcb79"
api_secret = "29eebe28b4a9a808"
min_date = '2018-01-01'
out_dir = "static"

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')

def date_checker1(min_date, max_date):
    today = date.today()
    if min_date and max_date <= str(today):
        return True
    else:
        False    

       

def date_checker(min_date, max_date):
    if min_date < max_date :
        return True
    else:
        return False    

def get_pic(tag,min_date,max_date):
    flickr=flickrapi.FlickrAPI(api_key,api_secret,cache=True, format='etree')
    
    print(min_date)
    print(max_date)

    try:
        if min_date == "":
            min_date = '2018-01-01'
        if max_date == "":
            max_date = '2018-01-02'  
        photos=flickr.walk(tags=tag,extras='url_c,date_taken,owner_name',sort='interestingness-desc',content_type='1',min_upload_date =min_date ,max_upload_date =max_date)
    except Exception as e:
        print(e)
    
    file_name = tag + '_id.csv'
    full_name = out_dir + '/' + file_name
    df_pic = pd.DataFrame(columns=['pic_id','url','tag','date_taken','Owner_name'])
    df_pic.to_csv(full_name,sep=',',index=None)
    total = 0
    amount = 0
    drop_nan = 0
    
    for photo in photos:
            
        exist = photo.get('url_c')!= 0
        if exist:
            df_pic['pic_id'] = pd.Series(str(photo.get('id')))
            url = photo.get('url_c')
            if url != None:
                df_pic['url'] = pd.Series(photo.get('url_c'))
            else:
                df_pic['url'] = pd.Series('No_url')   


            # value = pd.Series(photo.get('url_c'))
            # if value != "":
            #     df_pic['url'] = value
            # else:
            #     df_pic['url'] = pd.Series("no_info")
            
            amount += 1
        else:
            drop_nan += 1
        
        df_pic['tag'] = tag
        df_pic['date_taken'] = pd.Series(photo.get('datetaken'))
        df_pic['Owner_name'] = pd.Series(photo.get('ownername'))      
        df_pic.to_csv(full_name,sep=',',index=False,header=None,mode='a')
        df_pic = pd.DataFrame()
        
        total += 1
    

       
    return


def get_camera_info(search_keyword, df_pic):
    df_info = pd.DataFrame(columns=['pic_id','Camera_Make','Camera_Model',
                                    'Aperture','Exposure_Program',
                                    'ISO','Metering_Mode','Flash','Focal_Length',
                                    'Color_Space','Lens_Model'])
    file_name = search_keyword+"_camera.csv"
    full_name = out_dir + '/' + file_name
    df_info.to_csv(full_name, sep=",", index=None)                          

    df_pic_list = df_pic['pic_id'].tolist()
    for i in range(len(df_pic_list)):
        try:
            flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
            # exif = flickr.photos.getExif(photo_id=df_pic['pic_id'].iloc[i])
            exif = flickr.photos.getExif(photo_id=df_pic_list[i])
            info_get = exif['photo']['exif']
            for info in info_get:
                if info['label'] == 'Make':
                    df_info['Camera_Make'] = pd.Series(info['raw']['_content'])
                elif info['label'] == 'Model':
                    df_info['Camera_Model'] = pd.Series(info['raw']['_content'])
                elif info['label'] == 'Aperture':
                    df_info['Aperture'] = pd.Series(float(info['raw']['_content'].strip()))
                elif info['label'] == 'Exposure Program':
                    df_info['Exposure_Program'] = pd.Series(info['raw']['_content'])
                elif info['label'] == 'ISO Speed':
                    df_info['ISO'] = pd.Series(float(info['raw']['_content'].strip()))
                elif info['label'] == 'Metering Mode':
                    df_info['Metering_Mode'] = pd.Series(info['raw']['_content'])
                elif info['label'] == 'Flash':
                    df_info['Flash'] = pd.Series(info['raw']['_content'])
                elif info['label'] == 'Focal Length':
                    df_info['Focal_Length'] = pd.Series(float(info['raw']['_content'].replace('mm','').strip()))
                elif info['label'] == 'Color Space':
                    df_info['Color_Space'] = pd.Series(info['raw']['_content'])
                elif info['label'] == 'Lens Model':
                    df_info['Lens_Model'] = pd.Series(info['raw']['_content'])
                elif info['label'] == "" :
                       df_info['Lens_Model'] = pd.Series("No_info")
                
            df_info['pic_id'] = df_pic['pic_id'].iloc[i]
            df_info.to_csv(full_name,sep=',',index=None,header=None,mode='a')          

        except Exception as e:
            print("API limit reached at Camera Info :: ",e)             
                

def get_geo_info(search_keyword, df_pic):
    file_name = search_keyword+"_geo.csv"
    full_name = out_dir + '/' + file_name
    df_info = pd.DataFrame(columns=['pic_id','latitude','longitude','county','region','country'])
    df_info.to_csv(full_name, sep=",", index=None)

    df_pic_list = df_pic['pic_id'].tolist()
    for i in range(len(df_pic_list)):
        flickr=flickrapi.FlickrAPI(api_key,api_secret,format='parsed-json')
        try:
            
            pic_geo = flickr.photos.geo.getLocation(photo_id=str(df_pic_list[i]))
            geo = pic_geo['photo']['location']

            for loc in geo:
                df_info['pic_id'] = df_pic['pic_id'][i]
                if loc == 'latitude':
                    df_info[loc] = pd.Series(geo[loc])
                if loc == 'longitude':
                    df_info[loc] = pd.Series(geo[loc])
                if loc == 'county':
                    df_info[loc] = pd.Series(geo[loc]['_content'])
                if loc == 'region':
                    df_info[loc] = pd.Series(geo[loc]['_content'])
                if loc == 'country':
                    df_info[loc] = pd.Series(geo[loc]['_content'])

            df_info.to_csv(full_name,sep=',',index=False,header=None,mode='a')     

        except Exception as e:
            print("No geo info for this pic at geo :: ",e)
            pass  

   


# def merge(search_keyword):
#     full_dir = out_dir + '/' + search_keyword
#     df_pic = pd.read_csv("static"+"/"+search_keyword+'_id.csv',sep=',')
#     df_exif = pd.read_csv("static"+"/"+search_keyword+'_camera.csv',sep=',')
#     df_geo = pd.read_csv("static"+"/"+search_keyword+'_geo.csv',sep=',')

#     df_merge = pd.merge(df_pic, df_exif, on=['pic_id','pic_id'])
#     df_merge = pd.merge(df_merge, df_geo, on=['pic_id','pic_id'])
#     df_merge.to_csv(full_dir+"_Merged.csv", sep=',', index=None)

#     return df_merge
  
    
   
    
           

    


# get_pic(search_keyword)   
# df_pic = pd.read_csv(search_keyword+'_id.csv',sep=',') 
# get_camera_info(search_keyword, df_pic)
# get_geo_info(search_keyword, df_pic)
# merge(search_keyword)

# def manually_merge(file1, file2):
#     file1 = pd.read_csv(file1,sep=',')
#     file2 = pd.read_csv(file2,sep=',')

#     pic_id = file1['pic_id']
#     file2['pic_id'] = pic_id
#     for item in pic_id:
#         if item in file2['pic_id']:
#             print("Found")
      

# manually_merge('Sri lanka_id.csv','Sri lanka_exif.csv')
