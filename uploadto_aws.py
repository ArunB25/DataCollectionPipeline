import boto3
import requests
import pandas as pd
import json
from sqlalchemy import create_engine


class aws_client:
    def __init__(self,s3bucket_name):
        """
        set up s3 client and sets bucket
        """
        self.s3_client = boto3.client('s3')
        self.s3 = boto3.resource('s3')
        self.bucket_string = s3bucket_name
        
        self.DATABASE_TYPE = 'postgresql'
        self.DBAPI = 'psycopg2'
        self.ENDPOINT = 'ukc-database-datacollectionpipeline.cg8b8vgge9xb.eu-west-2.rds.amazonaws.com' # Change it to your AWS endpoint
        self.USER = 'postgres'
        self.PASSWORD = 'Aicore123'
        self.PORT = 5432
        self.DATABASE = 'postgres'


    def upload_json(self,json_file,obj_name):
        """
        Requires name of json file (with .json in string) and the desired object name for the json file and uploads the json file to the s3 database
        """
        response = self.s3_client.upload_file(json_file, self.bucket_string, obj_name)
    def upload_src_image(self,img_url,obj_name):
        """
        requests image from image source URL and directly uploads to s3 storage without downloading loacally
        """
        try:
            image = requests.get(img_url, stream=True)
            self.s3_client.upload_fileobj(image.raw, self.bucket_string, obj_name)
            print("Upload Successful")       

        except :
           print("The file was not found or other Error")
           
    def print_allobjects(self):
        """
        prints all object names in s3 storage
        """
        bucket = self.s3.Bucket(self.bucket_string)
        for file in bucket.objects.all():
            print(file.key)

    def download_s3(self,obj_name,file_name):
        """
        downloads object from s3 storage and names file from file_name
        """
        self.s3_client.download_file(self.bucket_string,obj_name,file_name)

    def create_dataframe(self, data, upload):
        """
        Takes crag dictionary and transfers data into a dataframe. Has the option to upload to AWS RDS.
        """
        crag_details = {key: data[key] for key in data.keys() & {"crag uid","crag name","crag URL","rocktype", "guidebook","guidebook URL"}}
        crag_df = pd.DataFrame(crag_details,index=[0])
        climbs_df = pd.DataFrame(data["climbs"]).T
        crag_df = pd.concat([crag_df]*(len(climbs_df)))
        routes_df = pd.concat([climbs_df.reset_index(drop= True),crag_df.reset_index(drop= True)],axis=1)
        
        if upload == True:
            self.uploadto_RDS(routes_df)
        else:
            return(routes_df)
    
    def uploadto_RDS(self,routes_df):
        """
        uploads the routes dataframe to the AWS RDS using SQLalchemy
        """
        engine = create_engine(f"{self.DATABASE_TYPE}+{self.DBAPI}://{self.USER}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DATABASE}") 
        conn = engine.connect()
        routes_df.to_sql('routes_dataset', conn, if_exists='replace',index=False)


        

if __name__ == "__main__":
    ukc_s3 = aws_client("ukc-data")

    #testing methods 
    # ukc_s3.upload_json("first_crag.json", "fist_crag")
    # ukc_s3.upload_src_image("https://imgcdn.ukc2.com/i/55419?fm=webp&time=1162047992&s=9a228b2987fa6763d784f2f123376baf","test_img")
    # ukc_s3.print_allobjects()
    # ukc_s3.download_s3("test_img","testimg.png")
    
    with open('first_crag.json') as json_file:
        crag_data = json.load(json_file)
    ukc_s3.create_dataframe(crag_data["crag:0"],upload = True)