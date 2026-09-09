from model import Modul
import os

class Controller:

    #Konstrukur erhält eine Objekte aus Applikation-Klasse und weist die den eigenen Attributen zu
    def __init__(self, studiengang, service, view, repository):
        self.cyber = studiengang
        self.service = service
        self.view = view
        self.repository = repository
            
    #Methode zum Starten des Programmes bzw. zum Aufruf der Methoden zur Steuerung des Programmes
    def start(self):
        #Das aktuelle Semester wird durch die Domain Methode abgerufen und in einer Variable zugewiesen, im Laufe des Programms auch immer wieder aktualisiert
        angezeigtes_semester=self.cyber.aktuelles_semester_objekt
        
        
        #Schleife, die dauerhaft läuft, bis auf "break" getroffen wird
        while True:
            #Das Fenster wird "geleert", damit die alte Anzeige verschwindet
            os.system("cls")
            #Zeigt immer das Letzte Semester für das Dashboard an (allgemeiner Teil)
            aktuelles_semester=self.cyber.aktuelles_semester_objekt
            #Abholen der Daten von den Service Methoden zum Darstellen des Dashboards
            name, ects, durchschnitt, ziel, beginn, geplantes_ende = self.service.dashboard_daten_berechnen()
            semester_nummer, module, semester_durchschnitt, semester_ects = (self.service.semester_daten_berechnen(angezeigtes_semester))

            #Übergabe der Abgeholten Daten an die View-Klasse und Darstellung des Dashboards, Semesteranzeige und Navigation
            self.view.dashboard_start(name,ects,durchschnitt,ziel,beginn,geplantes_ende,aktuelles_semester.nummer)
            self.view.semster_anzeigen(semester_nummer,module,semester_durchschnitt, semester_ects)
            self.view.navigation_anzeigen()

            #Abfrage der Userinteraktion
            auswahl = self.view.auswahl_abfragen()

            #Je nachdem, was der User ausgewählt hat, wird eine dieser Aktionen ausgeführt
            if auswahl == "1":
                #User möchte ein bestimmtes Semester anzeigen. Daher wird die Auswahl in "angezeigtes_semester" gespeichert, sodass bei der nächsten Darstellung das gewünschte Semester angezeigt wird
                sem_auswahl = int(self.view.semester_int_abfragen()) - 1

                angezeigtes_semester = self.cyber.semester[sem_auswahl]

            elif auswahl == "2":
                #User möchte ein neues Semester erstellen. Semester wird durch die entsprechende Methode erstellt
                #und neuestes Semster wird direkt im Dashboard angezeigt
                angezeigtes_semester=self.cyber.semester_erstellen()

            elif auswahl == "3":
                #User möchte ein Modul hinzufügen. Daher werden die Nötigen Informationen durch die View-Methode abgefragt und an eine andere Methode als Parameter übergeben
                titel,ects=self.view.modul_abfragen()
                modul=Modul(titel,ects)
                #modul.pruefung_hinzufuegen(note)

                #self.cyber.aktuelles_semester_objekt.modul_hinzufuegen(modul)
                angezeigtes_semester.modul_hinzufuegen(modul)
            elif auswahl == "4":
                modul_index = self.view.modul_auswaehlen(angezeigtes_semester.module)

                modul = angezeigtes_semester.module[modul_index]
                note = self.view.pruefungsleistung_abfragen()
                modul.pruefung_hinzufuegen(note)

                #print("\033[92mModul mit Pruefungsleistung hinzugefügt!\033[0m")
            elif auswahl == "5":
                #Alle Daten werden in die Datenbank geschrieben. Anschließend wird das Programm beendet
                self.repository.alle_daten_speichern(self.cyber)
                print("Daten erfolgreich gespeichert!")
                break

            elif auswahl == "0":
                #Programm wird ohne zu Speichern beendet
                #print(self.cyber)
                break
