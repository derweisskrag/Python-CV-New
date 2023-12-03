from form import Form
from login import Login


import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg 
from PyQt5.QtCore import Qt

# Form module contains our set up, so this is entry point of GUI
# Here we simply create the entire GUI and API endpoins for Mongoose

class MainWindow(qtw.QWidget):
	def __init__(self):
		super().__init__()

		# set window title
		self.setWindowTitle("CV App - Login page")

		# set a size
		self.setFixedSize(450, 350)

		# Implement login page
		login_page = Login(qtw=qtw, qtg=qtg) # pass `qtw`
		login_form = login_page.generate_login()
	
		# set the layout (we return form_layout)
		self.setLayout(login_form)
		
		
		# show the app
		self.show()

app = qtw.QApplication([])
mw = MainWindow()

app.exec_()