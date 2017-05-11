#!/usr/bin/python3

import gi
import os
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import re
import ruamel.yaml

def return_files_in_dir(path,extension):
    dirs = os.listdir( path )
    #dirs.sort() #Um die Dateien nicht zufällig wiederzugeben.
    files = []
    for temp in dirs:
        temp = path+temp
        if os.path.isfile(temp):
            switch = re.search(r"(."+extension+")",temp)
            if switch != None:
                files.append(temp)
    return files
    



class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Classifier")
        self.grid=Gtk.Grid()
        self.img = Gtk.Image()
        self.add(self.grid)
        home = os.path.expanduser('~')
        path = home
        self.button = Gtk.Button(label="Start")
        self.button.connect("clicked", self.on_start_clicked)
        self.path_dialog  = Gtk.FileChooserDialog(title="Select folder",
                        action=Gtk.FileChooserAction.SELECT_FOLDER,
                       buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
                       "Select", Gtk.ResponseType.OK),parent=None)
        response = self.path_dialog.run() 
        if response == Gtk.ResponseType.OK:
            path = self.path_dialog.get_filename()+"/"
            self.path = path
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")              
        self.path_dialog.destroy()
        self.grid.attach(self.button,1,0,1,1)
        self.grid.attach(self.img,1,0,1,20)
        self.image = None 
# Nachher eigene Funktion
        with open("config.yaml", "r") as config:
            config_map = ruamel.yaml.load(config, ruamel.yaml.RoundTripLoader)
            test_list = config_map['types']
            test_list_names = config_map['typenames']
            extension = config_map['extension']

# ----------------------
        self.filelist = return_files_in_dir(path,extension)
        self.button_list = []
        for i in range(len(test_list)):
            self.button_list.append(Gtk.Button(label=test_list_names[i]))
            self.button_list[i].connect("clicked",self.on_clicked,test_list[i])
            y=i%10
            x=2+i//10
            self.grid.attach(self.button_list[i],x,y,1,1)

    def write_classification(self,image,classification):
        with open(self.path+"classification.txt", "a") as classfile:
            classfile.write(image+";"+classification+"\n")

    def show_image(self):
        if self.image != None:
            self.img.set_from_file(self.image)
        else:
            self.grid.remove(self.img)
    
    def on_start_clicked(self,widget):
        self.grid.remove(self.button)
        self.image=self.get_next_image()
        self.img.set_from_file(self.image)
    
    def get_next_image(self):
        if(len(self.filelist)>0):
            return self.filelist.pop()
    
    def on_clicked(self,widget,*category):
        if self.image != None:
            self.write_classification(self.image,category[0])
        self.image = self.get_next_image()
        self.show_image()
        

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
