import os
from flask import Flask
from flaskext.mysql import MySQL  # For newer versions of flask-mysql

app = Flask(__name__)

mysql = MySQL()

# Using environment variables for flexibility (optional)
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER', 'db_user')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD', 'Passw0rd')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB', 'employee_db')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST', '18.101.105.198')

mysql.init_app(app)

@app.route("/")
def main():
    return "Welcome!"

@app.route('/how are you')
def hello():
    return 'I am good, how about you?'

@app.route('/read from database')
def read():
    
    # Open a new connection for each request
    conn = mysql.connect()
    cursor = conn.cursor()

    if conn.open:
            print("✅ Successfully connected to the database!")
    
    cursor.execute("USE employee_db")
    
    cursor.execute("SELECT * FROM employees")
    row = cursor.fetchone()
    result = []
    
    while row is not None:
        result.append(row[0])  # Assuming the first column contains the data you need
        row = cursor.fetchone()

    cursor.close()  # Always close the cursor
    conn.close()    # Always close the connection

    return ",".join(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
