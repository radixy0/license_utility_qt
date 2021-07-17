from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QRadioButton, QPushButton, QMessageBox, QFileDialog
from PyQt5 import uic
import sys
import winreg
import webbrowser

REGKEY  = r"Software\Siemens_PLM_Software\Common_Licensing"
REGVALUE = r"SE_SERVER"
registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
opened_key = winreg.OpenKey(registry, REGKEY, 0, winreg.KEY_ALL_ACCESS)
 
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi(r".\files\ui.ui", self)

        #find elements from xml
        self.lineEdit_reg_value = self.findChild(QLineEdit, "lineEdit_reg_value")
        self.lineEdit_licensefile = self.findChild(QLineEdit, "lineEdit_licensefile")
        self.lineEdit_licensename = self.findChild(QLineEdit, "lineEdit_licensename")

        self.RadioButton_delete = self.findChild(QRadioButton, "radioButton_delete") 
        self.RadioButton_licensefile = self.findChild(QRadioButton, "radioButton_licensefile") 
        self.RadioButton_licensename = self.findChild(QRadioButton, "radioButton_licensename") 

        self.button_OK = self.findChild(QPushButton, "pushButton_OK")
        self.button_Help = self.findChild(QPushButton, "pushButton_Help")
        self.button_Exit = self.findChild(QPushButton, "pushButton_Exit")
        self.button_Browse = self.findChild(QPushButton, "button_browse")
        
        #connect elements
        self.button_Help.clicked.connect(self.handleHelpButton)
        self.button_Exit.clicked.connect(self.handleExitButton)
        self.button_OK.clicked.connect(self.handleOKButton)
        self.button_Browse.clicked.connect(self.handleBrowseButton)

        #preload textfield
        self.updateTextfield()

        self.show()

    def handleBrowseButton(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("License files (*.lic, *.txt, *.dat);;All files (*.*)")
        dialog.setWindowTitle("Open File")
        if(dialog.exec_()):
            filename = dialog.selectedFiles()[0]
            self.lineEdit_licensefile.setText(filename)
        

    def handleOKButton(self):
        if(self.RadioButton_delete.isChecked()):
            deleteVar()
        elif(self.RadioButton_licensefile.isChecked()):
            setVar(self.lineEdit_licensefile.text())
        elif(self.RadioButton_licensename.isChecked()):
            setVar(self.lineEdit_licensename.text())
        
        self.updateTextfield()


    def handleExitButton(self):
        self.close()


    def handleHelpButton(self):
        txt = "help"
        try:
            with open("files/help.txt") as f:
                txt = f.read()
        except:
            None

        msgBox = QMessageBox()
        msgBox.setWindowTitle("Help")
        msgBox.setText(txt)
        msgBox.exec()

    def updateTextfield(self):
        self.lineEdit_reg_value.setText(getVar())


def setVar(newVar):
    winreg.SetValueEx(opened_key, REGVALUE, 0, winreg.REG_SZ, newVar)

def getVar():
    try:
        result, _ = (winreg.QueryValueEx(opened_key, REGVALUE))
        return result
    except:
        return "No Value"
    

def deleteVar():
    try:
        winreg.DeleteValue(opened_key, REGVALUE)
    except:
        None
 

app = QApplication(sys.argv)
window = UI()
app.exec_()