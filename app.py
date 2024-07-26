from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para flash messages

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="OpticalUserAdmin",
        password="Kolyutyt1234",
        database="Optical"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/administracion', methods=['GET', 'POST'])
def administracion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            db = connect_to_database()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM USERS WHERE User_Name = %s AND Password = %s", (username, password))
            user = cursor.fetchone()
            
            if user:
                session['username'] = username
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
        except mysql.connector.Error as err:
            flash('Error al conectar a la base de datos: {}'.format(err), 'error')
        finally:
            if 'db' in locals():
                db.close()
    
    return render_template('administracion.html')

@app.route('/admin_dashboard')

def admin_dashboard():
    return render_template('admin-dashboard.html')

@app.route('/catalogo')
def catalogo():
    try:
        db = connect_to_database()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM MARCAS")
        marcas = cursor.fetchall()
        return render_template('catalogo.html', marcas=marcas)
    except mysql.connector.Error as err:
        return "Error al conectar a la base de datos: {}".format(err)
    finally:
        if 'db' in locals():
            db.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
