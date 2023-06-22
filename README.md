#####  FastAPI backend API to demonstrate permissioned routes

#####  Stack 
* fastAPI web framework
* Sqlite3 database

#####  Installation
* Use an environment with `python3` installed
* Open a terminal and navigate to project's folder `cd backend/`
* Create a python virtual environment by running the following command:
`python3.11 -m venv python_venv`
* Activate the python virtual environment by running the command:
`source python_venv/bin/activate`
* Install requirements of app by running the following command:
`pip3 install -r requirements.txt`

* Create admin user by inserting directly into `local_storage.db` database via an Sqlite3 browser tool:
  - `INSERT INTO users (email,password,name,surname,register_date, role) VALUES('admin@example.com', '$2b$12$tLGdEP/3.B.sFTNITAfX5uLDzs6kgXq1PU8yxP/EnFIPBBWsvR4HG', 'Admin name', 'Admin surname', '2023-06-21', 'ADMINISTRATOR');`
  - Created user:
    * username: `admin@example.com`
    * password: `1234`
* Run the server
  - `python3.11 main.py`
* Access the API at `localhost:9999/v1`
* Access the API Swagger UI documentation at `localhost:9999/v1/documentation`


