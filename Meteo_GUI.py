import tkinter as tk
from tkinter import BOTH
from tkinter import YES
from tkinter import LEFT
from tkinter import Frame ,Canvas
from tkinter import Label
from tkinter import PhotoImage
from tkinter import NW,NE, N,GROOVE, Y, W
import os
from PIL import Image, ImageTk


nbrePageMax = 3
PageNbr = 1
prevPage=0
titrepage1 =Label()
page1 = Frame()

#def :defilement du numero de page
def nextPage():
    global PageNbr, nbrePageMax
    if PageNbr <nbrePageMax :
        PageNbr = PageNbr+1
    else :
        PageNbr=1
    afficher_text_P1(win.page1)
    

def prevPage():
    global PageNbr, nbrePageMax
    if PageNbr == 1:
        PageNbr = nbrePageMax
    else :
        PageNbr=PageNbr-1
    afficher_text_P1(win.page1)
    

#afficher le texte de la page en cours :
def afficher_text_P1(frame):
    global PageNbr, prevPage, titrepage1
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

# création des éléments :
class gui_defilement(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self, master=None, width=700, height=500,background='black')
        self.pack(expand=YES)
        self.creer_nextbutton()
        self.creer_prevbutton()
        self.creer_exitbutton()
        self.creer_page1()
        
#bouton page suivante en haut à droite
    def creer_nextbutton(self):
        self.nextbutton = tk.Button(self, text="next page >", command=nextPage)
        self.nextbutton.grid(row = 1,column =3,  sticky = NE,  )

#bouton page précédente en haut à gauche
    def creer_prevbutton(self):
        self.prevbutton=tk.Button(self, text="prev page <", command=prevPage)
        self.prevbutton.grid(row = 1,column =1, sticky = NW) 

#bouton exit centrer en haut
    def creer_exitbutton(self):
        self.exitbutton=tk.Button(self, text="exit", command=self.quit)
        self.exitbutton.grid(row = 1,column =2,sticky = N) 
#page1
    def creer_page1(self):
        
        global titrepage1

        self.page1=tk.Frame(self ,background='black' ,width=700, height=500, borderwidth=2, relief=GROOVE)
        #texte du titre
        titrepage1= Label(self.page1,text="Météo du jour",font = ('Comic Sans MS',20))
        titrepage1.grid(row = 1,columnspan =3, sticky = N)

        #affichage de l'icone
        #modification du format de fichier
        icon_path = "/home/pi/meteo/img/{}.gif".format("blizzard")
        # a remplacer par un try except
        # verification si chemin existe 
        # if os.path.isfile(icon_path):
        #     print('Existe..')
        #     print(icon_path)
        # else:
        #     print('Existe pas!')
        #image = Image.open(icon_path)
        icon_today = tk.PhotoImage(file=icon_path)
        w= icon_today.width()
        h= icon_today.height()

        label_icon = Label(self.page1 , width=w, height=h, image=icon_today )
        label_icon.grid(row = 2,sticky = W )
        label_icon.image = icon_today #reference mise en memoire essentiel pour affichage en sortie de fonction

        self.page1.grid(row = 2,column = 1, columnspan = 3)
        
        


if __name__ == '__main__':
    win = gui_defilement()
    win.master.geometry('700x500')
    win.master.title('station météo')
    
    win.mainloop()