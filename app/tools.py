import subprocess
import os
import shutil
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

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
        f"-p{MYSQL_PASS}",
        "-e",
        f"CREATE DATABASE IF NOT EXISTS `{target_db}`;"
    ]

    print("Creating target database...")
    subprocess.run(create_db_cmd, shell=False, check=True)

    # Step 2 → Dump source database
    dump_cmd = [
        "mysqldump",
        f"-u{MYSQL_ROOT}",
        f"-p{MYSQL_PASS}",
        source_db
    ]

    print(f"Dumping database '{source_db}'...")
    with open(dump_file, "wb") as f:
        subprocess.run(dump_cmd, stdout=f, shell=False, check=True)

    # Step 3 → Import dump into target
    import_cmd = [
        "mysql",
        f"-u{MYSQL_ROOT}",
        f"-p{MYSQL_PASS}",
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
