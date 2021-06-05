# Project: Data Modeling with Postgres

## Set up
- The db runs in a docker container, as described in this [knowledge article](https://knowledge.udacity.com/questions/59537).
- Install the dependencies listed in `requirements.txt`
- Make sure to use Python 3.

## How to run
- From the main project folder, run `python3 create_tables.py` to set up tables.
- Then run `python3 etl.py` to run the etl process.
- You can connect to the db directly by running `psql postgresql://student:student@localhost/sparkifydb`.

### Note
I've used the [project specs](https://review.udacity.com/#!/rubrics/2500/view) as guidance for completing the project.
Since the jupyter notebooks aren't part of the specs I went ahead and started working with `etl.py` right away.