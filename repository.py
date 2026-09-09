import sqlite3
from datetime import date
from model import Studiengang, Semester, Modul, pruefungsleistung

class Repository:

    #Konstruktor zum Zuweisen des Datenbannkpfads zum Attribut
    def __init__(self, db="data.db"):
        self.datenbank = db

    #Methode zum Speichern aller Daten
    def alle_daten_speichern(self, studiengang):
        #Aufbau der Verbindung und Erstellen eines "Cursors"
        conn = sqlite3.connect(self.datenbank)
        cursor = conn.cursor()

        #Leeren der Tabellen, bevor neue Daten gespeichert werden
        cursor.execute("DELETE FROM pruefungsleistung")
        cursor.execute("DELETE FROM modul")
        cursor.execute("DELETE FROM semester")
        cursor.execute("DELETE FROM studiengang")

    # Alle Attribute des Studiengangs werden in die Tabelle "Studiengang" eingefügt
        cursor.execute(f"""
            INSERT INTO studiengang
            (name, noten_schnitt_ziel, beginn, geplantes_ende)
            VALUES ('{studiengang.name}',{studiengang.noten_schnitt_ziel},'{studiengang.beginn}','{studiengang.geplantes_ende}')
            """)

        #Speichert die ID des eingefügten Studiengangs, damit man anschließend die Semester diesem Studiengang zuordnen kann
        studiengang_id = cursor.lastrowid

    # Speichert die Semesternummer in Bezug zur Studiengang ID
        for semester in studiengang.semester:

            cursor.execute(f"""
                INSERT INTO semester
                (studiengang_id, nummer)
                VALUES ({studiengang_id},{semester.nummer})
            """)
            #Speichert die ID des gerade eingefügten Semesters
            semester_id = cursor.lastrowid

        # Speichert Module und bezieht sich dabei auf das gerade eingefügte Semester, um die Zuordnung nicht zu verlieren
            for modul in semester.module:

                cursor.execute(f"""
                    INSERT INTO modul
                    (semester_id, titel, ects)
                    VALUES ({semester_id},'{modul.titel}',{modul.ects})
                """)
                #Speichert die ID des gerade gespeicherten Moduls
                modul_id = cursor.lastrowid

            #  Speichert Pruefungen und bezieht sich dabei auf das gerade eingefügte Modul, um die Zuordnung nicht zu verlieren
                for pruefung in modul.pruefungen:

                    cursor.execute(f"""
                        INSERT INTO pruefungsleistung
                        (modul_id, note)
                        VALUES ({modul_id},{pruefung.note})
                    """)
        #Anwenden der Änderungen
        conn.commit()
        #Schließen der Sitzung
        conn.close()


    #Methode zum Laden aller in der DB gespeicherten Daten
    def alle_daten_laden(self):
        #Aufbau der Verbindung und Erstellen eines "Cursors"
        conn = sqlite3.connect(self.datenbank)
        cursor = conn.cursor()

    # Studiengang laden LIMIT 1 gibt an, dass nur der erste geladen wird (daher wird beim Speichern die Tabelle geleert)
        cursor.execute("""
            SELECT id, name, noten_schnitt_ziel, beginn, geplantes_ende
            FROM studiengang
            LIMIT 1
        """)
        #Speichern der Daten in Variable
        studiengang_daten = cursor.fetchone()

        #Prüfen ob keine Daten gespeichert sind, falls dem so ist, Verbindung schließen
        if studiengang_daten is None:
            conn.close()
            return None

        #Speichern der einzelnen Werten in den jeweiligen Variablen
        studiengang_id, name, noten_schnitt_ziel, beginn, geplantes_ende = studiengang_daten

    # Objekt Studiengang wird aus den obigen erstellten Variablen erstellt
        studiengang = Studiengang(name=name,noten_schnitt_ziel=noten_schnitt_ziel,beginn=date.fromisoformat(beginn),geplantes_ende=date.fromisoformat(geplantes_ende))

    # Alle Semester laden, die die obige StudienID haben
        cursor.execute("""
            SELECT id, nummer
            FROM semester
            WHERE studiengang_id = ?
        """, (studiengang_id,))
        #Output in Variable ablegen
        semester_daten = cursor.fetchall()

        #Aus den Daten werden Semesterobjekte generiert und in die Semester Liste des Studiengangs eingefügt
        for semester_id, nummer in semester_daten:

            semester = Semester(nummer)
            studiengang.semester.append(semester)

        # Alle Module des gerade zu iterierenden Semesters erhalten
            cursor.execute("""
                SELECT id, titel, ects
                FROM modul
                WHERE semester_id = ?
            """, (semester_id,))

            #Output zu Variable zuweisen
            modul_daten = cursor.fetchall()

            #Aus jedem Modul ein Modulobjekt erstellen und es der Liste hinzufügen
            for modul_id, titel, ects in modul_daten:

                modul = Modul(titel, ects)
                semester.module.append(modul)

            # Prüfungsleistungen des gerade zu iterierenden Moduls laden
                cursor.execute("""
                    SELECT note
                    FROM pruefungsleistung
                    WHERE modul_id = ?
                """, (modul_id,))

                #Output in Variable speichern
                pruefungen = cursor.fetchall()

                #Jede Prüfungsleistung dem gerade iterierenden Modul hinzufügen
                for (note,) in pruefungen:
                    pruefung = pruefungsleistung(note)
                    modul.pruefungen.append(pruefung)

        conn.close()

        #Rückhgabe des fertig geladenen und erstellten Objektes
        return studiengang

    #Gehört nicht direkt zum Projekt. Methode zum leeren der Datenbank
    def leere_datenbank(self):
        conn = sqlite3.connect(self.datenbank)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM pruefungsleistung")
        cursor.execute("DELETE FROM modul")
        cursor.execute("DELETE FROM semester")
        cursor.execute("DELETE FROM studiengang")

        conn.commit()
        conn.close()

    #Gehört nicht direkt zum Projekt. Methode wurde zum Überprüfen des Inhalts genutzt
    def querry_ausführen(self):
        conn=sqlite3.connect(self.datenbank)
        cursor=conn.cursor()

        cursor.execute("""
            SELECT * from modul
        """)

        res=cursor.fetchall()
        conn.commit()
        conn.close()
        return res


#repo=Repository()
#repo.leere_datenbank()