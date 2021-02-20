from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_mysqldb import MySQL
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'adventureworks'
mysql = MySQL(app)



@app.route('/update', methods=['POST'])
def update_contact(id):
    content=request.json
    Title= content['Title']
    FirstName = content['First_Name']
    MiddleName = content['MiddleName']
    LastName content['LastName']
    email = content['EmailAddress']
    phone = content['Phone']
    password=content['password']
    cur = mysql.connection.cursor()
    cur.execute("""
            UPDATE adventureworks.contact
            SET Tittle = %s,
                FirstName = %s,
                MiddleName = %s,
                LastName = %s,
                email = %s,
                phone = %s,
                password = %s
            WHERE EmaiAddress = %s
        """, (Title,MiddleName,LastName,email,phone,password,email))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<email>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM adventureworks.contact WHERE EmailAddress = %s'.format(id))
    mysql.connection.commit()
    f={"status":"Data deleted succesfully”}
    return jsonify(f)
    
@app.route('/request/<email>', methods = ['POST', 'GET'])
def get_contacts(email):
    cur = mysql.connection.cursor()
    cur.execute('SELECT Title,FirstName,MiddleName,LastName,EmailAddress,Phone,ModifiedDate,PasswordHash FROM adventureworks.contact WHERE EmailAddress = %s', [email])
    data = cur.fetchall()
    cur.close()
    payload=[]
    content={}
    for result in data:
        content={'Title':result[0],'First_Name':result[1],'MiddleName':result[2],'Last_Name':result[3],'Email':result[4],'phone':result[5],'modified Date':result[6],'Password':result[7]}
        payload.append(content)
        content={}
    
    return jsonify(payload)

@app.route('/insert', methods = ['POST'])
def obtener():
     content=request.json
     Title= content['Title']
     FirstName = content['First_Name']
     MiddleName = content['MiddleName']
     LastName content['LastName']
     email = content['EmailAddress']
     phone = content['Phone']
     ModifiedDate=dt_string
     Password=content['password']
     cur = mysql.connection.cursor()
     cur.execute("INSERT INTO adventureworks.contact (Title,FirstName,MiddleName,LastName,EmailAddress,Phone,ModifiedDate,PasswordHash) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (Title,FirstName,MiddleName,LastName,email,phone,ModifiedDate,Password))
     mysql.connection.commit()
     f={"status":"Load was succesfull"}
     return jsonify(f)
        


# starting the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
