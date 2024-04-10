Welcome to the meal planner app. The purpose of this app is to allow a user to find recipe inspirations using a single ingredient. When the program is run, the user inputs the amount of recipes they'd like to see, along with the primary ingredient they'll be using. For now the program fetches the data using the Spoonacular API and stores it in a PostgreSQL database. Certain error handling conditions are implemented to ensure proper usage. These include limiting the number of recipes per fetch, ensuring no duplicate entries into the db, and ensuring valid ingredient queries. The next stop will be to make this more interactive and displayable through a web page.

Meal Planner App Setup and Run Instructions
Step 1: PostgreSQL Database Setup
Install PostgreSQL if it's not already installed. Download from PostgreSQL official website.

Create a Database and User:

Access psql as a superuser, typically postgres.
Create a new database: CREATE DATABASE my_project_database;
Create a user with a password: CREATE USER my_project_user WITH PASSWORD 'password';
Grant privileges to the user: GRANT ALL PRIVILEGES ON DATABASE my_project_database TO my_project_user;
Create Required Table(s):

Connect to your database: \c my_project_database
Execute the SQL command to create a recipes table:
sql
Copy code
CREATE TABLE recipes (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  image VARCHAR(255) NOT NULL
);
Step 2: Obtain Spoonacular API Key
Sign Up/Log In at Spoonacular API Developer Portal.
Subscribe to the free tier.
Copy Your API Key from the dashboard.
Step 3: Prepare Your Python Environment
Install Python from the official Python website.

Set Up a Virtual Environment (recommended):

Navigate to your project directory.
Create the environment: python -m venv venv
Activate it:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
Install Required Packages:

With the environment activated, run: pip install requests psycopg2
Step 4: Configure and Run the Scripts
Download/Clone Scripts to your project directory.

Configure Scripts:

In db_manager.py, update database connection parameters with your details.
In spoonacular_data_ingestion.py, replace your_spoonacular_api_key with your obtained API key.
Run the Scripts:

Ensure PostgreSQL is running and your virtual environment is activated.
Run db_manager.py to set up the schema.
Run spoonacular_data_ingestion.py to fetch data and insert it into your database.
Step 5: Verify Data Insertion
Using psql:

Access with: psql -d my_project_database -U my_project_user
Query data: SELECT * FROM recipes;
Exit with: \q
Using pgAdmin: Navigate to your recipes table to view the data.

Final Notes
Execute commands and scripts in the correct environment.
Adjust configurations as needed for different environments.
