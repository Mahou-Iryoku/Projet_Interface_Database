from tkinter import * 
import sqlite3

#Fenêtre d'affichage
root = Tk()
root.title("Projet Interface graphique: Gestion d'une base de données des utilisateurs")   
root.geometry("650x550")

#Première connexion à la base de données
conn = sqlite3.connect('C:\\Users\\vince\\Projet_Logiciel\\database.db')
c = conn.cursor()

#Fonction qui permet de quitter l'interface graphique
def leave(): 
    conn = sqlite3.connect('C:\\Users\\vince\\Projet_Logiciel\\database.db')
    conn.commit()
    conn.close()
    root.destroy()

#Focntion qui permet de mettre à jour la base de données 
def update():
    conn = sqlite3.connect('C:\\Users\\vince\\Projet_Logiciel\\database.db')
    c = conn.cursor()
    
    data_id = delete_box.get()

    c.execute("""UPDATE utilisateurs SET 
        Name = :name, 
        Age = :age,
        Email = :email 
        WHERE oid = :oid""",
        {
            'name': name_edit.get(),
            'age': age_edit.get(),
            'email': email_edit.get(),
            'oid': data_id
        })
    
    if data_id:
        update_label = Label(root,text="Vos données ont été bien à jour")
        update_label.grid(row=6,column=0)

    conn.commit()
    conn.close()
    editor.destroy()

#Fonction qui permet d'éditer les données dans la base de données en ouvrant une nouvelle fenêtre
def edit():
    global editor
    editor = Tk()
    editor.title("Mise à jour de la Base de données")   #Ouverture une nouvelle fenêtre
    editor.geometry("530x150")

    conn = sqlite3.connect('C:\\Users\\vince\\Projet_Logiciel\\database.db')
    c = conn.cursor()

    data_id = delete_box.get()

    if not delete_box.get(): 
        update_label = Label(editor,text="Vous n'avez pas choisi votre numéro ID")
        update_label.grid(row=1,column=0)

    c.execute("SELECT * FROM utilisateurs WHERE oid= "+data_id)
    datas = c.fetchall() #Permet de contrôler le tableau des données sur la base de données

    #Creation des variables globales pour les zones de textes
    global name_edit
    global age_edit
    global email_edit

    name_edit = Entry(editor,width=30)
    name_edit.grid(row=0,column=1,padx=20,pady=(10,0))
    age_edit = Entry(editor,width=30)
    age_edit.grid(row=1,column=1)
    email_edit = Entry(editor,width=30)
    email_edit.grid(row=2,column=1)

    name_label = Label(editor,text="Prenom:")
    name_label.grid(row=0,column=0,pady=(10,0))
    age_label = Label(editor,text="Age:")
    age_label.grid(row=1,column=0) 
    email_label = Label(editor,text="Email:")
    email_label.grid(row=2,column=0)

    #Boucle pour ajouter les ajoutés une fois remplacé
    for data in datas:
        name_edit.insert(0,data[0])
        age_edit.insert(0,data[1]) 
        email_edit.insert(0,data[2]) 

    #Creation un bouton de sauvegarde de la base de données
    edit_btn = Button(editor,text="Sauvegarde de données",command=update)
    edit_btn.grid(row=6,column=0,columnspan=2,pady=10,padx=10,ipadx=145)


def delete():
    #Creation fonction de suppression des valeurs dans la table de données utilisateurs
    conn = sqlite3.connect('C:\\Users\\vince\\Projet_Logiciel\\database.db')
    c = conn.cursor()

    if delete_box.get(): 
        submit_label = Label(root,text="Vos données ont été bien supprimés")
        submit_label.grid(row=6,column=0)
    else:
        submit_label = Label(root,text="Vos données n'ont pas été supprimés")
        submit_label.grid(row=6,column=0)

    c.execute("DELETE FROM utilisateurs WHERE oid= " +delete_box.get())

    delete_box.delete(0,END)
    conn.commit()
    conn.close()


# Fonction d'ajout des valeurs dans la table de données utilisateurs 
def submit():
    
    conn = sqlite3.connect('C:\\Users\\vince\\Projet_Logiciel\\database.db')
    c = conn.cursor()

    #Insérer les valeurs dans la table de données utilisateurs
    c.execute("INSERT INTO utilisateurs VALUES(:name, :age, :email)",
    {
        'name': name.get(),
        'age': age.get(),
        'email': email.get()
    }
    )
    if name.get() and age.get() and email.get():
        submit_label = Label(root,text="Vos données ont été tout ajoutées")
        submit_label.grid(row=6,column=0)
    else:
        submit_label = Label(root,text="Vos données n'ont pas été tout ajoutées")
        submit_label.grid(row=6,column=0)

    #Chargement de données
    conn.commit()

    #Fermeture de la connexion
    conn.close()

    #Nettoyer les données dans la zone de texte une fois ajouté dans la base de données
    name.delete(0,END)
    age.delete(0,END)
    email.delete(0,END)

#Creation fonction d'affichage
def query():
    
    conn = sqlite3.connect('C:\\Users\\vince\\Projet_Logiciel\\database.db')
    c = conn.cursor()

    #Affichage de la base de données
    c.execute("SELECT *,oid FROM utilisateurs")
    datas = c.fetchall() #Permet de contrôler le tableau des données sur la base de données
    print(datas)

    #Boucle d'affichage
    print_datas = ''
    for data in datas:
        print_datas += str(data[0]) + "   " + str(data[1]) +"   "+ str(data[2]) +"   "+"\t"+str(data[3])+ "\n"

    query_Label = Label(root,text= print_datas)
    query_Label.grid(row=8,column=0, columnspan=2)

    conn.commit()
    conn.close()


#Creation des zones de textes
name = Entry(root,width=30)
name.grid(row=0,column=1,padx=20,pady=(10,0))

age = Entry(root,width=30)
age.grid(row=1,column=1)

email = Entry(root,width=30)
email.grid(row=2,column=1)

delete_box = Entry(root,width=30)
delete_box.grid(row=9,column=1)

#Creation des étiquettes attribués aux zones de textes
name_label = Label(root,text="Prenom:")
name_label.grid(row=0,column=0,pady=(10,0))

age_label = Label(root,text="Age:")
age_label.grid(row=1,column=0) 

email_label = Label(root,text="Email:")
email_label.grid(row=2,column=0) 

ID_label = Label(root,text="Selectionner l'ID:")
ID_label.grid(row=9,column=0)

#Creation Bouton d'ajout de données
submit_btn = Button(root, text="Ajouter et enregistrer les données à la base de données",command=submit)
submit_btn.grid(row=5,column=0,columnspan=2,pady=10,padx=10,ipadx=100)

#Creation Bouton d'affichage de données
query_btn = Button(root,text="Afficher les données",command=query)
query_btn.grid(row=7,column=0,columnspan=2,pady=10,padx=10,ipadx=137)

#Creation Bouton de suppresssion de données
delete_btn = Button(root,text="Suppression des données de l'ID",command=delete)
delete_btn.grid(row=10,column=0,columnspan=2,pady=10,padx=10,ipadx=136)

#Creation Bouton Mise à jour de données
edit_btn = Button(root,text="Mise à jour des données de l'ID",command=edit)
edit_btn.grid(row=12,column=0,columnspan=2,pady=10,padx=10,ipadx=142)

#Creation Bouton Quitter la page
edit_btn = Button(root,text="Quitter la fenêtre",command=leave)
edit_btn.grid(row=13,column=0,columnspan=2,pady=10,padx=10,ipadx=150)

#Chargement de données
conn.commit()

#Fermeture de la connexion
conn.close()

#Ouverture de la fenêtre principale
root.mainloop() 
