**Author: Facundo Padilla**

**Social networks:**

- Facebook: https://www.facebook.com/facundodeveloper

- Instagram: https://www.instagram.com/facundodeveloper

- LinkedIn: https://www.linkedin.com/in/facundopadilla

- Udemy: https://www.udemy.com/user/facundo-padilla/

# **Version:**

- 1.0: 
	- 01/02/2021 (DD-MM-YYYY)
	-  02/01/2021 (MM-DD-YYYY)
	-  2021/02/01 (YYYY-MM-DDDD)

# What is this?:

- This Flask project is reusable and also an example of how to merge *Flask, Docker, Nginx, Gunicorn, MySQL, new: Flask-RESTX,  Factory Method design pattern,* and other optional dependencies such as D*ynaconf, Marshmallow, SQLAlchemy, Faker, PyMySQL, Pytest, etc...* which are installed inside the virtual environment "*env_flask*".

# How to use it?

- Easy, if you have Docker Compose installed, just run the following command inside the project directory: *docker-compose up*

- You can also use the commands created inside the "Makefile" file, simply by executing the "make" command; make [OPTION] - Example: *make full-start*

- Once you execute any of these commands, it starts to create the containers to work, they are already linked so you should have no problems to get it to work
- Once you have finished running and creating the containers, simply go to http://localhost:80/

# Initialize application:

- After you have executed the commands like *docker-compose up, make full-start* or whatever you have created in the Makefile or used, it automatically creates the tables and works without problems, the tables are created in the predefined database with the name "*flask_api*", if you want to change the name of this database just go to the file "docker-compose.yaml" and change the environment variable "*MYSQL_DATABASE*". 

- And that's it, once the tables are created, you only have to go to http://localhost:80 (Nginx)

# "Hot-Reloading":

- You could use Watchman to do hot-reaload, but it gives some problems/bugs, so you can directly work with the virtual environment "*env_flask*" and start working there to simulate a hot-reload, also, it is not recommended that a container contains integrated hot-realoading if it is going to be used for hot-reloading.

- **How to activate env_flask**:

	- **Linux / PowerShell**:
		
		1) Run: pip3 install virtualenv && python3 -m virtualenv env_flask
		2) Enter directory *../env_flask/bin/activate* and execute: **source activate** (in the terminal)
		3) Return to the path where **run_debug.py** is found, and run: pip install -r requirements.txt
		4) Run the following commands:
			- *export FLASK_APP=run_debug.py*
			- *flask run -h 0.0.0.0 -p 5001*(the host and port can be changed to the one you want)
			or
			- *python run_debug.py*

	- **Windows:**
		
		1) Run: pip3 install virtualenv && python3 -m virtualenv env_flask
		2) Enter directory ../env_flask/bin/activate and execute: **activate** in CMD
		3) Return to the path where **run_debug.py** is found, and run: pip install -r requirements.txt
		4) Run the following commands:
			- *set FLASK_APP=run_debug.py*
			- *flask run -h 0.0.0.0 -p 5001* (the host and port can be changed to the one you want)
			or
			- *python run_debug.py*
			
**ATTENTION:** in the Dynaconf configuration file (*settings.toml*), when running the *run_debug.py* , the MySQL connection points to *localhost* and port *3307*, if it is going to be uploaded to production, remove the "expose" option from the docker-file.yaml file.

- **Deactivate the virtual environment:**

	- Execute *deactivate* in the terminal or CMD

# Settings:

- **docker-compose.yaml:**

	- **MySQL (db)**:

		- MYSQL_USER: the user name you want to customize (the root user is default and cannot be deleted)

		- MYSQL_PASSWORD= the password of the user (not the root)

		- MYSQL_DATABASE= name of the database you want

		- MYSQL_ROOT_PASSWORD= root user password

		- More documentation: https://hub.docker.com/_/mysql

	- **Flask (flask_app)**:

		- PYTHONBUFFERED= by default leave it set to 1, it is used to display Python logs.

		- ENVVAR_PREFIX_FOR_DYNACONF= the name of our module

		- ENVVAR_FOR_DYNACONF= file name with extension ".toml", Dynaconf supports several others: https://dynaconf.readthedocs.io/en/docs_223/guides/examples.html

		- FLASK_APP= the name of the Python file to be executed by the server

		- FLASK_RUN_HOST= the host address of the application, defaulting to 0.0.0.0

		- FLASK_DEBUG= WARNING!, 1 enables debug, 0 for production.

		- command: Gunicorn command to execute

		- More documentation: https://hub.docker.com/_/python

	- **Nginx (nginx lol)**:

		- Read the docs: https://hub.docker.com/_/nginx

- **settings.toml (Dynaconf file):**
	- [default]
		- SQLALCHEMY_TRACK_MODIFICATIONS = "False" (is a setting that is no longer used, leave it at false)
	- [development]:
		> When you switch to debug mode, the db name becomes localhost and port 3307.
		- DEBUG = "True"
		- SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost:port/db_name"
		
	- [production]:
		> When in production, mostly in the docker, it keeps running this configuration
		- DEBUG = "False"
		- SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@db_container_name/db_name"

# python run.py vs flask run:

- The difference between using Python to execute "run.py" and using "flask run", is that when you have the file "\_\_module__.py" in the project, Python automatically adds it to the "syspath", in the case of "flask run", this does not happen, even if there is the "\_\_init__.py" and the "\_\_module__.py" , so to avoid problems when working with flask run, in each \_\_init__.py file the following code fragment is added:

	    import sys
	    sys.path.append(".")
