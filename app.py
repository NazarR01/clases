import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
load_dotenv()

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

#Set up Datanase
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

nombre="Nazar"
apellido="Narvaez"

consulta = text("INSERT INTO registro (nombre, apellido) VALUES(:nombre, :apellidos)")
db.execute(consulta, {"nombre": nombre, "apellidos":apellido})
db.commit()