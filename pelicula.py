class Pelicula:
    def __init__(self, id, titulo, genero, duracion, imagen):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.duracion = duracion
        self.imagen = imagen

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'genero': self.genero,
            'duracion': self.duracion,
            'imagen': self.imagen
        }

    @staticmethod
    def from_dict(data):
        return Pelicula(
            data['id'],
            data['titulo'],
            data['genero'],
            data['duracion'],
            data['imagen']
        )