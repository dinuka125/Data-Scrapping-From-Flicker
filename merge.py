import pandas as pd 
import numpy as np

out_dir = "./static/"


def merger(keyword):
    final_path = out_dir+keyword+"_Merged.csv"
    headers = []
    def header_creator(file_1):
        df = pd.read_csv(file_1)
        columns = list(df.columns)
        for items in columns:
            headers.append(items)
    header_creator('static/'+keyword+'_id.csv')
    header_creator('static/'+keyword+'_camera.csv')
    header_creator('static/'+keyword+'_geo.csv')     

    headers = list(dict.fromkeys(headers))
    merged_df = pd.DataFrame(columns=headers)
    merged_df.to_csv(final_path,sep=",", index=None)

    df_id = pd.read_csv('static/'+keyword+'_id.csv')
    df_id = df_id.drop_duplicates()
    df_id = df_id.to_numpy()
    
    df_camera = pd.read_csv('static/'+keyword+'_camera.csv')  
    df_camera = df_camera.drop_duplicates()  
    df_camera = df_camera.to_numpy()
    
    df_geo = pd.read_csv('static/'+keyword+'_geo.csv')
    df_geo = df_geo.drop_duplicates() 
    df_geo = df_geo.to_numpy()


    final_array = []
    none_merged_array = []

    for item_id in df_id:
        status = False
        for item_camera in df_camera:
                if item_id[0] in item_camera:
                    new_df = np.append(item_id,item_camera[1:])
                    final_array.append(new_df)
                    status = True

        if status == False:
            none_merged_array.append(item_id)


    new_df = pd.DataFrame(final_array)# df which has both pic id csv data and camera info data
    none_merged_df = pd.DataFrame(none_merged_array)
    none_merged_df = none_merged_df.drop_duplicates()#df whih dont have the camera info
    


    array_with_nef_geo = []
    none_merged_geo_array = []

    new_df_for_geo_merge = new_df.to_numpy()

    for item in new_df_for_geo_merge:
        status = False
        for new_item in df_geo:
            if item[0] in new_item:
                new_geo_df = np.append(item, new_item[1:])
                array_with_nef_geo.append(new_geo_df)
                status = True
            
        if status == False:
            none_merged_geo_array.append(item)
    
    array_with_nef_geo_df = pd.DataFrame(array_with_nef_geo)
    none_merged__geo_df = pd.DataFrame(none_merged_geo_array)
    none_merged__geo_df = none_merged__geo_df.drop_duplicates()


    for item in array_with_nef_geo:
        merged_df["pic_id"] = pd.Series(item[0])
        merged_df["url"] = pd.Series(item[1])
        merged_df["tag"] = pd.Series(item[2])
        merged_df['date_taken'] = pd.Series(item[3])
        merged_df['Owner_name'] = pd.Series(item[4])
        merged_df["Camera_Make"] = pd.Series(item[5])
        merged_df["Camera_Model"] = pd.Series(item[6])
        merged_df["Aperture"] = pd.Series(item[7])
        merged_df["Exposure_Program"] = pd.Series(item[8])
        merged_df["ISO"] = pd.Series(item[9])
        merged_df["Metering_Mode"] = pd.Series(item[10])
        merged_df["Flash"] = pd.Series(item[11])
        merged_df["Focal_Length"] = pd.Series(item[12])
        merged_df["Color_Space"] = pd.Series(item[13])
        merged_df["Lens_Model"] = pd.Series(item[14])
        merged_df["latitude"] = pd.Series(item[15])
        merged_df["longitude"] = pd.Series(item[16])
        merged_df["county"] = pd.Series(item[17])
        merged_df["region"] = pd.Series(item[18])
        merged_df["country"] = pd.Series(item[19])
        merged_df.to_csv(final_path,sep=',',header=False ,index=False,mode='a')


    none_merged_geo_array = none_merged__geo_df.to_numpy()

    for item in none_merged_geo_array:
        merged_df["pic_id"] = pd.Series(item[0])
        merged_df["url"] = pd.Series(item[1])
        merged_df["tag"] = pd.Series(item[2])
        merged_df['date_taken'] = pd.Series(item[3])
        merged_df['Owner_name'] = pd.Series(item[4])
        merged_df["Camera_Make"] = pd.Series(item[5])
        merged_df["Camera_Model"] = pd.Series(item[6])
        merged_df["Aperture"] = pd.Series(item[7])
        merged_df["Exposure_Program"] = pd.Series(item[8])
        merged_df["ISO"] = pd.Series(item[9])
        merged_df["Metering_Mode"] = pd.Series(item[10])
        merged_df["Flash"] = pd.Series(item[11])
        merged_df["Focal_Length"] = pd.Series(item[12])
        merged_df["Color_Space"] = pd.Series(item[13])
        merged_df["Lens_Model"] = pd.Series(item[14])
        merged_df["latitude"] = pd.Series("no_info")
        merged_df["longitude"] = pd.Series("no_info")
        merged_df["county"] = pd.Series("no_info")
        merged_df["region"] = pd.Series("no_info")
        merged_df["country"] = pd.Series("no_info")
        merged_df.to_csv(final_path,sep=',',header=False ,index=False,mode='a')    


    final_merge_array = []
    final_none_merge_array = []    

    none_merge = none_merged_df.to_numpy()

    for item in none_merge:
        status = False
        for geo_item in df_geo:
            
            if item[0] in geo_item:
                final_df = np.append(item, geo_item[1:])
                final_merge_array.append(final_df)
                status = True
        if status == False:
            final_none_merge_array.append(item)    
                
    final_none_merge_array_df = pd.DataFrame(final_none_merge_array)
    final_none_merge_array_df = final_none_merge_array_df.drop_duplicates()


    for item in final_merge_array:
        merged_df["pic_id"] = pd.Series(item[0])
        merged_df["url"] = pd.Series(item[1])
        merged_df["tag"] = pd.Series(item[2])
        merged_df['date_taken'] = pd.Series(item[3])
        merged_df['Owner_name'] = pd.Series(item[4])
        merged_df["Camera_Make"] = pd.Series("no_info")
        merged_df["Camera_Model"] = pd.Series("no_info")
        merged_df["Aperture"] = pd.Series("no_info")
        merged_df["Exposure_Program"] = pd.Series("no_info")
        merged_df["ISO"] = pd.Series("no_info")
        merged_df["Metering_Mode"] = pd.Series("no_info")
        merged_df["Flash"] = pd.Series("no_info")
        merged_df["Focal_Length"] = pd.Series("no_info")
        merged_df["Color_Space"] = pd.Series("no_info")
        merged_df["Lens_Model"] = pd.Series("no_info")
        merged_df["latitude"] = pd.Series(item[4])
        merged_df["longitude"] = pd.Series(item[5])
        merged_df["county"] = pd.Series(item[6])
        merged_df["region"] = pd.Series(item[7])
        merged_df["country"] = pd.Series(item[8])
        merged_df.to_csv(final_path,sep=',',header=False ,index=False,mode='a')



    final_none_merge_array_df_array = final_none_merge_array_df.to_numpy()

    for item in final_none_merge_array_df_array:
        merged_df["pic_id"] = pd.Series(item[0])
        merged_df["url"] = pd.Series(item[1])
        merged_df["tag"] = pd.Series(item[2])
        merged_df['date_taken'] = pd.Series(item[3])
        merged_df['Owner_name'] = pd.Series(item[4])
        merged_df["Camera_Make"] = pd.Series("no_info")
        merged_df["Camera_Model"] = pd.Series("no_info")
        merged_df["Aperture"] = pd.Series("no_info")
        merged_df["Exposure_Program"] = pd.Series("no_info")
        merged_df["ISO"] = pd.Series("no_info")
        merged_df["Metering_Mode"] = pd.Series("no_info")
        merged_df["Flash"] = pd.Series("no_info")
        merged_df["Focal_Length"] = pd.Series("no_info")
        merged_df["Color_Space"] = pd.Series("no_info")
        merged_df["Lens_Model"] = pd.Series("no_info")
        merged_df["latitude"] = pd.Series("no_info")
        merged_df["longitude"] = pd.Series("no_info")
        merged_df["county"] = pd.Series("no_info")
        merged_df["region"] = pd.Series("no_info")
        merged_df["country"] = pd.Series("no_info")
        merged_df.to_csv(final_path,sep=',',header=False ,index=False,mode='a')
    