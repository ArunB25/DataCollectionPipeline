# DataCollectionPipeline
AiCore Data collection pipeline project

This project uses slenium on a chrome driver to scrape the web.
A zoopla scraper was initially created to understand how to use xpath and seleniums others tools.

Then a scraper was made to go through the ukc website and collect all of the guide books that are in prints URLs of a certain country. It has several methods that get all of the crags from each guidebook along with details of the crag. For each the all of the buttresses with routes there details can be retrieved, along with the images from the crag page. A unique v4 UUID is generated for each picture

A nested dictionary stores the crags,with the buttresses there climbs and the images of the crag. The dictionary is saved to a .json file.

Test file for the ukc scraper was made to verify the methods return the corect data types under correct and incrorrect inputs and cirumstances.