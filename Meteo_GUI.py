import os
import datetime
import tkinter as tk
from tkinter import BOTH, LEFT, RIGHT,YES
from tkinter import Frame, Canvas, Label, PhotoImage
from tkinter import NW,NE, N,GROOVE, Y, W

from PIL import Image, ImageTk

from meteo_today_forecast import data_forecast, today_data

####declaration de constante :
TIME_REFRESH_PAGE1 = 9000

# création des éléments :
class GUI_Meteo(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self, master=None, width=700, height=500,background='black')
        self.pack(expand=YES)
        self.creer_nextbutton()
        self.creer_prevbutton()
        self.creer_exitbutton()
        self.creer_page1()
        

    #def :defilement du numero de page
    def _nextPage(self,PageNbr, nbrePageMax):
        return
        # if PageNbr <nbrePageMax :
        #     PageNbr = PageNbr+1
        # else :
        #     PageNbr=1
        # #afficher_text_P1(win.page1)
    

    def _prevPage(self,PageNbr, nbrePageMax):
        return
        # if PageNbr == 1:
        #     PageNbr = nbrePageMax
        # else :
        #     PageNbr=PageNbr-1
        # #afficher_text_P1(win.page1)

    #afficher le texte de la page en cours :
    def _afficher_text_P1(frame,PageNbr, prevPage, titrepage1):
        
        titrepage1.destroy()
        if PageNbr != prevPage :
            texte_page = "page "+ str(PageNbr)+"""
            blabla
            blibli
            """
            prevPage = PageNbr
        #affichage du texte de page1
        titrepage1 = Label(frame, text=texte_page,font = ('Comic Sans MS',30))
        titrepage1.grid(padx=30, pady=30)

    #mise a jour de l'heure :
    def _maj_heure(self):
        myDatetime = datetime.datetime.now()
        heure = myDatetime.strftime('%H:%M:%S')
        return heure
        
    def _refresh_heure(self):
        new_heure = self._maj_heure()
        self.label_heure.configure(text = new_heure)
        self.label_heure.after(1000, self._refresh_heure)
    
    #creation données du jour à afficher
    def _create_data_today_text(self):

        #import depuis la base sql
        update_data_today = today_data()
        #mise a jour des variables
        #icon=update_data_today.get("today_icon")
        myDatetime = datetime.datetime.now()
        myString = myDatetime.strftime('%H:%M:%S')
        data_text =f"""
        {datetime.date.today()}

        temperature : {update_data_today.get("temperature")} °C

        pression atmos. : {update_data_today.get("pressure")} hPa

        humidité de l'air : {update_data_today.get("humidity")} %

        vitesse du vent : {update_data_today.get("wind")} m/s"""
        return data_text

    #mise a jour des données du jour :
    def _update_data_today(self):
        data_text = self._create_data_today_text()
        self.label_data_text.configure(text = data_text)
        self.label_data_text.after(2000, self._update_data_today)

    def _create_icon_today(self):
        
        update_data_today = today_data()

        #modification du format de fichier
        icon_path = "/home/pi/meteo/img/GIF/250x250/{}.gif".format(update_data_today.get("today_icon"))

        if os.path.isfile(icon_path):
             icon_today = tk.PhotoImage(file=icon_path)
        else:
            print(icon_path+" N'existe pas!")
        
        return icon_today

    #mise a jour de l'icone du jour   
    def _refresh_icon_today(self):
        update_icon_today = self._create_icon_today()
        self.label_icon.configure(image = update_icon_today)
        self.label_icon.image = update_icon_today
        self.label_icon.after(TIME_REFRESH_PAGE1, self._refresh_icon_today)

######################      élément de l'affichage  ######################

#bouton page suivante en haut à droite
    def creer_nextbutton(self):
        self.nextbutton = tk.Button(self, text="next page >", command=self._nextPage)
        self.nextbutton.grid(row = 1, column = 3,  sticky = NE)

#bouton page précédente en haut à gauche
    def creer_prevbutton(self):
        self.prevbutton=tk.Button(self, text="prev page <", command=self._prevPage)
        self.prevbutton.grid(row = 1, column = 1, sticky = NW) 

#bouton exit centrer en haut
    def creer_exitbutton(self):
        self.exitbutton=tk.Button(self, text="exit", command=self.quit)
        self.exitbutton.grid(row = 1, column = 2, sticky = N) 

#page1
    def creer_page1(self):

        self.page1=tk.Frame(self ,background='black', width=700, height=500, borderwidth=2, relief=GROOVE)
        #texte du titre
        titrepage1= Label(self.page1, text="Météo du jour", background='black', fg ="WHITE", font = ('Comic Sans MS',20))
        titrepage1.grid(row = 1, columnspan = 3, sticky = N)

        #affichage de l'icone
        
        icon_today = self._create_icon_today()
        w= icon_today.width()
        h= icon_today.height()

        self.label_icon = Label(self.page1 , width = w, height = h, image=icon_today )
        self.label_icon.grid(rowspan = 2,sticky = W )
        self.label_icon.image = icon_today #reference mise en memoire essentiel pour affichage en sortie de fonction
        self.label_icon.after(TIME_REFRESH_PAGE1, self._refresh_icon_today)

        #affichage de l'heure :
        heure = self._maj_heure()
        self.label_heure = Label(self.page1, text=heure, background='black', fg ="WHITE", font = ('Comic Sans MS', 22))
        self.label_heure.grid(row = 2, column=2)
        self.label_heure.after(1000, self._refresh_heure)

        #affichage texte des données du jour :
        data_text = self._create_data_today_text()

        self.label_data_text = Label(self.page1, text = data_text, background = 'black', fg = "WHITE", font = ('Comic Sans MS',14))
        self.label_data_text.grid(row = 3, column=2)
        self.label_data_text.after(TIME_REFRESH_PAGE1, self._update_data_today)

        #init de la page 1
        self.page1.grid(row = 2, column = 1, columnspan = 3)
        

        


if __name__ == '__main__':
    

    win = GUI_Meteo()
    win.master.geometry('700x500')
    win.master.title('station météo')
    
    win.mainloop()