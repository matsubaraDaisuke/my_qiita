#!/usr/bin/env python

__version__ = "1.0"

import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk as vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

#UI配置用のクラス
class Ui_MainWindow(object):

	def setupUi(self, MainWindow):
		
		#引数で得たMainWindowに色々設定
		MainWindow.setObjectName("MainWindow")
		MainWindow.setWindowTitle("ToolBar v%s" %__version__)
		MainWindow.setEnabled(True)
		MainWindow.resize(1280,720)

		self.centralwidget = QWidget(MainWindow)

		self.toolBar = QToolBar(MainWindow) #ツールバーを用意
		self.toolBar.setObjectName("toolBar")
		MainWindow.addToolBar(self.toolBar) #ツールバーを配置

		self.actionOpenFile = QAction(MainWindow)	#「ファイルを開く」用のアクションを用意
		self.actionOpenFile.setIcon(QIcon("open_file.png")) #アイコンを設定                                  
		self.toolBar.addAction(self.actionOpenFile) #ツールバーに「ファイルを開く」アイコンを配置

		self.actionResetFile = QAction(MainWindow) #「ファイルを削除」用のアクションを用意
		self.actionResetFile.setIcon(QIcon("quit.png")) #アイコンを設定                                     
		self.toolBar.addAction(self.actionResetFile) #ツールバーに「ファイルを削除」アイコンを配置

#MainWindow用のクラス
class MyForm(QMainWindow): 
	#UIの配置や初期画面の設定はここで行う.
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.widget = QVTKRenderWindowInteractor(self)
		self.widget.Initialize()
		##背景色の設定
		self.ren = vtk.vtkRenderer()
		self.ren.GradientBackgroundOn()      #グラデーション背景を設定
		self.ren.SetBackground2(0.2,0.4,0.6) #上面の色
		self.ren.SetBackground(1,1,1)        #下面の色

		self.widget.GetRenderWindow().AddRenderer(self.ren)
		self.widget.Start()
		self.widget.show()

		self.setCentralWidget(self.widget)
		#UIのインスタンスを介してアイコンと実体(関数)をつなげる
		self.ui.actionOpenFile.triggered.connect(self.openFile)
		self.ui.actionResetFile.triggered.connect(self.resetFile)

	#アイコンの実体(関数)はここで宣言
	def resetFile(self):


		self.ren = vtk.vtkRenderer()		#空のレンダーを作成
		##背景色の設定
		self.ren.GradientBackgroundOn()      #グラデーション背景を設定
		self.ren.SetBackground2(0.2,0.4,0.6) #上面の色
		self.ren.SetBackground(1,1,1)        #下面の色
	
		self.widget.GetRenderWindow().AddRenderer(self.ren) #貼り直し
		self.widget.Render()				#これがないと，反映が遅れる
		
	def openFile(self):
	
		#ここでファイルを開くを実行．開けるファイルは「.foam」形式に限定
		fileName = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop',"OpenFOAM File (*.foam)")

		print(fileName)
		reader = vtk.vtkOpenFOAMReader()
		reader.SetFileName(str(fileName[0]))	#パス＋ファイル名が格納されるのは[0]番．「1]にはファイルの形式「OpenFOAM File (*.foam)」が格納される．

		reader.CreateCellToPointOn()
		reader.DecomposePolyhedraOn()
		reader.EnableAllCellArrays()
		reader.Update()

		filter2 = vtk.vtkGeometryFilter()
		filter2.SetInputConnection(reader.GetOutputPort())

		mapper = vtk.vtkCompositePolyDataMapper2()
		mapper.SetInputConnection(filter2.GetOutputPort())
		actor = vtk.vtkActor()
		actor.SetMapper(mapper)
		ren = vtk.vtkRenderer()
		##背景色の設定
		ren.GradientBackgroundOn()      #グラデーション背景を設定
		ren.SetBackground2(0.2,0.4,0.6) #上面の色
		ren.SetBackground(1,1,1)        #下面の色
		self.widget.GetRenderWindow().AddRenderer(ren)
		ren.AddActor(actor)

if __name__ == '__main__':

	import sys

	app = QApplication(sys.argv)
	form = MyForm()
	form.show() 
	sys.exit(app.exec_())

