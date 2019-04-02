from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# mysql connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='fastcontacts'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

# Routes the App
@app.route('/')
def Index():
        cur = mysql.connection.cursor()
        cur.execute('select * from contacts')
        data = cur.fetchall()
        return render_template('index.html',contacts = data)

@app.route('/add_contact',methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname=request.form['fullname']
        phone=request.form['phone']
        email= request.form['email']
        cur=mysql.connection.cursor()
        cur.execute('insert into contacts (fullname,phone,email) values (%s,%s,%s)',
        (fullname,phone,email))
        mysql.connection.commit()
        flash('Contacto Agregado Satisfactoriamente')
        return redirect(url_for('Index'))       

@app.route('/edit/<id>')
def get_contact(id):
        cur= mysql.connection.cursor()
        cur.execute('select * from contacts where id= %s',(id))
        data = cur.fetchall()
        return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods =['POST'])
def update_contact(id):
        if request.method == 'POST':
                fullname= request.form['fullname']
                email= request.form['email']
                phone= request.form['phone']
                cur= mysql.connection.cursor()
                cur.execute('update contacts set fullname= %s, email= %s, phone= %s  where id= %s',(fullname,phone,email,id))
                mysql.connection.commit()
                flash('Contacto actualidado satisfactoriamente')
                return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
        cur = mysql.connection.cursor()
        cur.execute('delete from contacts where id={0}'.format(id))
        mysql.connection.commit()
        flash('Contacto Eliminado Satisfactoriamente')
        return redirect(url_for('Index')) 

if __name__ == '__main__':
    app.run( port=3000, debug= True)
