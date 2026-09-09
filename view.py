from datetime import date

class DashboardView:
    #Methode zum Berechnen und Darstellen des Fortschrittsbalken auf Grundlage der ECTS
    def fortschrittsbalken_ects(self,wert_aktuell,wert_ende):
        #Breite des Balkens wird angegeben. Berechnung des Fortschritts in Prozent.
        breite=30
        prozent=wert_aktuell/wert_ende
        #Berechnung, wie viele Balken zum anzeigen des Fortschritts benötigt werden
        balken_anzahl=int(prozent*breite)
 
        #Erstellen des Strings mit richten Anzahl an Balken (vorher in balken_anzahl berechnet)
        fortschritt="█" * balken_anzahl
        #Erstellen des Strings mit den Balken, die den "nicht vollständigen" Fortschritt darstellen
        fortschritt_leer="░" * (breite - balken_anzahl)
 
        #Zusammensetzung des Strings und Ausgabe
        return f"[{fortschritt}{fortschritt_leer}] {prozent * 100:.1f}%"
   

#Methode zum Berechnen und Darstellen des Fortschrittsbalken auf Grundlage des Zeitraums
    def fortschrittsbalken_datetime(self, beginn, geplantes_ende):

        jetzt = date.today()

        gesamt = geplantes_ende - beginn
        vergangen = jetzt - beginn

        prozent = vergangen / gesamt

        breite = 30
        balken_anzahl = int(prozent * breite)

        fortschritt = "█" * balken_anzahl
        fortschritt_leer = "░" * (breite - balken_anzahl)

        return f"[{fortschritt}{fortschritt_leer}] {prozent * 100:.1f}%"

    #Methode zum Darstellen des "Allgemeinen" Teils des Dashboards
    def dashboard_start(self, name, ects, durchschnitt, ziel, beginn, geplantes_ende,aktuelles_semester):
        print("====================================================")
        print("\t\t STUDIUMS-DASHBOARD")
        print("====================================================")
        print("\n Allgemeines")
        print("----------------------------------------------------")
        print("Studiengang:\t\t\t" + name)
        #Darstellen der Fortschrittsbalken durch Aufruf der Methoden der eigenen Klasse
        print("Fortschritt ECTS:\t\t" +self.fortschrittsbalken_ects(ects, 180))
        print("Fortschritt Zeitraum:\t\t" +self.fortschrittsbalken_datetime(beginn, geplantes_ende))
        print("Aktuelles Semester:\t\t"+ str(aktuelles_semester))

        #Prüfung ob bereits ein Durchschnitt berechnet werden kann
        if durchschnitt is None:
            durchschnitt_anzeige = "Noch keine Noten"
        #Falls größer/gleich Ziel (2.0), dann in Rot
        elif durchschnitt <= ziel:
            durchschnitt_anzeige = f"\033[92m{durchschnitt:.1f}\033[0m"
        #anderenfalls in grüner Schriftfarbe
        else:
            durchschnitt_anzeige = f"\033[91m{durchschnitt:.1f}\033[0m"

        print("Durchschnittsnote:\t\t" + durchschnitt_anzeige)
        print("ECTS:\t\t\t\t" + str(ects) + " von 180")

    #Methode zum Darstellen des "Semester" Teils des Dashboards
    def semster_anzeigen(self,semester_nummer,module,durchschnitt,ects):

        print("\n\nModule des "+ str(semester_nummer)+ ". Semesters")
        print("---------------------------------------------------")
        print("Modulname:\t\t\tNote")
        #Ausgabe jedes Moduls mit Namen und Noten in tabellarischer Form
        for titel, note in module:
            print(f"{titel:<35}{note}")
        print(f"\n{'Durchschnittsnote:':<35}{durchschnitt:.1f}")
        print(f"{'ECTS:':<35}{ects:.1f}")
        print("\n\n====================================================")

    #Methode zum Darstellen des "Navigation" Teils des Dashboards
    def navigation_anzeigen(self):
        print("\t\t NAVIGATION")
        print("====================================================")
        print("[1] Semster anzeigen")
        print("[2] Semster hinzufügen")
        print("[3] Modul hinzufügen")
        print("[4] Prüfungsleistung hinzufügen")
        print("[5] Speichern")
        print("[0] Beenden")
    
    #Methode zur Abfrage dr Auswahl des Nutzers
    def auswahl_abfragen(self):
        return input("Ihre Wahl: ")

    #Methode zur Abfrage aller nötigen Informationen zum hinzufuegen eines Moduls
    def modul_abfragen(self):
        titel=input("Modulname: ")
        ects=int(input("Anzahl ECTS: "))
        #note = float(input("Note: "))

        return titel,ects#,note
    #Methode zun Auswählen des Moduls zu welchem die Prüfungsleistung hinzugefügt werden soll
    def modul_auswaehlen(self, module):
        print("\nModule:")
        #Alle möglichen Module des Semesters werden mit einer Zahl (zur Navigation) dargestellt
        for i, modul in enumerate(module, start=1):
            print(f"[{i}] {modul.titel}")
        #Die Auswahl wird gespeichert
        auswahl = int(input("Welches Modul? ")) - 1

        return auswahl


    #Methode zur Abfrage, welches Semester im "Semester" Teil des Dashboards angezeigt werden soll
    def semester_int_abfragen(self):
        #Eingabe dafür, welches Semester angezeigt werden soll
        semester_auswahl = input("Welches Semster anzeigen?")
        return semester_auswahl

    #Nötige Informationen zur Prüfungsleistung werde abgefragt
    def pruefungsleistung_abfragen(self): 
        note = float(input("Note der Prüfungsleistung: "))
        return note

    
    