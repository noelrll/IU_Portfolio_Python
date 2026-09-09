#Import der anderen Klassen
from controller import Controller
from model import Studiengang
from service import Service
from view import DashboardView
from repository import Repository

class Application:
    #Methode zum Starten des Programmes
    def main(self):
        #Controller Objekt wird erstellt und die Methode "start" ausgeführt
        repository = Repository()
        studiengang = repository.alle_daten_laden()
        
        #Falls kein Studiengang in den gespeicherten Daten gespeichert ist, wird ein Studiengang und Semester angelegt
        if studiengang is None:
            studiengang = Studiengang()
            studiengang.semester_erstellen()
        
        #Studiengang wird an weitere Klassen weitergegeben
        service = Service(studiengang)
        view = DashboardView()
        controller = Controller(studiengang,service,view,repository)

        controller.start()

#Erstellen eines "Application" Objects und Aufrufen von "main", wodurch das Programm letzendlich startet
app=Application()
app.main()