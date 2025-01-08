import os
import pandas as pd
import pymysql
import psycopg2
import tempfile
from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
import openpyxl  # Import openpyxl to handle Excel files

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For flash messages
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()  # Use system's temp folder for uploads
app.config['ALLOWED_EXTENSIONS'] = {'xls', 'xlsx', 'xlsm', 'csv', 'pdf', 'txt', 'html', 'js', 'css', 'mp4'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def connect_to_database(db_type, host, user, password):
    """Connect to MySQL or PostgreSQL based on the selected db_type."""
    connection = None
    try:
        if db_type == 'mysql':
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password
            )
        elif db_type == 'postgresql':
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password
            )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def insert_dataframe_to_db(df, db_type, table_name, host, user, password, database):
    """Insert DataFrame into the selected database."""
    connection = connect_to_database(db_type, host, user, password)
    if connection:
        try:
            # Create database if not exists
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            connection.select_db(database) if db_type == 'mysql' else None

            # Exclude the 'id' column from the DataFrame for the CREATE TABLE statement
            columns = [col for col in df.columns if col.lower() != 'id']
            
            # Create table dynamically, excluding 'id'
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    {', '.join([f"{col} TEXT" for col in columns])}
                )
            """)

            # Insert DataFrame into the table, excluding 'id' in the columns
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
            for row in df.itertuples(index=False):
                cursor.execute(insert_query, tuple(getattr(row, col) for col in columns))
            connection.commit()

        except Exception as e:
            print(f"Error while inserting data into the database: {e}")
        finally:
            cursor.close()
            connection.close()




@app.route('/')
def index():
    # Make sure 'db_connected' is initialized to False if not already set
    if 'db_connected' not in session:
        session['db_connected'] = False  # Initial state (Step 1 shown)
    return render_template('index.html', db_connected=session['db_connected'])


@app.route('/connect', methods=['POST'])
def connect_to_db():
    db_type = request.form['db_type']
    host = request.form['host']
    user = request.form['user']
    password = request.form['password']
    
    connection = connect_to_database(db_type, host, user, password)
    if connection:
        session['db_connected'] = True  # Mark the database as connected
        session['db_type'] = db_type
        session['host'] = host
        session['user'] = user
        session['password'] = password
        flash('Successfully connected to the database!', 'success')
        return render_template('index.html', db_connected=True)
    else:
        session['db_connected'] = False  # Database connection failed
        flash('Failed to connect to the database. Please check your credentials.', 'danger')
        return render_template('index.html', db_connected=False)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    table_name = request.form['table_name']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Read the uploaded file into a DataFrame
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath, engine='openpyxl')
        
        # Log DataFrame to check the data
        print("DataFrame loaded from file:")
        print(df.head())

        db_type = session.get('db_type')
        host = session.get('host')
        user = session.get('user')
        password = session.get('password')
        database = request.form['create_database']

        try:
            insert_dataframe_to_db(df, db_type, table_name, host, user, password, database)
            flash(f"Data successfully inserted into {database} in {table_name} table.", 'success')
        except Exception as e:
            flash(f"Error: {e}", 'danger')
        
        return redirect('/')
    
    flash('Invalid file format. Please upload a valid file.', 'danger')
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
