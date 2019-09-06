# Senior Data Eng Homework

What follows is the instructions to run my solution to the data eng homework. Thanks for taking the time to review.

## Setup
---
From the top level directory

```
# Build & run the Docker image
docker build -t "hinge:postgres" ./docker/postgres
docker run -d -p 5432:5432 hinge:postgres

# Setup virtualenv and install project dependencies
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Fix the errors in the datasets (see below)
python ./scripts/fix_files.py --input-file-dir ./dataset

# Load the data into postgres
python ./scripts/load_datasets.py --input-file-dir ./dataset --user postgres --pwd password

# Run queries
See ANSWERS.md

```




### Fixing errors in input data
---

Visually inspecting the datasets I noticed there are issues in some of the csv files.

I chose to fix these files separately instead of during the ingestion stage to modularize the ingestion. 

Typically in this situation I would advocate that the third party take the action to fix the dataset before receipt takes place, but for completeness I've created a script to fix the data. The script can be expanded by adding to the `regex_sub_dict` patterns if further issues arise.

