import sqlite3
import easygui
conn= sqlite3.connect('proyectos.db')
#Parte gráfica
proyecto = easygui.enterbox("Nombre del proyecto")
S= easygui.enterbox("Sondeo: ")
P= easygui.enterbox("Peso: ")
H= easygui.enterbox("Humedad: ")
G= easygui.enterbox("Grava: ")
A= easygui.enterbox("Nombre del proyecto")
F= easygui.enterbox("Nombre del proyecto")
Lu= easygui.enterbox("Nombre del proyecto")
LT= easygui.enterbox("Nombre del proyecto")
LC= easygui.enterbox("Nombre del proyecto")
LS= easygui.enterbox("Nombre del proyecto")
LN= easygui.enterbox("Nombre del proyecto")
def crear_tabla():
    conn= sqlite3.connect('proyectos.db')
    c =  conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS prueba(
            nombre_proyecto TEXT NOT NULL,
            Sondeo TEXT NOT NULL,
            Peso   TEXT NOT NULL,
            Humedad TEXT NOT NULL,
            Grava TEXT NOT NULL,
            Arena TEXT NOT NULL,
            Finos TEXT NOT NULL,
            D10 TEXT,
            D30 TEXT,
            D50 TEXT,
            D60 TEXT,
            D90 TEXT)""")
    conn.close()
    
def nuevo_trabajo():
        conn= sqlite3.connect('proyectos.db')
        c= conn.cursor()
        c.execute("INSERT INTO proyectos (nombre_proyecto) VALUES ('{0}')".format(Proyecto))
        c.execute("INSERT INTO proyectos (Sonde     o) VALUES ('{0}')".format(S))
        c.execute("INSERT INTO proyectos (Peso) VALUES ('{0}')".format(P))
        c.execute("INSERT INTO proyectos (Humedad) VALUES ('{0}')".format(H))
        c.execute("INSERT INTO proyectos (Grava) VALUES ('{0}')".format(G))
        c.execute("INSERT INTO proyectos (Arena) VALUES ('{0}')".format(A))
        c.execute("INSERT INTO proyectos (Finos) VALUES ('{0}')".format(F))
        c.execute("INSERT INTO proyectos (D10) VALUES ('{0}')".format(Lu))
        c.execute("INSERT INTO proyectos (D30) VALUES ('{0}')".format(LT))
        c.execute("INSERT INTO proyectos (D50) VALUES ('{0}')".format(LC))
        c.execute("INSERT INTO proyectos (D60) VALUES ('{0}')".format(LS))
        c.execute("INSERT INTO proyectos (D90) VALUES ('{0}')".format(LN))
        conn.close()

crear_tabla()        
nuevo_trabajo()
conn.commit()
conn.close()