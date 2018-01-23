#!/usr/bin/env python

# -*- coding: utf-8 -*-
import os
import vtk as vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

rootDir = "pitzDaily"
fileName = rootDir + "/system/controlDict"

# reader
reader = vtk.vtkOpenFOAMReader()
reader.SetFileName(fileName)
reader.CreateCellToPointOn()
reader.DecomposePolyhedraOn()
reader.EnableAllCellArrays()
reader.Update()

tArray =vtk_to_numpy(reader.GetTimeValues())    #出力ファイルの時間を格納
print(tArray)                                   #output-> [   0.  100.  200.  300.  400.  406.]
reader.UpdateTimeStep(tArray[-1])               #最新の時間406を出力設定
reader.Update()

filter = vtk.vtkGeometryFilter()
filter.SetInputConnection(reader.GetOutputPort()) #filterにreaderを設定


# mapper
mapper = vtk.vtkCompositePolyDataMapper2()
mapper.SetInputConnection(filter.GetOutputPort()) #mapperにfilterを設定
##スカラー値の設定
mapper.SetScalarModeToUseCellFieldData() #scalarデータ用に設定
mapper.SelectColorArray("p")             #圧力を表示する
mapper.SetScalarRange(-10,50)            #圧力を[-10,50]の範囲で表示

# actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)             #actorにmapperを設定

# renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)            #rendererにactorを設定

##背景色の設定
renderer.GradientBackgroundOn()      #グラデーション背景を設定
renderer.SetBackground2(0.2,0.4,0.6) #上面の色
renderer.SetBackground(1,1,1)        #下面の色

#Window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)         #Windowにrendererを設定

iren = vtk.vtkRenderWindowInteractor();
iren.SetRenderWindow(renWin);

renWin.SetSize(850, 850)
renWin.Render()
iren.Start();


