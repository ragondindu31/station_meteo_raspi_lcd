import os
import datetime, time
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
        self.creer_page2()
        

    #def :defilement du numero de page
    def _nextPage(self,PageNbr, nbrePageMax):
        return

    def _prevPage(self,PageNbr, nbrePageMax):
        return
    
    def _create_data_list(self):
        data_list = data_forecast()
        return data_list

    def _create_icon (self,data_list):
        
        #modification du format de fichier
        icon_path = "/home/pi/meteo/img/GIF/150x150/{}.gif".format(data_list)
        if os.path.isfile(icon_path):
             icon_today = tk.PhotoImage(file=icon_path)
        else:
            print(icon_path+" N'existe pas!")
        
        
        return icon_today

######################      élément de l'affichage  ######################
    def _labels_forecast (self,icon_morning,icon_afternoon,date,temp_morning, temp_afternoon,column):
        #infos des icones à afficher
        w_morning = icon_morning.width()
        h_morning = icon_morning.height()
        h_afternoon = icon_afternoon.height()
        w_afternoon = icon_afternoon.width()

        #icone du matin
        label_icon_M = Label(self.page2 , width = w_morning, height = h_morning, image = icon_morning)
        label_icon_M.grid(row = 3, column = column)
        label_icon_M.image = icon_morning #reference mise en memoire essentiel pour affichage en sortie de fonction

        #icon de l après midi
        label_icon_A = Label(self.page2 , width = h_afternoon, height = h_afternoon, image = icon_afternoon  )
        label_icon_A.grid(row = 4, column = column)
        label_icon_A.image = icon_afternoon 

        # date du jour de prevision 
        #conversion de la str time en timestamp
        timestamp= time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timetuple())
        #conversion du timestamp dasn le nouveau format
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%a %d/%m')

        label_date = Label(self.page2, text = date, background = 'black', fg = "WHITE", font = ('Comic Sans MS',10))
        label_date.grid(row = 2, column= column)

        #temperature du matin
        label_temp_M = Label(self.page2, text = str(temp_morning)+' °C', background = 'WHITE', fg = "black", font = ('Comic Sans MS',10))
        label_temp_M.grid(row = 3, column = column,sticky = NE)
        
        #temperature de l'apres midi
        label_temp_A = Label(self.page2, text = (str(temp_afternoon)+' °C'), background = 'WHITE', fg = "black", font = ('Comic Sans MS',10))
        label_temp_A.grid(row = 4, column = column,sticky = NE)

        #icon pour indiqué le moment de la prevision
        label_temp_AM = Label(self.page2, text = 'AM', background = 'WHITE', fg = "black", font = ('Comic Sans MS',8))
        label_temp_AM.grid(row = 3, column = column,sticky = NW)
        label_temp_PM = Label(self.page2, text = 'PM', background = 'WHITE', fg = "black", font = ('Comic Sans MS',8))
        label_temp_PM.grid(row = 4, column = column,sticky = NW)


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

        
#page2
    def creer_page2(self):

        #import de la liste de data
        data_list = self._create_data_list()
        print(data_list)
        #création de la page2
        self.page2 = tk.Frame(self ,background='black', width=700, height=500, borderwidth=2, relief=GROOVE)
        #texte du titre
        titrepage2 = Label(self.page2, text="previsions météo", background='black', fg ="WHITE", font = ('Comic Sans MS',20))
        titrepage2.grid(row = 1, columnspan = 5, sticky = N)

       
        #forecast day 1:
        icon_morning = self._create_icon(data_list[1])
        icon_afternoon = self._create_icon(data_list[4])
        self._labels_forecast(icon_morning,icon_afternoon,data_list[3],data_list[2], data_list[5],1)

        #forecast day 2:
        icon_morning = self._create_icon(data_list[7])
        icon_afternoon = self._create_icon(data_list[10])
        self._labels_forecast(icon_morning,icon_afternoon,data_list[9],data_list[8], data_list[11],2)

        #forecast day 3:
        icon_morning = self._create_icon(data_list[13])
        icon_afternoon = self._create_icon(data_list[16])
        self._labels_forecast(icon_morning,icon_afternoon,data_list[15],data_list[14], data_list[17],3)
        
        self.page2.grid(row = 2, column = 1, columnspan = 3)
        

if __name__ == '__main__':
    

    win = GUI_Meteo()
    win.master.geometry('700x500')
    win.master.title('station météo')
    
    win.mainloop()