class Service:

    #Übergabe des in Controller.py erstellen Studiengangs an Service Klasse
    def __init__(self,Studiengang):
        self.studiengang=Studiengang

    #Iterarieren durch Semster und Module innerhalb der Semester, um alle Noten zu erhalten, um den Durchschnitt zu berechnen
    def gesamt_durchschnitt_berechnen(self):
        noten = []

        for semester in self.studiengang.semester:
            for modul in semester.module:
                for pruefung in modul.pruefungen:
                    noten.append(pruefung.note)
        #Falls keine noten vorhanden sind, wird nichts zurückgegeben
        if not noten:
            return None

        return sum(noten) / len(noten)
        
    #Iterieren durch Semester und Module, um alle ECTS zu summieren
    def gesamt_ects_berechnen(self):
        ges=0
        
        for semester in self.studiengang.semester:
            for modul in semester.module:
                # Prüfen, ob das Modul bestanden wurde, da nur dann die ECTS gezählt werden sollen
                if modul.pruefungen and any(pruefung.note <= 4.0 for pruefung in modul.pruefungen):
                    ges += modul.ects
        return int(ges)

    #Methode zum Berechnen aller benötigten Daten, die angezeigt werden sollen. Werden für die view Klasse zurückgegeben
    def dashboard_daten_berechnen(self):
        name = self.studiengang.name
        ects = self.gesamt_ects_berechnen()
        durchschnitt = self.gesamt_durchschnitt_berechnen()
        ziel = self.studiengang.noten_schnitt_ziel
        beginn = self.studiengang.beginn
        geplantes_ende = self.studiengang.geplantes_ende

        return name, ects, durchschnitt, ziel, beginn, geplantes_ende

    #Methode zum Berechnen aller benötigten Daten, die angezeigt werden sollen. Werden für die view Klasse zurückgegeben
    def semester_daten_berechnen(self, semester):
        module = []

        for modul in semester.module:
            if not modul.pruefungen:
                note = "Noch keine Note"
            else:
                note = ", ".join(str(pruefung.note)for pruefung in modul.pruefungen)

            module.append((modul.titel, note))

        # Durchschnitt über das Semester berechnen
        durchschnitt = semester.semester_durchschnitt_berechnen()
        ects=semester.semester_ects_berechnen()

        return semester.nummer, module, durchschnitt, ects
        