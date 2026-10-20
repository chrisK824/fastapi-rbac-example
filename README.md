#####  FastAPI backend API to demonstrate permissioned routes

#####  Stack 
* fastAPI web framework
* Sqlite3 database

#####  Installation
* Use an environment with `uv` installed
* Open a terminal and navigate to project's folder `cd backend/`
* Create a python virtual environment by running the following command:
`uv venv -p 3.14 venv`
* Activate the python virtual environment by running the command:
`source venv/bin/activate`
* Install requirements of app by running the following command:
`uv pip install -r requirements.txt`

* Create admin user by inserting directly into `local_storage.db` database via an Sqlite3 browser tool:
  - `INSERT INTO users (email,password,name,surname, role) VALUES('admin@example.com', '$2b$12$tLGdEP/3.B.sFTNITAfX5uLDzs6kgXq1PU8yxP/EnFIPBBWsvR4HG', 'Admin name', 'Admin surname', 'ADMINISTRATOR');`
  - Created user:
    * username: `admin@example.com`
    * password: `1234`
* Run the server
  - `python3.14 main.py`
* Access the API at `localhost:9999/v1`
* Access the API Swagger UI documentation at `localhost:9999/v1/documentation`


