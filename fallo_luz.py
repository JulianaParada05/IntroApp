from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import func
from datetime import date

# Inicializa la instancia de SQLAlchemy
db = SQLAlchemy()

# Modelo de la tabla 'fallo_luz'
class FalloLuz(db.Model):
    __tablename__ = 'fallo_luz'

    # ID autoincremental (clave primaria)
    id = db.Column(db.Integer, primary_key=True)

    # Fecha del reporte (no puede ser nula)
    fecha = db.Column(db.Date, nullable=False)

    # Dirección (puede ser nula)
    direccion = db.Column(db.String(150), nullable=True)

    # Descripción del fallo (puede ser nula)
    descripcion = db.Column(db.String(500), nullable=True)

    # Coordenadas geográficas como POINT de PostGIS (latitud, longitud)
    # Nota: SRID 4326 es el sistema de referencia para GPS (WGS84)
    localizacion = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    # Estado del fallo (por ejemplo: 0 = pendiente, 1 = en proceso, 2 = resuelto)
    estado = db.Column(db.Integer, nullable=False)

    # Nombre de quien reporta (obligatorio)
    nombre = db.Column(db.String(100), nullable=False)

    # Celular de contacto (puede ser nulo)
    celular = db.Column(db.String(10), nullable=True)

    # Representación textual del objeto para depuración
    def __repr__(self):
        return f'<FalloLuz {self.id} - {self.direccion} - {self.fecha}>'

    # Método auxiliar para devolver coordenadas como tupla (latitud, longitud)
    @property
    def coordenadas(self):
        # Usa funciones espaciales de PostGIS para extraer lat y lon
        return db.session.query(
            func.ST_Y(self.localizacion),
            func.ST_X(self.localizacion)
        ).filter(FalloLuz.id == self.id).first()
