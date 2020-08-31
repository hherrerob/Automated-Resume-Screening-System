# PeopleAnalytics Candidates Compare and Filter

This project is an API based off [Automated Resume Screening System](https://www.google.com/search?client=firefox-b-e&q=utomated+Resume+Screening+System), to better filter out candidates and provide the better candidate for an specific offer description.


# Installation
First you have to clone the repo and cd.
Then to install dependencies:

	$ pip install -r requeriments.txt

Then to start the flask server:

	$ python app.py

And you are good to go.

Alternatively you can use [Gunicorn](https://pypi.org/project/gunicorn/) to start the server:

	$ gunicorn --workers 4 --bind 0.0.0.0:5000 --timeout 600 app:app

# Use

This API contains 2 endpoints both accessed by a **POST** request.

## Candidate search

This endpoint is used for searching keywords within all available data for a candidate.

	$ /candidate/search

|PARAMS		|IS REQUIRED	|DESCRIPTION                   			   		|
|---------------|---------------|---------------------------------------------------------------|
|offer		|`True`		|Description for an offer (Works better with long descriptions).|
|candidates	|`True`		|List of candidates to filter.          			|


## Candidate compare
This endpoint is used for comparing an offer with all available data for a candidate.

	$ /candidate/compare

|PARAMS		|IS REQUIRED	|DESCRIPTION                   			   		|
|---------------|---------------|---------------------------------------------------------------|
|search		|`True`		|Text used for candidate comparison.				|
|candidates	|`True`		|List of candidates to filter.          			|

It is mandatory that the list of candidates sent to any of the endpoints has certain format:

```
candidates = [{
	"id": {id of the candidate},
	"description": {Single string containing all the data about a candidate}
}]
```

Meaning that each candidate within the list of candidates must have an **"id"** field and a **"description"** field.