import subprocess
import os
import shutil
import mysql.connector
from dotenv import load_dotenv
import json

load_dotenv()

import requests
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

MYSQL_ROOT = os.getenv("MYSQL_ROOT_USER")
MYSQL_PASS = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")


# 1. Copy Database
# def copy_database(source_db, target_db, user, password):
#     dump_file = f"{source_db}.sql"
#     # print("MYSQL_ROOT", MYSQL_ROOT)
#     # Export
#     os.system(f"mysqldump -u {MYSQL_ROOT} -p{MYSQL_PASS} {source_db} > {dump_file}")

#     # Create target db
#     os.system(f"mysql -u {MYSQL_ROOT} -p{MYSQL_PASS} -e 'CREATE DATABASE IF NOT EXISTS {target_db}'")
#     # create_database(target_db)

#     # Import data
#     os.system(f"mysql -u {MYSQL_ROOT} -p{MYSQL_PASS} {target_db} < {dump_file}")

#     return f"Database copied from {source_db} to {target_db}"

def copy_database(source_db, target_db, user, password):
    """
    Copy a MySQL database:
    1. Creates target DB if not exists
    2. Dumps source DB to temp file
    3. Restores dump into target DB
    """

    dump_file = f"{source_db}.sql"

    # Step 1 → Create target database
    create_db_cmd = [
        "mysql",
        f"-u{MYSQL_ROOT}",
        # f"-p{MYSQL_PASS}",
        "-e",
        f"CREATE DATABASE IF NOT EXISTS `{target_db}`;"
    ]

    print("Creating target database...")
    subprocess.run(create_db_cmd, shell=False, check=True)

    # Step 2 → Dump source database
    dump_cmd = [
        "mysqldump",
        f"-u{MYSQL_ROOT}",
        # f"-p{MYSQL_PASS}",
        source_db
    ]

    print(f"Dumping database '{source_db}'...")
    with open(dump_file, "wb") as f:
        subprocess.run(dump_cmd, stdout=f, shell=False, check=True)

    # Step 3 → Import dump into target
    import_cmd = [
        "mysql",
        f"-u{MYSQL_ROOT}",
        # f"-p{MYSQL_PASS}",
        target_db
    ]

    print(f"Importing into '{target_db}'...")
    with open(dump_file, "rb") as f:
        subprocess.run(import_cmd, stdin=f, shell=False, check=True)

    # Cleanup temp file
    os.remove(dump_file)

    return (f"Database '{source_db}' successfully copied to '{target_db}'!")


def create_database(db_name):
    print("db_name", db_name)
    """
    Creates a new MySQL database if it does not already exist.
    """

    create_db_cmd = [
        "mysql",
        f"-u{MYSQL_ROOT}",
        f"-p{MYSQL_PASS}",
        "-e",
        f"CREATE DATABASE IF NOT EXISTS `{db_name}`;"
    ]

    print(f"Creating database '{db_name}'...")
    subprocess.run(create_db_cmd, shell=False, check=True)
    return (f"Database '{db_name}' created successfully!")

# 2. Create DB Credential
def create_db_user(db_user, db_pass):
    conn = mysql.connector.connect(
        user=MYSQL_ROOT,
        password=MYSQL_PASS,
        host=MYSQL_HOST
    )
    cur = conn.cursor()
    cur.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_pass}'")
    conn.commit()
    return f"Database user created: {db_user}"


# 3. Give Permissions
def grant_permission(db_user, db_name):
    conn = mysql.connector.connect(
        user=MYSQL_ROOT,
        password=MYSQL_PASS,
        host=MYSQL_HOST
    )
    cur = conn.cursor()
    cur.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'%'")
    conn.commit()
    return f"Permissions granted on database {db_name} to {db_user}"


# 4. Create folder
def create_folder(path):
    os.makedirs(path, exist_ok=True)
    return f"Folder created: {path}"


# 5. Folder permission
def set_folder_permission(path, permission):
    os.chmod(path, permission)
    return f"Permission {oct(permission)} applied to {path}"


# 6. Copy file
def copy_file(src, dest):
    shutil.copy(src, dest)
    return f"Copied file from {src} to {dest}"

def copy_files_only(source_folder, destination_folder):
    print("Starting file copy...")

    # Create destination folder if not exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Loop files
    for filename in os.listdir(source_folder):
        src = os.path.join(source_folder, filename)
        dst = os.path.join(destination_folder, filename)

        # Copy only files
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            print(f"Copied: {filename}")

    return f"All files copied successfully."

def copy_all(source_folder, destination_folder):
    print("Copying entire folder...")

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy folder tree
    for root, dirs, files in os.walk(source_folder):
        # Make subdirectories in destination
        for dir_name in dirs:
            dest_dir = os.path.join(destination_folder, os.path.relpath(os.path.join(root, dir_name), source_folder))
            os.makedirs(dest_dir, exist_ok=True)

        # Copy files
        for file_name in files:
            src_file = os.path.join(root, file_name)
            rel_path = os.path.relpath(root, source_folder)
            dest_dir = os.path.join(destination_folder, rel_path)
            os.makedirs(dest_dir, exist_ok=True)

            shutil.copy2(src_file, os.path.join(dest_dir, file_name))
            print(f"Copied: {src_file}")

    return f"Folder copied successfully."

def all_in_one(source_db, target_db, user, password, db_user, db_pass,
               path, src):
    copy_database(source_db, target_db, user, password)
    create_db_user(db_user, db_pass)
    grant_permission(db_user, target_db)
    # create_folder(path)
    # set_folder_permission(path, permission)
    copy_all(src, path)
    # copy_file(src, path)
    return f"Successfully done copy_database, create_db_user, grant_permission, create_folder and copy_all"

def get_data(database, table, columns="*", where=None):
    """
    Fetch data from a table.
    
    :param table: table name
    :param columns: list of columns OR "*" for all
    :param where: optional WHERE condition (string)
    :return: fetched rows as list of dicts
    """

    # Convert list of columns to CSV format
    if isinstance(columns, list):
        columns = ", ".join(columns)

    try:
        conn = mysql.connector.connect(
            user=MYSQL_ROOT,
            password=MYSQL_PASS,
            host=MYSQL_HOST,
            database = database
        )
        cursor = conn.cursor(dictionary=True)

        query = f"SELECT {columns} FROM {table}"

        if where:
            query += f" WHERE {where}"

        # print("Query:", query)

        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    except mysql.connector.Error as err:
        return {"error": str(err)}
    
def insert_data(database, table, data):
    """
    Insert data into a table.
    
    :param table: table name
    :param data: dict of column-value pairs
    :return: success message or error
    """

    try:
        conn = mysql.connector.connect(
            user=MYSQL_ROOT,
            password=MYSQL_PASS,
            host=MYSQL_HOST,
            database = database
        )
        cursor = conn.cursor()

        # print("Data to insert:", data)

        data = json.loads(data)
        
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = list(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        # print("Query:", query)
        # print("Values:", values)

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return {"success": "Data inserted successfully."}

    except mysql.connector.Error as err:
        return {"error": str(err)}
    
def get_weather(city: str):
    API_KEY = WEATHER_API_KEY
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    return requests.get(url).json()
