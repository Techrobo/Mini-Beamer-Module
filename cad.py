# -*- coding: utf-8 -*-
import Part
import FreeCAD as App
from FreeCAD import Base
import FreeCADGui as Gui
import Mesh, MeshPart
import ImportGui
from PySide import QtGui
import math
import csv
import shutil
import os
import time


#Used in __init__.py to initilize doc_name as assembly
from doe_config_Beamer import __path__, doc_name  #https://stackoverflow.com/questions/2699287/what-is-path-useful-for
#from doe_config_Beamer.bom import make_BOM    #importing method make_BOM from bom.py
source_path = os.path.join(__path__[0], 'step')	#__path__ variable take default system folder (doe_config_main) and then go to step folder
source_path = os.path.normpath(source_path) #normalize the path based on operating system eg windows has \\ mac has /

#storing names of all the files stores in step folder
optics_filename = 'Minibeamer_Optik'
baseframe_filename = 'Minibeamer_Baseframe'
mount_filename = 'Mount'
clamping_Holder_filename = 'FT_Klemmbuchse5_37679_dummie___V02'
HoldingSlot_filename = 'HoldingSlot'

#name of the final bom file that will be made- argument of make_BOM method
bom_filename = 'bom.csv'


RotCenter0 = Base.Vector(0, 0, 0)	#create a vector at center axis using base object of freecad using vector function
RotAxisZ = Base.Vector(0, 0, 1)	#create a vector at center axis using base object of freecad using vector function



#Function to clear Window using Freecad methods
def clearAll():
    doc = App.ActiveDocument
    for obj in doc.Objects:
        doc.removeObject(obj.Label)

def create_doc():
    # Only create new document if one does not yet exist
    if doc_name not in App.listDocuments():
        App.newDocument(doc_name)

    App.setActiveDocument(doc_name)
    App.ActiveDocument = App.getDocument(doc_name)
    Gui.ActiveDocument = Gui.getDocument(doc_name)

#To close the documents
def close_document():
    if doc_name in App.listDocuments():
        App.closeDocument(doc_name)

#To save assembly
def save_assembly(dest):
    doc = App.getDocument(doc_name)
    Gui.export(doc.Objects, dest)

#To save individual parts
def save_parts_web(base_dir):
    doc = App.getDocument(doc_name)
    for partname in ['DOE_Holder1', 'DOE_Holder3', 'LaserHolder1', 'LensHolder', 'cap', 'Mount_Shroud']:
        obj = doc.getObject(partname)
        if obj is not None:
            m = MeshPart.meshFromShape(Shape=obj.Shape, LinearDeflection=0.1, AngularDeflection=0.2)
            file_name = os.path.join(base_dir, partname) + '.x3d'
            m.write(file_name)

#To see the final files once parts are made , bom is made and saved 
def watch_file(base_dir, csv_file, output_file):
    csv_f = os.path.join(base_dir, csv_file)
    out_f = os.path.join(base_dir, output_file)
    bom_f = os.path.join(base_dir, bom_filename)
    while True:
        if os.path.exists(csv_f):
            make_parts(csv_filename=csv_f)
            make_BOM(csv_f, bom_f)
            save_parts_web(base_dir)
            save_assembly(out_f)
            os.remove(csv_f)
        time.sleep(1)
        QtGui.QApplication.processEvents()


 # To save invudual parts after importing from existing stl and step format

def save_parts(format_,dest):
    parts_list = ['Beamer_Frame', 'Beamer_Base_Holder']

    if format_ == 0:
        print("Format STL")

        source = os.path.join(source_path, doe_halter_filename + '.STL')
        destination = "%s/DOE_Holder1_new.stl" % dest
        shutil.copy(source,destination)

        source = os.path.join(source_path, deckel_filename + '.STL')
        destination = "%s/cap_new.stl" % dest
        shutil.copy(source,destination)

        for p in parts_list:
            objs_to_save = [App.getDocument(doc_name).getObject(p)]
            save_name = '%s.%s' % (p, 'stl')
            save_path = os.path.join(dest , save_name)
            Mesh.export(objs_to_save, save_path)
            print(save_path)

    elif format_ == 1:
        print("Format STEP")

        source = os.path.join(source_path, doe_halter_filename + '.STEP')
        destination = "%s/DOE_Holder1_new.step" % dest
        shutil.copy(source,destination)

        source = os.path.join(source_path, deckel_filename + '.STEP')
        destination = "%s/cap_new.step" % dest
        shutil.copy(source,destination)

        for p in parts_list:
            objs_to_save = [App.getDocument(doc_name).getObject(p)]
            save_name = '%s.%s' % (p, 'step')
            save_path = os.path.join(dest, save_name)
            ImportGui.export(objs_to_save, save_path)
            print(save_path)

    elif format_ == 2:
        print(".FreeCAD")
        save="%s .FCStd" % dest
        #Gui.SendMsgToActiveView("SaveAs")
        App.getDocument(doc_name).saveAs(save)


def make_parts(*, csv_filename=None, params=None):						#Plot Part
    
    if csv_filename is not None: #csv_filename is not used in call in gui.py 
        with open(csv_filename,"r") as csvdatei:
            csv_reader = csv.reader(csvdatei, delimiter=';')
            zeilennummer = 0
            for row in csv_reader:
                if zeilennummer == 0:
                    print(f'Spaltennamen sind: {", ".join(row)}')
                else:
                    Width=float(row[0])
                    Height=float(row[1])
                    Depth=float(row[2])
                    Lens_x=float(row[3])
                    Lens_y=float(row[4])


                    

                zeilennummer += 1

    elif params is not None:
        Height, Width, Depth, Lens_x, Lens_y = params
    else:
        raise TypeError('Either csv_filename or params must be given')
            

    create_doc()
    
    clearAll()
    #The above code is used to obtain parameters from gui.py as params which will be used to make parts
    ###Part-Code###############################################################


    




    ###Beamer-Holder2##############################################################
    #Base

    
    # create a small sample part
    #Part.show(Part.makeBox(180,150,50).cut(Part.makeBox(180,Width,Depth).translate((10,(150-Width)/2,3)).cut(Part.makeBox(180,Width-10,3).translate((0,(150-Width)/2,0)))

    Holder_height=Height+20  #140
    Holder_width=Width+5     #125
    Holder_depth=Depth+5     #50
    BossExtrude1=Part.makeBox(Holder_height,Holder_width,Holder_depth)#dimentions of holder

    #Square Hole
    CutExtrude1=Part.makeBox(Holder_height-10,Width,Depth)
    CutExtrude2=Part.makeBox(Holder_height,Width-10,3) #to remove top of holder
    CutExtrude3=Part.makeBox(10,Width-10,Depth)#to remove the backside of the holder
    CutExtrude4=Part.makeBox(Height,(Holder_width-Width)/2,Depth-6)#to remove the side of the holder
    CutExtrude5=Part.makeBox(Height,(Holder_width-Width)/2,Depth-6)#to remove the side of the holder
    
    #Screw Hole
    CutExtrude6=Part.makeCylinder(2.1,(Holder_width-Width)/2)
    CutExtrude7=Part.makeCylinder(2.1,(Holder_width-Width)/2+5)
    CutExtrude8=Part.makeCylinder(2.1,(Holder_width-Width)/2)
    CutExtrude9=Part.makeCylinder(2.1,(Holder_width-Width)/2+5)
    #TranslationCutExtrude1=(10,(150-Width)/2,3)
    TranslationCutExtrude1=(0,(Holder_width-Width)/2,3)
    TranslationCutExtrude2=(0,(Holder_width+10-Width)/2,0)#for the top of holder cut
    TranslationCutExtrude3=(Holder_height-10,(Holder_width+10-Width)/2,3)#for the backside of holder cut
    TranslationCutExtrude4=(Holder_height-Height-10,((Holder_width-Width)/2+Width),3+3)#for the right sides of holder cut
    TranslationCutExtrude5=(Holder_height-Height-10,0,3+3)#for the left sides of holder cut
    TranslationCutExtrude6=(5,0,Depth/2+3)#for the screw hole left sides of holder cut
    TranslationCutExtrude7=(Holder_height-5,0,Depth/2+3)#for the screw hole left sides of holder cut
    TranslationCutExtrude8=(5,((Holder_width-Width)/2+Width),Depth/2+3)#for the screw hole left sides of holder cut
    TranslationCutExtrude9=(Holder_height-5,((Holder_width-Width)/2+Width-5),Depth/2+3)#for the screw hole left sides of holder cut


    #TranslationCutExtrude1=(10,30,0)
    CutExtrude1.translate(TranslationCutExtrude1)
    CutExtrude2.translate(TranslationCutExtrude2)
    CutExtrude3.translate(TranslationCutExtrude3)
    CutExtrude4.translate(TranslationCutExtrude4)
    CutExtrude5.translate(TranslationCutExtrude5)
    #CutExtrude6.translate(TranslationCutExtrude6)
    #CutExtrude6.rotate(RotCenter0, RotAxisZ, 0)
    #CutExtrude6.rotate(Base.Vector(5,0,Depth/2+3),Base.Vector(1, 0, 0), 270) 
    CutExtrude6.rotate(Base.Vector(0,0,0),Base.Vector(1, 0, 0), 270) 
    CutExtrude6.translate(TranslationCutExtrude6)
    CutExtrude7.rotate(Base.Vector(0,0,0),Base.Vector(1, 0, 0), 270) 
    CutExtrude7.translate(TranslationCutExtrude7)
    CutExtrude8.rotate(Base.Vector(0,0,0),Base.Vector(1, 0, 0), 270) 
    CutExtrude8.translate(TranslationCutExtrude8)
    CutExtrude9.rotate(Base.Vector(0,0,0),Base.Vector(1, 0, 0), 270) 
    CutExtrude9.translate(TranslationCutExtrude9)

    PartCutExtrude1=BossExtrude1.cut(CutExtrude1)
    PartCutExtrude2=PartCutExtrude1.cut(CutExtrude2) #for nested cutting
    PartCutExtrude3=PartCutExtrude2.cut(CutExtrude3)
    PartCutExtrude4=PartCutExtrude3.cut(CutExtrude4)
    PartCutExtrude5=PartCutExtrude4.cut(CutExtrude5)
    PartCutExtrude6=PartCutExtrude5.cut(CutExtrude6)
    PartCutExtrude7=PartCutExtrude6.cut(CutExtrude7)
    PartCutExtrude8=PartCutExtrude7.cut(CutExtrude8)
    PartCutExtrude9=PartCutExtrude8.cut(CutExtrude9)


   
    PartCutExtrude9.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90) #To align at x axis , angle 0
    PartCutExtrude9.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180) #To align at y axis , angle 0
    PartCutExtrude9.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 0) #To align at z axis , angle 0

    #AssemblyTranslation=(210,40.5,-138.5)
    AssemblyTranslation=(210,40.5,-68.5)
    PartCutExtrude9.translate(AssemblyTranslation)

    AssemblyTranslation=(0,Depth/2-7.5,0)
    PartCutExtrude9.translate(AssemblyTranslation)
    
    #PartCutExtrude2=BossExtrude1.cut(CutExtrude2)
    #DOEHolder3Translation=(-20,-15,-19.5)
    #PartCutExtrude1.translate(DOEHolder3Translation)

    #chamfer
    #DOE_Holder_3=App.ActiveDocument.addObject("Part::Feature", "DOE_Holder_3")
    #DOE_Holder_3.Shape=PartCutExtrude1
    #DOE_Holder_3.Shape=PartCutExtrude2
    #fuse1=PartCutExtrude2
    #fuse2=fuse1.fuse(PartCutExtrude1)
    #Part.show(fuse2)
    #Part.show(PartCutExtrude1)
    #Part.show(PartCutExtrude2)
    
    #Renaming Part
    Beamer_Frame=App.ActiveDocument.addObject("Part::Feature", "Beamer_Frame")
    Beamer_Frame.Shape=PartCutExtrude9

    Gui.ActiveDocument.Beamer_Frame.Visibility = True
    #Part.show(PartCutExtrude9)

    ###baseframe-Holder1_End############################################################

    #Make front Holdng Slot
    FrontHoldingSlot_height=40+Lens_y-4.5 #Lens_Y minimum is 4.5
    FrontHoldingSlot_width=5    #125
    FrontHoldingSlot_depth=30     #50
    FrontHoldingSlot=Part.makeBox(FrontHoldingSlot_height,FrontHoldingSlot_width,FrontHoldingSlot_depth)#dimentions of holder
    

    CutExtrude_Holder=Part.makeCylinder(2.1,FrontHoldingSlot_width)
    TranslationCutExtrude_Holder=(5,0,FrontHoldingSlot_depth/2)
    CutExtrude_Holder.rotate(Base.Vector(0,0,0),Base.Vector(1, 0, 0), 270)
    CutExtrude_Holder.translate(TranslationCutExtrude_Holder)
    PartCutExtrude_HolderL=FrontHoldingSlot.cut(CutExtrude_Holder)
    PartCutExtrude_HolderR=FrontHoldingSlot.cut(CutExtrude_Holder)
    
    
    PartCutExtrude_HolderL.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90) #To align at x axis , angle 0
    PartCutExtrude_HolderL.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 0) #To align at y axis , angle 0
    PartCutExtrude_HolderL.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -90) #To align at z axis , angle 0
    #AssemblyTranslation=(157.37-(Holder_height-4.8-2.9-4.2-15-15.5),5,22)
    #AssemblyTranslation=(190,-15,-67.7)
    AssemblyTranslation=(220,35,-67.7)
    #AssemblyTranslation=(0,0,0)
    PartCutExtrude_HolderL.translate(AssemblyTranslation)
    AssemblyTranslation=(-(Holder_height-5.8-4.2),0,0)
    PartCutExtrude_HolderL.translate(AssemblyTranslation)
    #Part.show(PartCutExtrude_HolderL)

    
    PartCutExtrude_HolderR.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90) #To align at x axis , angle 0
    PartCutExtrude_HolderR.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 0) #To align at y axis , angle 0
    PartCutExtrude_HolderR.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -90) #To align at z axis , angle 0
    #AssemblyTranslation=(157.37-(Holder_height-4.8-2.9-4.2-15-15.5),5,-(Holder_width+5+1-22))
    #AssemblyTranslation=(190,5,-(Holder_width+5+1-22))
    AssemblyTranslation=(220,35,-67.7)
    #AssemblyTranslation=(217.35,27,-67.7)
    PartCutExtrude_HolderR.translate(AssemblyTranslation)
    AssemblyTranslation=(-(Holder_height-5.8-4.2),0,-(Holder_width+5+1))
    PartCutExtrude_HolderR.translate(AssemblyTranslation)
    #Part.show(PartCutExtrude_HolderR)
    
    #STEP-Import-Rear HoldingSlot left
    Holding_SlotL = Part.Shape()
    source = os.path.join(source_path, HoldingSlot_filename + '.STEP')
    Holding_SlotL.read(source)

    Holding_SlotL.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 270) #To align at x axis , angle 0
    Holding_SlotL.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 0) #To align at y axis , angle 0
    Holding_SlotL.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 0) #To align at z axis , angle 0
    #AssemblyTranslation=(0,0,Holder_width+5+1)
    AssemblyTranslation=(0,0,0)
    Holding_SlotL.translate(AssemblyTranslation)
    AssemblyTranslation=(0,0,-(Holder_width+5+1))
    Holding_SlotL.translate(AssemblyTranslation)
    
    #Display
    #HoldL = App.ActiveDocument.addObject("Part::Feature", "HoldingSlotL")
    #HoldL.Shape=Holding_SlotL
    #HoldL.ViewObject.ShapeColor = (0.0,0.0,192/255)

    #STEP-Import-Rear HoldingSlot Right
    Holding_SlotR = Part.Shape()
    source = os.path.join(source_path, HoldingSlot_filename + '.STEP')
    Holding_SlotR.read(source)

    Holding_SlotR.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 270) #To align at x axis , angle 0
    Holding_SlotR.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 0) #To align at y axis , angle 0
    Holding_SlotR.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 0) #To align at z axis , angle 0
    AssemblyTranslation=(0,0,0)
    Holding_SlotR.translate(AssemblyTranslation)
    
    #Display
    #HoldR = App.ActiveDocument.addObject("Part::Feature", "HoldingSlotR")
    #HoldR.Shape=Holding_SlotR
    #HoldR.ViewObject.ShapeColor = (0.0,192/255,0.0)

    #Make Rear HoldingSlot Bottom
    FrontHoldingSlot_bottom_height=31.9+Lens_y-4.5 #Lens_y minimum is 4.5
    FrontHoldingSlot_bottom_width=5    #125
    FrontHoldingSlot_bottom_depth=30     #50
    FrontHoldingSlot_bottom_L=Part.makeBox(FrontHoldingSlot_bottom_height,FrontHoldingSlot_bottom_width,FrontHoldingSlot_bottom_depth)#dimentions of holder
    FrontHoldingSlot_bottom_R=Part.makeBox(FrontHoldingSlot_bottom_height,FrontHoldingSlot_bottom_width,FrontHoldingSlot_bottom_depth)#dimentions of holder
    
    
    FrontHoldingSlot_bottom_R.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90) #To align at x axis , angle 0
    FrontHoldingSlot_bottom_R.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 0) #To align at y axis , angle 0
    FrontHoldingSlot_bottom_R.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -90) #To align at z axis , angle 0
    #AssemblyTranslation=(157.37-(Holder_height-4.8-2.9-4.2-15-15.5),5,22)
    AssemblyTranslation=(217.35,27,-67.7)
    #AssemblyTranslation=(0,0,0)
    FrontHoldingSlot_bottom_R.translate(AssemblyTranslation)
    RearHoldingSlot_R=Holding_SlotR.fuse(FrontHoldingSlot_bottom_R)
    #Part.show(RearHoldingSlot_R)
    #Part.show(FrontHoldingSlot_bottom_R)

    FrontHoldingSlot_bottom_L.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90) #To align at x axis , angle 0
    FrontHoldingSlot_bottom_L.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 0) #To align at y axis , angle 0
    FrontHoldingSlot_bottom_L.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -90) #To align at z axis , angle 0
    #AssemblyTranslation=(157.37-(Holder_height-4.8-2.9-4.2-15-15.5),5,22)
    AssemblyTranslation=(217.35,27,-67.7)
    #AssemblyTranslation=(0,0,0)
    FrontHoldingSlot_bottom_L.translate(AssemblyTranslation)
    AssemblyTranslation=(0,0,-(Holder_width+5+1))
    FrontHoldingSlot_bottom_L.translate(AssemblyTranslation)
    RearHoldingSlot_L=Holding_SlotL.fuse(FrontHoldingSlot_bottom_L)
    #Part.show(RearHoldingSlot_L)
    #Part.show(FrontHoldingSlot_bottom_L)


    #Make Holder Base 
    Base_height=Holder_height+60 #140
    Base_width=Holder_width+49    #125
    Base_depth=5   #50
    HolderBase=Part.makeBox(Base_height,Base_depth,Base_width)#dimentions of holder
    HolderBase.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 0) #To align at x axis , angle 0
    HolderBase.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180) #To align at y axis , angle 0
    HolderBase.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 0) #To align at z axis , angle 0
    AssemblyTranslation=(220,-10,-41.8)
    HolderBase.translate(AssemblyTranslation)
    AssemblyTranslation=(0,-(Lens_y-4.5),0) #Lens_y minimum is 4.5
    HolderBase.translate(AssemblyTranslation)
    
    #Make Hole in Base for optic mount
    CutExtrude_Base=Part.makeCylinder(2.0,Base_depth)
    
    TranslationCutExtrude_Base=(213.55,-10,-40.08 )
    
    CutExtrude_Base.rotate(Base.Vector(0,0,0),Base.Vector(1, 0, 0), 270)
    
    CutExtrude_Base.translate(TranslationCutExtrude_Base)
    TranslationCutExtrude_Base=((-(Base_height-17),-(Lens_y-4.5),-(37+Lens_x-7.5)) )
    CutExtrude_Base.translate(TranslationCutExtrude_Base)
    #TranslationCutExtrude_Base=(0,10,0 )
    #CutExtrude_Base.translate(TranslationCutExtrude_Base)
    #Part.show(CutExtrude_Base)
    PartCutExtrude_Base=HolderBase.cut(CutExtrude_Base)
    #Part.show(HolderBase)
    #Part.show(PartCutExtrude_Base)
    
    
    
    
    ###baseframe-Holder1_End############################################################

    ###Optics lens_Start ###############################################################
    
    #STEP-Import-Optics lens
    opticspart = Part.Shape()
    source = os.path.join(source_path, optics_filename + '.STEP')
    opticspart.read(source)
    
    
    opticspart.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 0) #To align at x axis , angle 0
    opticspart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 270) #To align at y axis , angle 0
    opticspart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 0) #To align at z axis , angle 0
    AssemblyTranslation=(250,30,-77.1)
    opticspart.translate(AssemblyTranslation)
    AssemblyTranslation=(-(Base_height-17),0,-(Lens_x-7.5))  #Lens_x minimun value is 7.5
    opticspart.translate(AssemblyTranslation)
    
    #Display
    Optics = App.ActiveDocument.addObject("Part::Feature", "OpticsLens")
    Optics.Shape=opticspart
    #Optics.ViewObject.ShapeColor = (0.0,10,0.0)
    
    
    ###Optics lens_End ############################################################


    ###Optics-Mount##############################################################"""
    #Base

    
    # create a small sample part
    #Part.show(Part.makeBox(180,150,50).cut(Part.makeBox(180,Width,Depth).translate((10,(150-Width)/2,3)).cut(Part.makeBox(180,Width-10,3).translate((0,(150-Width)/2,0)))

    Optics_mount_height=10
    Optics_mount_width=10
    Optics_mount_depth=14.5+Lens_y-4.5
    Optics_mountExtrude=Part.makeBox(Optics_mount_height,Optics_mount_depth,Optics_mount_width)#dimentions of holder
    #Make Hole in optic mount
    CutExtrude_mount=Part.makeCylinder(2.0,Optics_mount_depth)
    
    #TranslationCutExtrude_mount=(215,-5,-41.8 )
    
    CutExtrude_mount.rotate(Base.Vector(0,0,0),Base.Vector(1, 0, 0), 270)
    
    #CutExtrude_mount.translate(TranslationCutExtrude_mount)
    TranslationCutExtrude_mount=(Optics_mount_height/2,0,Optics_mount_width/2) 
    CutExtrude_mount.translate(TranslationCutExtrude_mount)
    #TranslationCutExtrude_mount=(0,10,0 )
    #CutExtrude_mount.translate(TranslationCutExtrude_mount)
    #Part.show(CutExtrude_mount)
    PartCutExtrude_mount=Optics_mountExtrude.cut(CutExtrude_mount)
    #Part.show(HolderBase)
    
    AssemblyTranslation=(208.55,-5,-45.1)
    PartCutExtrude_mount.translate(AssemblyTranslation)
    AssemblyTranslation=((-(Base_height-17),-(Lens_y-4.5),-(37+Lens_x-7.5)) )
    PartCutExtrude_mount.translate(AssemblyTranslation)

    #Part.show(PartCutExtrude_mount)

    BaseHolder1=PartCutExtrude_Base.fuse(PartCutExtrude_mount)
    BaseHolder2=BaseHolder1.fuse(PartCutExtrude_HolderL)
    BaseHolder3=BaseHolder2.fuse(PartCutExtrude_HolderR)
    BaseHolder4=BaseHolder3.fuse(RearHoldingSlot_R)
    BaseHolder5=BaseHolder4.fuse(RearHoldingSlot_L)

    #Renaming Part
    Beamer_Base_Holder=App.ActiveDocument.addObject("Part::Feature", "Beamer_Base_Holder")
    Beamer_Base_Holder.Shape=BaseHolder5

    Gui.ActiveDocument.Beamer_Base_Holder.Visibility = True

    #App.ActiveDocument.recompute()
    
    #Part.show(BaseHolder5)
    

    
    #Show parts in a nice View
    App.activeDocument().recompute()
    Gui.activeDocument().activeView().viewRear()
    #Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")

params=(120,120,45,20,20)
make_parts(params=params)

########################################################################


