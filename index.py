from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='12345678'
app.config['MYSQL_DB']='casino'

mysql= MySQL(app)

@app.route('/')
def home():
	base= mysql.connection.cursor()
	base.execute('SELECT * FROM jugadores')
	datos=base.fetchall()
	return render_template('home.html', jugador=datos)

@app.route('/add_jugador', methods=['POST'])
def add_jugador():
	if request.method== 'POST':
		Nombre=request.form['Nombre']
		Telefono=request.form['Telefono']
		base=mysql.connection.cursor()
		base.execute("INSERT INTO jugadores (nombre,telefono,dinero) VALUES (%s,%s,%s)",
			(Nombre,Telefono,10000))
		mysql.connection.commit()
		return redirect(url_for('jugadores'))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/jugar/<string:id>')
def jugar(id):
	if id != '0':
		
		return "el ganador es el id "+ id
	else:
		return "No hay ganador"

@app.route('/jugadores')
def jugadores():
	base= mysql.connection.cursor()
	base.execute('SELECT * FROM jugadores')
	datos=base.fetchall()
	return render_template('jugadores.html', jugador=datos)

@app.route('/edit/<string:id>')
def editar(id):
	base = mysql.connection.cursor()
	base.execute('SELECT * FROM jugadores WHERE id = {0}'.format(id))
	datos=base.fetchall()
	print(datos)
	return render_template('actualizar.html', jugador=datos[0])



@app.route('/actualizar/<string:id>', methods=['POST'])
def actualizar(id):
	if request.method== 'POST':
		Nombre=request.form['Nombre']
		Telefono=request.form['Telefono']
		dinero=request.form['dinero']
		base = mysql.connection.cursor()
		base.execute("""UPDATE jugadores 
			SET nombre=%s,
				telefono=%s,
				dinero=%s
			WHERE id=%s
			""",
			(Nombre,Telefono,dinero,id))
		mysql.connection.commit()
		return redirect(url_for('jugadores'))
@app.route('/eliminar/<string:id>')
def eliminar(id):
	base = mysql.connection.cursor()
	base.execute("DELETE FROM jugadores WHERE id = {0}".format(id))
	mysql.connection.commit()
	return redirect(url_for('jugadores'))

if __name__ == '__main__':
	app.run(debug=True)