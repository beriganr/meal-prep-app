## Meal Planner App Setup and Run Instructions

### Step 1: PostgreSQL Database Setup

1. **Install PostgreSQL** if it's not already installed on your machine. Download it from the [official PostgreSQL website](https://www.postgresql.org/download/).

2. **Create a Database and User**:
   - Open the PostgreSQL command line tool, `psql`, logged in as a superuser (usually `postgres`).
   - Create a new database: `CREATE DATABASE my_project_database;`
   - Create a user with a password: `CREATE USER my_project_user WITH PASSWORD 'password';`
   - Grant privileges to the user: `GRANT ALL PRIVILEGES ON DATABASE my_project_database TO my_project_user;`

3. **Create the Required Table(s)**:
   - Connect to the database: `\c my_project_database`
   - Create a `recipes` table:
     ```sql
     CREATE TABLE recipes (
       id SERIAL PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       image VARCHAR(255) NOT NULL
     );
     ```

### Step 2: Obtain Spoonacular API Key

1. Sign Up or Log In to the [Spoonacular API Developer Portal](https://spoonacular.com/food-api).
2. Subscribe to the free tier to get this project up and running.
3. Copy Your API Key from your Spoonacular API dashboard.

### Step 3: Prepare Your Python Environment

1. Install Python if not already installed. Download it from the [official Python website](https://www.python.org/downloads/).

2. **Set Up a Virtual Environment** (optional but recommended):
   - Navigate to your project directory in the terminal or command prompt.
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment:
     - Windows: `venv\Scripts\activate`
     - macOS/Linux: `source venv/bin/activate`

3. **Install Required Packages**:
   - Ensure your virtual environment is activated.
   - Install `requests` and `psycopg2` using pip: `pip install requests psycopg2`

### Step 4: Configure and Run the Scripts

1. Download or Clone the Scripts into your project directory.

2. **Configure the Scripts**:
   - Open `db_manager.py` and `spoonacular_data_ingestion.py` in a text editor.
   - In `db_manager.py`, update the database connection parameters (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) with your own.
   - In `spoonacular_data_ingestion.py`, replace `your_spoonacular_api_key` with the API key you obtained from Spoonacular.

3. **Run the Scripts**:
   - Ensure your PostgreSQL server is running and your virtual environment is activated.
   - First, run `db_manager.py` to set up the database schema: `python db_manager.py`
   - Next, run `spoonacular_data_ingestion.py` to fetch data from the Spoonacular API and insert it into your database: `python spoonacular_data_ingestion.py`

### Step 5: Verify Data Insertion

- **Using `psql`**:
  - Start with the command: `psql -d my_project_database -U my_project_user`
  - Query the contents of the database using `SELECT * FROM recipes;`
  - When done, enter `\q`

### Final Notes

- Ensure all commands and scripts are executed in the correct environment (e.g., the virtual environment, if used).
- Adjust configurations, like the database connection details and the API key, as needed for different environments (development, testing, production).
