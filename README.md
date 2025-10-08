# The database schema is fully normalized into multiple related tables that represent different aspects of the property data:

property: Contains core property information including address, type, size, year built, amenities, and location details.  
valuation: Multiple valuation records per property capturing list price, Zestimate, ARV, rent estimates, etc.  
hoa: Homeowners association flags and fees associated with properties.  
rehab: Rehabilitation flags and cost estimates per property.  
taxes: Property tax-related records including tax rates and valuations.  
leads: Lead review status, market, source, and related metadata.  

Each table uses primary keys and foreign keys (property_id) to enforce relationships. The schema uses string types for textual descriptive fields (e.g. train proximity, water source) to avoid type mismatch errors encountered with integer columns.

The schema design balances normalization with the need to preserve all raw data semantics described in the Field Config file.

## **How to Run and Test the Scripts**

### Prerequisites

Install Python 3.8 or higher
Docker Desktop running and configured
MySQL Docker container as specified below
Network connectivity to localhost:3306

### Step-by-step

### Clone the repo and rename the directory to include your full name:  
git clone [https://github.com/100x-Home-LLC/data_engineer_assessment.git](https://github.com/100x-Home-LLC/data_engineer_assessment.git)  
mv data_engineer_assessment data_engineer_assessment_newton_sathyavety  
cd data_engineer_assessment_newton_sathyavety  

### Start the MySQL Docker container:  
docker-compose -f docker-compose.initial.yml up --build -d

### Create your normalized schema in the MySQL database:  
mysql -u root -p6equj5_root home_db < sql/01_schema.sql

### Install required Python libraries:  
pip install -r requirements.txt

### Use the raw JSON data file at data/fake_property_data.json.

### Run the ETL script to ingest and normalize data:  
python scripts/etl-script.py

Verify the data is successfully loaded and normalized into the MySQL tables.

### Step-by-step (PowerShell-friendly)

1. Clone the repo and rename the directory to include your full name:

```powershell
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
mv data_engineer_assessment data_engineer_assessment_newton_sathyavety
cd data_engineer_assessment_newton_sathyavety
```

2. Start the MySQL Docker container:

```powershell
docker-compose -f docker-compose.initial.yml up --build -d
```

3. Copy the schema file into the running MySQL container and apply it:

- Find the container name or id (example below uses a container named `mysql_ctn`):

```powershell
docker ps
```

- Copy the schema file from the host into the container:

```powershell
docker cp .\sql\01_schema.sql mysql_ctn:/tmp/01_schema.sql
```

- Enter the container's shell:

```powershell
docker exec -it mysql_ctn bash
```

- Run the mysql client inside the container to load the schema. When prompted for the password, enter: `6equj5_db_user`.

```bash
mysql -u db_user -p home_db < /tmp/01_schema.sql
# Enter password: 6equj5_db_user
```

- Exit the container shell when finished:

```bash
exit
```

- Optional: run the mysql client from the host if port 3306 is exposed:

```powershell
mysql -h 127.0.0.1 -P 3306 -u db_user -p home_db < .\sql\01_schema.sql
# Enter password: 6equj5_db_user
```

4. Create and activate a Python virtual environment (PowerShell):

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run (as Administrator):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

5. Install required Python libraries:

```powershell
pip install -r .\scripts\requirements.txt
```

6. Use the raw JSON data file at `data/fake_property_data.json`.

7. Run the ETL script to ingest and normalize data (PowerShell):

```powershell
python .\scripts\etl_script.py
```

Notes:
- The ETL script is `scripts/etl_script.py` (check for similar filenames like `etl-script.py`).
- Ensure your virtual environment is activated before running the script.
- To stop the Docker containers later:

```powershell
docker-compose -f docker-compose.initial.yml down
```

Each table uses primary keys and foreign keys (`property_id`) to enforce relationships. The schema uses string types for textual descriptive fields (e.g., train proximity, water source) to avoid type mismatch errors encountered with integer columns.

The schema design balances normalization with the need to preserve all raw data semantics described in the Field Config file.

---

## ETL Logic

- The ETL is implemented in Python in `scripts/etl-script.py`.
- It reads the JSON file, performs cleansing and transformation of data types.
- It splits nested arrays of valuations, HOA, and rehab records into separate normalized tables.
- Inserts data into MySQL using hand-written parameterized queries preserving data integrity.
- Uses transactional commits and rollbacks to ensure clean database state on errors.
- Handles special data mappings and null values as per the field configuration.

---

## Requirements

All dependencies are listed in `requirements.txt`. Key packages include:

- `mysql-connector-python` (MySQL database connection)
- `pandas` (for data manipulation)
- `python-dotenv` (for environment variable management, optional)
- `numpy` (dependency for pandas)

### Example `requirements.txt`:
```

mysql-connector-python==8.0.33
numpy==1.24.3
pandas==2.0.3
protobuf==3.20.3
python-dateutil==2.9.0.post0
python-dotenv==1.0.0
pytz==2025.2
six==1.17.0
tzdata==2025.2

```

---

All source codes, schema, and scripts required to reproduce end-to-end data ingestion are provided in their respective `sql/` and `scripts/` directories.

---

For any questions or clarifications, please contact me via the repository.
