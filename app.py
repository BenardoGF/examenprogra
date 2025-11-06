from flask import Flask, render_template, request, redirect, url_for, flash
from pelicula import Pelicula
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_12345'  # Necesario para usar flash messages

# Lista para almacenar las películas (simulando una base de datos)
peliculas = [
    Pelicula(1, "The Avengers", "Acción", "2h 23min", "default.jpg"),
    Pelicula(2, "Inception", "Ciencia Ficción", "2h 28min", "default.jpg"),
    Pelicula(3, "The Dark Knight", "Acción", "2h 32min", "default.jpg")
]

# Contador para los IDs de las películas
ultimo_id = 3

@app.route('/')
def index():
    return render_template('index.html', peliculas=peliculas)

@app.route('/pelicula/nueva', methods=['GET', 'POST'])
def nueva_pelicula():
    if request.method == 'POST':
        global ultimo_id
        ultimo_id += 1
        
        # Manejo de la imagen
        imagen = request.files['imagen']
        if imagen:
            # Guardar la imagen en la carpeta static/img
            filename = f"pelicula_{ultimo_id}_{imagen.filename}"
            imagen.save(os.path.join(app.static_folder, 'img', filename))
        else:
            filename = "default.jpg"
        
        # Crear nueva película
        nueva = Pelicula(
            ultimo_id,
            request.form['titulo'],
            request.form['genero'],
            request.form['duracion'],
            filename
        )
        peliculas.append(nueva)
        flash('Película agregada exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('nueva_pelicula.html')

@app.route('/pelicula/editar/<int:id>', methods=['GET', 'POST'])
def editar_pelicula(id):
    pelicula = next((p for p in peliculas if p.id == id), None)
    if pelicula is None:
        flash('Película no encontrada!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        pelicula.titulo = request.form['titulo']
        pelicula.genero = request.form['genero']
        pelicula.duracion = request.form['duracion']
        
        # Manejo de la imagen
        imagen = request.files['imagen']
        if imagen:
            filename = f"pelicula_{id}_{imagen.filename}"
            imagen.save(os.path.join(app.static_folder, 'img', filename))
            pelicula.imagen = filename
            
        flash('Película actualizada exitosamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('editar_pelicula.html', pelicula=pelicula)

@app.route('/pelicula/eliminar/<int:id>')
def eliminar_pelicula(id):
    global peliculas
    pelicula = next((p for p in peliculas if p.id == id), None)
    if pelicula:
        # Eliminar la imagen si existe
        if pelicula.imagen != "default.jpg":
            try:
                os.remove(os.path.join(app.static_folder, 'img', pelicula.imagen))
            except:
                pass
        peliculas = [p for p in peliculas if p.id != id]
        flash('Película eliminada exitosamente!', 'success')
    else:
        flash('Película no encontrada!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Crear el directorio de imágenes si no existe
    os.makedirs(os.path.join(app.static_folder, 'img'), exist_ok=True)
    app.run(debug=True)