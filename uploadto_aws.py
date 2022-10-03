#from pickle import FALSE
#from select import select
import boto3
import botocore
import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine


class aws_client:
    def __init__(self):
        """
        set up s3 client with bucket and engine for psycopg2 
        """
        ACCESS_ID = input("Enter AWS S3 Access ID: ")
        ACCESS_KEY = input("Enter AWS S3 Access Key: ")
        
        session= boto3.Session(aws_access_key_id=ACCESS_ID,
                                    aws_secret_access_key= ACCESS_KEY,
                                    region_name='eu-west-2')
        self.s3 = session.resource('s3')

        self.s3_client = session.client('s3')
        self.bucket_string = "ukc-images"
        

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = 'ukc-routes.c5dmobddqeyc.eu-west-2.rds.amazonaws.com' # Change it to your AWS endpoint
        USER = 'postgres'
        PASSWORD = input("Enter AWS RDS Password: ")
        PORT = 5432
        DATABASE = 'postgres'
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}") 

    def upload_images_s3(self,img_dict):
        """
        for each image in image dictionary requests image from image source URL and directly uploads to s3 storage without downloading loacally
        """
        image_list = list(img_dict.keys())
        for image in image_list:
            # try:
                image_file = requests.get(img_dict[image]["source"], stream=True)
                object_name = img_dict[image]['s3_object_name']
                self.s3_client.upload_fileobj(image_file.raw, self.bucket_string, object_name)
                print("Image Upload Successful")       

            # except :
            #     print("The Image file was not found or other Error")
           
    def isin_s3(self,object_name):
        """
        tries to load the object from the s3 storage, returns string whether or not the object exists
        """
        try:
            self.s3.Object(self.bucket_string, object_name).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return("object doesnt exist")
            else:
                return("Something else has gone wrong")
        else:
            return("object does exist")


    def download_s3(self,obj_name,file_name):
        """
        downloads object from s3 storage and names file from file_name
        """
        self.s3_client.download_file(self.bucket_string,obj_name,file_name)

    def create_dataframe(self, data, upload):
        """
        create_dataframe(data, upload=True)
        Takes crag dictionary and transfers data into a dataframe. Has the option to upload to AWS RDS.
        """
        if "climbs" in data:
            crag_details = {key: data[key] for key in data.keys() & {"crag_uid","crag_name","crag_URL","rocktype", "guidebook","guidebook_URL","country"}}
            crag_df = pd.DataFrame(crag_details,index=[0])
            climbs_df = pd.DataFrame(data["climbs"]).T
            crag_df = pd.concat([crag_df]*(len(climbs_df)))
            routes_df = pd.concat([climbs_df.reset_index(drop= True),crag_df.reset_index(drop= True)],axis=1)
            
            if upload == True:
                self.__uploadto_RDS(routes_df)
            else:
                return(routes_df)
        else: 
            return("no climbs in data, rotes may already be in database")


    def __uploadto_RDS(self,routes_df):
        """
        uploads the routes dataframe to the AWS RDS using SQLalchemy
        """
        try:
            
            conn = self.engine.connect()
            routes_df.to_sql('routes_dataset', conn, if_exists='append',index=False)
            print("Dataframe Uploded")
        except:
            print("Data Frame Upload FAILED")

    def isin_database(self,value,column):
       with self.engine.connect() as connection:
        try:
            result = connection.execute("SELECT * FROM routes_dataset WHERE routes_dataset.{} = '{}'".format(column,value))
            if result.fetchone() == None:
                return(False)
            else:
                return(True)
        except:
            print(f"Error checking if route {value} is in database (database might not exist) Program will continue")
            return(False)

        

if __name__ == "__main__":
    ukc_s3 = aws_client("ukc-data")

    #testing methods 
    # ukc_s3.upload_src_image("https://imgcdn.ukc2.com/i/55419?fm=webp&time=1162047992&s=9a228b2987fa6763d784f2f123376baf","test_img")
    # ukc_s3.print_allobjects()
    # ukc_s3.download_s3("test_img","testimg.png")
    
    # with open('first_crag.json') as json_file:
    #     crag_data = json.load(json_file)
    # ukc_s3.create_dataframe(crag_data["crag:0"],upload = True)

    print(ukc_s3.isin_database("4994291","route_uid"))