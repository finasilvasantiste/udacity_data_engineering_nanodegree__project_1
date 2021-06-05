# Project: Data Modeling with Postgres

## Summary
- The imaginary startup called Sparkify wants to analyze the data they've been collecting on songs 
  and user activity on their new music streaming app.
- The data sources are log files and song metadata files, both types are in `.json`.
- This ETL Pipeline makes that data available in an easy-to-consume/easy-to-analyze format while making sure
a useful relationship between data points exists, in other words, as tables in a relational db.  

## Set up
- The db runs in a docker container, as described in this [knowledge article](https://knowledge.udacity.com/questions/59537).
- Install the dependencies listed in `requirements.txt`
- Make sure to use Python 3.

## How to run
- From the main project folder, run `python3 create_tables.py` in a terminal to set up tables. If tables already exist,
  they will get deleted and recreated.
- Then run `python3 etl.py` to run the etl process. (`etl_transform_and_load.py` contains methods used in `etl.py`, but `etl.py`
  is the entry point.)
- You can connect to the db directly by running `psql postgresql://student:student@localhost/sparkifydb`, and
check the results by running sql statements inside the psql console.

### Note
I've used the [project specs](https://review.udacity.com/#!/rubrics/2500/view) as guidance for completing the project.
Since the jupyter notebooks aren't part of the specs I went ahead and started working with `etl.py` right away.