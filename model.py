from dataclasses import field, dataclass
from datetime import date

#Erstellen der Klasse "Studiengang"
@dataclass
class Studiengang:
    
    #Erstellen div. Attribute
    name: str = "Cyber Security"
    noten_schnitt_ziel: float = 2.0
    beginn: date = date(2026,7,1)
    geplantes_ende: date = date(2029,7,1)
    #Erstellen einer Liste. "field(default_factory=list)" gibt an, dass für jedes Semster eine eigene Liste geben muss.
    semester: list [Semester] = field(default_factory=list)

    #Getter zum Erhalten des aktuellen Semesters als Integer
    @property
    def aktuelles_semester(self):
        #Da Indiz immer eins mehr (beginnt bei 0) als Semster, wird 1 subtrahiert
        return self.semester[-1].nummer

    #Getter zum Erhalten des aktuellen Semesters als ganzes Objekt
    @property
    def aktuelles_semester_objekt(self):
        return self.semester[-1]

    #Erstellt ein neues Semesterobjekt und fügt es der oben genannte Liste hinzu
    def semester_erstellen(self):
        sem=Semester(len(self.semester) + 1)
        self.semester.append(sem)
        return sem

#Erstellen der Klasse "Semester"
@dataclass
class Semester:
    nummer: int
    #Erstellen einer Liste. "field(default_factory=list)" gibt an, dass für jedes Semster eine eigene Liste geben muss.
    module: list[Modul] = field(default_factory=list)

    #Methode zum hinzufuegen eines Moduls in die Liste
    def modul_hinzufuegen(self, modul: Modul):
        self.module.append(modul)

    #Iterieren durch die Module eines Semesters und summieren der ECTS
    def semester_ects_berechnen(self):
        ges=0
        for modul in self.module:
            if modul.pruefungen and any(
                pruefung.note <= 4.0 for pruefung in modul.pruefungen):
                ges += modul.ects
        return int(ges)

    #Iterieren durch die Module und innerhalb der Module durch die Liste "Pruefungen" zum Berechnen des Durchschnitts
    def semester_durchschnitt_berechnen(self):
        if not self.module:
            return 0.0

        ges=0
        anzahl_module=0

        #Zählt mit, wie viele Module es im Semester gibt, falls es keine gibt, wird 0.0 zurückgegeben, um einen ZeroDivisionError zuvorzukommen
        for mod in self.module:
            if mod.pruefungen:
                ges += sum(p.note for p in mod.pruefungen) / len(mod.pruefungen)
                anzahl_module += 1

        if anzahl_module == 0:
            return 0.0
            
        return ges / anzahl_module

    #Methode zum Ausgeben der Modulnamen, sowie die entsprechende zugehörige Note
    def noten_ausgeben(self):
        for modul in self.module:
            #Falls noch keine Pruefungen vorhanden, sind wird statt die Noten einfach "Noch keine Note" ausgegeben
            if not modul.pruefungen:
                print(f"{modul.titel:<35}Noch keine Note")
            else:
                #Iterieren durch die Pruefungen und zusammenfassen aller Noten zu einem String
                noten = ", ".join(str(pruefung.note) for pruefung in modul.pruefungen)
                print(f"{modul.titel:<35}{noten}")

#Erstellen der Klasse "Modul"
@dataclass
class Modul:
    titel: str
    ects: int
    #Erstellen einer Liste. "field(default_factory=list)" gibt an, dass für jedes Semster eine eigene Liste geben muss.
    pruefungen: list[pruefungsleistung] = field(default_factory=list)

    #Fügt ein Objekt der Klasse "Pruefungsleistung" zur Liste hinzu
    def pruefung_hinzufuegen(self, note):

        pruef=pruefungsleistung(note)
        self.pruefungen.append(pruef)

#Erstellen der Klasse "Pruefungsleistung"
@dataclass
class pruefungsleistung:
    note: float

