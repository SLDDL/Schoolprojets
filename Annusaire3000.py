# Importe la librairie tkinter et ces modules
import tkinter
import csv
from tkinter import *
import ctypes
import platform	
from ttkwidgets.autocomplete import AutocompleteEntryListbox
import ttkthemes
import tkinter.ttk as ttk
import os

#Fonction qui sauvegarde l'annuaire dans le fichier annuaire.csv
def sauvegarder(annuaire, fenetre):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "annuaire.csv")
    fichier = open(file_path, "w")
    #Crée un objet ecrivain pour écrire dans le fichier
    ecrivain = csv.writer(fichier)
    #Ecrit la première ligne du fichier
    ecrivain.writerow(["Nom", "Numero"])
    #Boucle qui écrit chaque nom et numéro de l'annuaire dans le fichier
    for nom, numero in annuaire.items():
        ecrivain.writerow([nom, numero])
    fichier.close()

def make_dpi_aware():
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
make_dpi_aware()

#Fonction qui charge l'annuaire du fichier annuaire.csv
def charger():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "annuaire.csv")
    fichier = open(file_path, "r")
    #Crée un objet lecteur pour lire le fichier
    lecteur = csv.DictReader(fichier)
    #Crée un dictionnaire vide
    annuaire = {}
    #Boucle qui ajoute chaque nom et numéro de l'annuaire dans le dictionnaire annuaire
    for colonnes in lecteur:
        annuaire[colonnes['Nom']] = colonnes['Numero']
    fichier.close()
    return annuaire

def ajouter(annuaire, fenetre):
    # Créer un style thématique en utilisant le thème equilux
    style = ttkthemes.ThemedStyle(fenetre)
    style.set_theme("equilux")
    # Créer une boîte de dialogue pour demander le nom du contact à ajouter
    nom = tkinter.simpledialog.askstring("Nom", "Entrez le nom du contact : ", parent=fenetre)
    # Valider le nom
    if nom is not None:
        nom = nom.title()
    if nom == None:
        tkinter.messagebox.showerror("Erreur", "Vous n'avez pas entré de nom.", parent=fenetre)
    elif nom in annuaire:
        tkinter.messagebox.showerror("Erreur", "Le nom entré est déjà présent dans l'annuaire.", parent=fenetre)
    else:
        # Créer une boîte de dialogue pour demander le numéro de téléphone du contact à ajouter
        numero = ["",""]
        numm = tkinter.simpledialog.askstring("Numero", "Entrez le numero du contact : ", parent=fenetre)
        # Valider le numéro de téléphone
        if numm is not None:
            if numm.isdigit() and len(numm) == 10:
                numero[0] = str(numm)
            else:
                tkinter.messagebox.showerror("Erreur", "Le numéro de téléphone entré est invalide.", parent=fenetre)
                return
        if numero[0] == None:
            tkinter.messagebox.showerror("Erreur", "Vous n'avez pas entré de numero.", parent=fenetre)
        else:
            # Ajouter le contact à l'annuaire et enregistrer l'annuaire
            annuaire[nom] = '<>'.join(numero)
            sauvegarder(annuaire, fenetre)
            notesedit2(annuaire,nom)


# Éditeur de notes
def notesedit(annuaire, fenetre, nom):
    # Si le nom est vide, afficher une erreur
    if nom == "":
        tkinter.messagebox.showerror("Erreur", "Vous n'avez pas entré de nom.", parent=fenetre)
    # Si le nom n'est pas dans l'annuaire, afficher une erreur
    elif not nom in annuaire:
        tkinter.messagebox.showerror("Erreur", "Le nom entré ne correspond à aucun contact.", parent=fenetre)
    else:
        # Créer une nouvelle fenêtre pour éditer les notes
        fenetr = Toplevel()
        titre = 'Notes ' + nom
        fenetr.title(titre)
        fenetr.configure(height=300, width=300)
        fenetr.resizable(False, False)
        # Récupérer les informations de contact associées au nom
        numm = annuaire[nom]
        numeroi = numm.split("<>")
        # Afficher une étiquette avec le texte "Notes:"
        label_notes = tkinter.Label(fenetr, text="Notes:")
        label_notes.pack()
        # Afficher un widget d'édition de texte avec les notes actuelles
        textEditor = Text(fenetr, width=43, height=10)
        textEditor.insert(INSERT, numeroi[1])
        textEditor.pack()
        # Définir une fonction pour demander à l'utilisateur s'il souhaite sauvegarder avant de quitter
        def on_closing():
            if tkinter.messagebox.askokcancel("Sauvegarder", "Veux tu sauvegarder et quiter?"):
                save()
        # Définir une fonction pour sauvegarder les modifications et fermer la fenêtre
        def save():
            numeroi[1] = textEditor.get('1.0', 'end-1c')
            annuaire[nom] = '<>'.join(numeroi)
            sauvegarder(annuaire, fenetre)
            fenetr.destroy()
        # Lorsque l'utilisateur ferme la fenêtre, appeler la fonction on_closing
        fenetr.protocol("WM_DELETE_WINDOW", on_closing)
        fenetr.mainloop()

# Création de notes lors de la création de contact
def notesedit2(annuaire, nom):
    # Créer une nouvelle fenêtre pour éditer les notes
    fenetre = Toplevel()
    titre = 'Notes ' + nom
    fenetre.title(titre)
    fenetre.configure(height=300, width=300)
    fenetre.resizable(False, False)
    # Récupérer les informations de contact associées au nom
    numm = annuaire[nom]
    numeroi = numm.split("<>")
    # Afficher une étiquette avec le texte "Notes:"
    label_notes = tkinter.Label(fenetre, text="Notes:")
    label_notes.pack()
    # Afficher un widget d'édition de texte avec les notes actuelles
    textEditor = Text(fenetre, width=43, height=10)
    textEditor.insert(INSERT, numeroi[1])
    textEditor.pack()
    # Définir une fonction pour demander à l'utilisateur s'il souhaite sauvegarder avant de quitter
    def on_closing():
        if tkinter.messagebox.askokcancel("Sauvegarder", "Veux tu sauvegarder et quiter?"):
            save()
    # Définir une fonction pour sauvegarder les modifications et fermer la fenêtre
    def save():
        numeroi[1] = textEditor.get('1.0', 'end-1c')
        annuaire[nom] = '<>'.join(numeroi)
        sauvegarder(annuaire, fenetre)
        fenetre.destroy()
    # Lorsque l'utilisateur ferme la fenêtre, appeler la fonction on_closing
    fenetre.protocol("WM_DELETE_WINDOW", on_closing)
    fenetre.mainloop()


#Fonction qui supprime un contact de l'annuaire
def supprimer(annuaire, fenetre):
    #Crée une fenêtre qui demande le nom du contact à supprimer
    nom = tkinter.simpledialog.askstring("Nom", "Entrez le nom du contact : ", parent=fenetre).title()
    if nom == "":
        tkinter.messagebox.showerror("Erreur", "Vous n'avez pas entré de nom.", parent=fenetre)
    elif not nom in annuaire:
        tkinter.messagebox.showerror("Erreur", "Le nom entré ne correspond à aucun contact.", parent=fenetre)
    else:
        #Supprime le contact de l'annuaire, puis sauvegarde l'annuaire
        del annuaire[nom]
        sauvegarder(annuaire, fenetre)

#Utilisé lors de la recherche de numero
def rechercher_numero():
    # déclare la variable selected_value comme étant globale
    global selected_value
    selected_value = ''
    
    # charge l'annuaire et en crée une copie
    annuaire = charger()
    annuair = charger()
    # convertit l'annuaire en liste et enlève le premier élément
    annuaire = list(annuaire.keys())
    annuaire = annuaire[1:]
    # crée une nouvelle fenêtre
    rc = Toplevel()
    rc.title('Recherche')
    # ajoute un label à la fenêtre
    tkinter.Label(rc, text='Recherche de contact').pack()
    # ajoute un widget d'entrée à la fenêtre avec la possibilité d'autocomplétion à partir de la liste annuaire
    nomm = AutocompleteEntryListbox(rc,completevalues=annuaire)
    nomm.pack()
    nomm.focus_set()
    
    # crée le bouton "Ok"
    ok_button = Button(rc, text="Ok", command=rc.destroy)
    ok_button.pack(side=tkinter.RIGHT)
    
    def save_selection():
        # récupère la valeur sélectionnée sous forme de chaîne de caractères
        global selected_value
        selected_value = nomm.get()
        # vérifie si la valeur sélectionnée se trouve dans la liste annuaire
        if selected_value in annuaire:
            # la valeur sélectionnée est valide, on la sauvegarde et on ferme la fenêtre
            rc.destroy()
            # appelle la fonction popup avec l'annuaire et la valeur sélectionnée en arguments
            popup(annuair,selected_value)
    
    # configure le bouton "Ok" pour qu'il appelle la fonction save_selection lorsqu'on clique dessus
    ok_button.configure(command=save_selection)
    # affiche la fenêtre et attends qu'elle soit fermée
    rc.mainloop()

#Utilisé lors de la modification de notes
def rechercher_numeronotes(fenetre):
    # déclare la variable selected_value comme étant globale
    global selected_value
    selected_value = ''
    
    # charge l'annuaire et en crée une copie
    annuaire = charger()
    annuair = charger()
    # convertit l'annuaire en liste et enlève le premier élément
    annuaire = list(annuaire.keys())
    annuaire = annuaire[1:]
    # crée une nouvelle fenêtre
    rc = Toplevel()
    rc.title('Recherche')
    # ajoute un label à la fenêtre
    tkinter.Label(rc, text='Recherche de contact').pack()
    # ajoute un widget d'entrée à la fenêtre avec la possibilité d'autocomplétion à partir de la liste annuaire
    nomm = AutocompleteEntryListbox(rc,completevalues=annuaire)
    nomm.pack()
    nomm.focus_set()
    
    # crée le bouton "Ok"
    ok_button = Button(rc, text="Ok", command=rc.destroy)
    ok_button.pack(side=tkinter.RIGHT)
    
    def save_selection():
        # récupère la valeur sélectionnée sous forme de chaîne de caractères
        global selected_value
        selected_value = nomm.get()
        # vérifie si la valeur sélectionnée se trouve dans la liste annuaire
        if selected_value in annuaire:
            # la valeur sélectionnée est valide, on la sauvegarde et on ferme la fenêtre
            rc.destroy()
            # appelle la fonction notesedit
            notesedit(annuair,fenetre,selected_value)
    
    # configure le bouton "Ok" pour qu'il appelle la fonction save_selection lorsqu'on clique dessus
    ok_button.configure(command=save_selection)
    # affiche la fenêtre et attends qu'elle soit fermée
    rc.mainloop()

#Fonction qui recherche le nom d'un contact dans l'annuaire
def rechercher_nom(annuaire, fenetre):
    #Crée une fenêtre qui demande le numéro du contact dont on veut connaitre le nom
    numer = tkinter.simpledialog.askstring("Numero", "Entrez le numero du contact : ", parent=fenetre)
    numer = numer.strip()
    test = numer.isnumeric()
    test2 = len(numer)
    if numer == "":
        tkinter.messagebox.showerror("Erreur", "Vous n'avez pas entré de numero.", parent=fenetre)
        numer.destroy()
    if test == False:
        tkinter.messagebox.showerror("Erreur", "Caractère interdit.", parent=fenetre)
        numer.destroy()
    if test2 !=10:
        tkinter.messagebox.showerror("Erreur", "Nombre de chiffres incorrect.", parent=fenetre)
        numer.destroy()
    for nom in annuaire:
        if annuaire[nom].split("<>")[0] == numer:
            #Crée une fenêtre qui affiche le nom du contact
            popup(annuaire,nom)
            trouve = True
    if trouve == False:
        tkinter.messagebox.showerror("Erreur", "Le numero entré ne correspond à aucun contact.", parent=fenetre)

def popup(annuaire,nom):
    # Récupère le numéro et les notes
    numer = annuaire[nom]
    numero= numer.split("<>")
    # Crée une fenêtre pour afficher le profil
    fenetre = Toplevel()
    fenetre.title(nom)
    # Crée un label qui affiche le nom
    label_nom = tkinter.Label(fenetre, text=nom, padx=20, pady=10)
    label_nom.pack()
    # Get the current font of the label
    current_font = label_nom["font"]
    # Parse the font size from the font string
    font_size = int(current_font.split(" ")[-1])
    # Set the font size to twice the parsed size
    label_nom.configure(font=(current_font[0], font_size*2))
    # Crée un label qui affiche le numéro
    label_numero = tkinter.Label(fenetre, text=numero[0], padx=20, pady=10)
    label_numero.pack()
    # Get the current font of the label
    current_font = label_numero["font"]
    # Parse the font size from the font string
    font_size = int(current_font.split(" ")[-1])
    # Set the font size to twice the parsed size
    label_numero.configure(font=(current_font[0], font_size*2))
    # Crée un label qui affiche les notes
    label_notes = tkinter.Label(fenetre, text=numero[1], padx=20, pady=10)
    label_notes.pack()
    # Get the current font of the label
    current_font = label_notes["font"]
    # Parse the font size from the font string
    font_size = int(current_font.split(" ")[-1])
    # Set the font size to twice the parsed size
    label_notes.configure(font=(current_font[0], font_size*2))
    # Affiche la fenêtre
    fenetre.mainloop()


#Fonction qui affiche tous les contacts de l'annuaire
def afficher_annuaire():
    annuaire = charger()
    for nom, numero, notes in annuaire.items():
        print("{} : {}".format(nom, numero, notes))

def main():
    #Charge l'annuaire du fichier
    annuaire = charger()
    #Crée une fenêtre pour afficher les boutons
    fenetre = tkinter.Tk()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "Azure-ttk-theme-2.1.0\\azure.tcl")
    fenetre.tk.call("source", file_path)
    fenetre.tk.call("set_theme", "dark")
    fenetre.title("Annuaire")
    fenetre.configure(height=300, width=300)
    fenetre.tk.call('tk', 'scaling', 2)
    fenetre.resizable(False, False)
    #Crée les quatre boutons
    bouton_ajouter = tkinter.Button(fenetre, text="Ajouter un contact", command=lambda: ajouter(annuaire, fenetre), height=5, width=30)
    bouton_supprimer = tkinter.Button(fenetre, text="Supprimer un contact", command=lambda: supprimer(annuaire, fenetre), height=5, width=30)
    bouton_notes = tkinter.Button(fenetre, text="Modifier les notes d'un contact", command=lambda: rechercher_numeronotes(fenetre), height=5, width=30)
    bouton_rechercher_numero = tkinter.Button(fenetre, text="Rechercher grâce au nom", command=lambda: rechercher_numero(), height=5, width=30)
    bouton_rechercher_nom = tkinter.Button(fenetre, text="Rechercher grâce au numero", command=lambda: rechercher_nom(annuaire, fenetre), height=5, width=30)
    bouton_fermer = tkinter.Button(fenetre, text="Quitter", command=lambda: exit(), height=5, width=30)
    #Affiche les quatre boutons
    bouton_ajouter.pack()
    bouton_supprimer.pack()
    bouton_rechercher_numero.pack()
    bouton_rechercher_nom.pack()
    bouton_notes.pack()
    bouton_fermer.pack()
    fenetre.mainloop()
main()
