import boto3
import requests

class aws_client:
    def __init__(self,s3bucket_name):
        """
        set up s3 client and sets bucket
        """
        self.s3_client = boto3.client('s3')
        self.s3 = boto3.resource('s3')
        self.bucket_string = s3bucket_name
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


if __name__ == "__main__":
    ukc_s3 = aws_client("ukc-data")
    #ukc_s3.upload_json("first_crag.json", "fist_crag")
    ukc_s3.upload_src_image("https://imgcdn.ukc2.com/i/55419?fm=webp&time=1162047992&s=9a228b2987fa6763d784f2f123376baf","test_img")
    #ukc_s3.print_allobjects()
    ukc_s3.download_s3("test_img","testimg.png")
    