# CSV to MySQL Importer Web App

A Flask-based web application that imports CSV files into MySQL databases. Supports both local and remote MySQL connections.

## Features
- CSV file upload functionality
- MySQL database integration
- Local and remote database support
- Simple web interface
- Data validation before import

## Prerequisites
- Python 3.x
- MySQL Server (local or remote)
- pip package manager

## Installation

### Local Database Setup
1. Clone this repository locally:
    ```bash
    git clone https://github.com/pankaj8782/Excel_to_SQL
    cd path/to/folder
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create your MySQL database and table structure

## Usage

### Local Deployment
1. Start the Flask application:
    ```bash
    python app.py
    ```

2. Access the web interface at:
    ```
    http://127.0.0.1:5000
    ```

### Remote Database Deployment
For online database connections, use our hosted version:  
[https://sql-importer.onrender.com](https://sql-importer.onrender.com)

## Configuration
- Modify `app.py` for database credentials
- Adjust allowed file types in `app.config['ALLOWED_EXTENSIONS']`
- Set debug mode (`DEBUG = False` for production)

## How to Use
1. Access the web interface
2. Connect to your MySQL database
3. Upload CSV file through the web form
4. Map CSV columns to database fields
5. Review and confirm import
6. View success message or error details

## Database Setup Example
Create your MySQL table (adjust columns according to your CSV structure):
    ```sql
    CREATE TABLE your_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        column1 VARCHAR(255),
        column2 INT,
        ...
    );
    ```

## License
[MIT License](LICENSE)

## Notes
- Ensure MySQL server is running before starting the application
- CSV file must have header row matching database columns
- Maximum file size limited to 16MB by default

## Troubleshooting
- Check MySQL connection credentials
- Verify database user privileges
- Ensure CSV format matches table structure
- Check error logs in terminal

## Acknowledgments
- Flask Framework
- MySQL Connector/Python
- CSV module

---

**Replace these placeholders in your actual implementation:**
1. `https://github.com/pankaj8782/Excel_to_SQL` - Your Git repository URL
2. Database credentials in `app.py`
3. Table structure in SQL example
4. Update license file if needed
