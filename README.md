# Population Data Analysis and SQL Export

## Description
This project processes historical population data and exports it into an SQL database. It utilizes Python scripts, CSV files, and a Jupyter notebook to extract, transform, and load (ETL) population and demographic data for regions, departments, and communes in France.

## Features
- **Data Preparation:**
  - Extract and clean data from multiple CSV sources.
  - Transform data into structured formats for Regions, Departments, Communes, Years, and Statistical information.
- **Database Integration:**
  - Supports multiple database dialects (MySQL, PostgreSQL, SQLite, and MSSQL).
  - Dynamically creates and populates database tables.
- **Statistical Insights:**
  - Historical population trends, birth/death rates, and housing data.

## File Structure
- **`createEmptyDTB.sql`**: SQL script for initializing an empty database.
- **`CSV_to_SQL.py`**: Python script to process CSV files and populate a SQL database.
- **`Project_BDD.ipynb`**: Jupyter notebook for exploring and visualizing the population data.
- **Data Files:**
  - `populationDepartementsFrance.csv`: Population data by department.
  - `populationMetaDataSerieHistorique2020.csv`: Metadata for historical population series.
  - `populationSerieHistorique2020.csv`: Historical population data.

## Requirements
### Python Packages
Install the required Python libraries:
```bash
pip install pandas sqlalchemy numpy
```

### Database Setup
Ensure you have a database instance (MySQL, PostgreSQL, SQLite, or MSSQL) available. Configure the database connection in the script by providing:
- Username
- Password
- Host
- Database dialect

## Usage
### Running the Python Script
1. Place the CSV files in a folder named `SourceData`.
2. Run the script using the following command:
   ```bash
   python CSV_to_SQL.py <username> <password> <host> <database_dialect>
   ```
   - Replace `<username>`, `<password>`, `<host>`, and `<database_dialect>` with the actual database credentials and type.
   - Use `nopass` if no password is required.

## Data Description
- **Regions**: Information about French regions (code and name).
- **Departments**: Data about departments, linked to their respective regions.
- **Communes**: Information on communes, including their size and department.
- **Years**: Yearly ranges for statistical aggregation.
- **Statistics**: Data for population, births, deaths, and housing for each year range.

## License
This project is open-source and available under the MIT License.

---
**Authors:**
- **ANTOGNELLI Pauline**
- **BENAMAR Yassine**
- **GARCIA Jeanne**
- **MARIAU Julia**

