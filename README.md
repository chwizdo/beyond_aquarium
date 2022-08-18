# beyond_aquarium
FYP project for client_20220723

## Prerequisite:

1. Install Docker Desktop here in your local machine.
2. Run Docker Desktop and keep it open for the entire process.

## Steps to Run Project:

1. Open a terminal console of your choice (CMD or PowerShell for Windows users, or terminal for Mac users). Alternative: Open the project in VSCode and use the built-in terminal.
2. Go to the root of the project.

```
cd [path_to_project_folder]
```

3. Run the following commands to start the server up.

```
docker-compose build
```

then

```
docker-compose up
```

4. Check if the server is running by going to ```localhost:8000/admin``` in your preferred browser. if the page is not accessible (means server not running), hit ```Ctrl+C``` on your keyboard to stop any running servers, and run ```docker-compose up``` again. Try it a few times until the server starts running.

5. After the server is booted up, open another terminal console (keep the previous one active) and run this command to get into the Docker environment.

```
docker exec -it beyond_aquarium_web bash
```

6. Now create database tables that the system will need in order to function by running the command below.

```
python manage.py migrate
```

7. Finally import initial data setup into the database, which consist of default user accounts and other sample data.

```
python manage.py loaddata initial_data.json
```

## Usage:

1. Go to ```localhost:8000/auth/login``` in your preferred browser choice to visit the unified login page for all different user account roles.
2. Here're the list of default accounts (with unique roles) to use:
   1. customer@gmail.com, customer
   2. staff@gmail.com, staff
   3. admin@gmail.com, admin
