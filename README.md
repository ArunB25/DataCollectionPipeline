# DataCollectionPipeline
AiCore Data collection pipeline project

This project uses slenium on a chrome driver to scrape the web.
A zoopla scraper was initially created to understand how to use xpath and seleniums others tools.

Then a scraper was made to go through the ukc website and collect all of the guide books that are in prints URLs of a certain country. It has several methods that get all of the crags from each guidebook along with details of the crag. For each the all of the buttresses with routes there details can be retrieved, along with the images from the crag page.
A nested dictionary stores the crags,with the buttresses there climbs and the images of the crag.

Test file for the ukc scraper was made to verify the public methods return the corect data types under correct and incrorrect inputs and cirumstances.

uploadto_aws file was created with methods to upload to aws cloud storage. Images uploaded to an s3 storage bucket, using the boto3 library, using the requests function images are got from the source url. There are also other methods to get a list of all the objects in the storage and to download specifice objects. Additional methods using pandas made to take routes dictionary from the scraper and transform it into a routes dataframe, which can be uploaded to an postgreSQL AWS RDS using sqlalchemy.
More methods added to verify whether objects are in the S3 or RDS storage already, by checking if uniqe id exists. 

A docker image of the scraper was created and pushed to the docker hub. Docker allows applications to be containerised with all the neccassary prerequisites including the operating system, programing language and libaries to execute the application. To create a docker image a docker file was required. The docker file contains all the steps to setup and run the application, its language is very similar to the CLI. Nearly all docker images are build upon an existing image in this case the python image.

If the scraper was to be run at a reoccuring set time, it would be tedious to keep manually running it. Contrab is a built in feature of linux that allows tasks to be scheduled. If the physical computer wasnt on however, the scheduled task wouldnt be able to be executed. AWS EC2 enables users to create instances of cloud computers, this means tasks could be scheduled to run no matter when so long as the instance is running. 
A EC2 instance was created to test if the docker image on the docker hub could be pulled and ran on the EC2 instance.