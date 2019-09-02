import StringParser as sp
import CircuitSolver as cs 
import sympy as sy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import sys

# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("UserInterface.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.circuitSolver = cs.circuitSolver()
        self.stringParser = sp.stringParser()

        self.setEqButton.clicked.connect(self.setEquations)
        self.clearAllButton.clicked.connect(self.clearAll)
        self.setUnknownsButton.clicked.connect(self.setUnknowns)
        self.goButton.clicked.connect(self.resolve)
        self.eqCreatorsList = [self.eqCreator_1,self.eqCreator_2,self.eqCreator_3,self.eqCreator_4,self.eqCreator_5,self.eqCreator_6]

    def setEquations(self):
        self.stringParser.eraseEq()
        for i in range(0,5):
            temp = self.eqCreatorsList[i].text()
            if(temp != ""):
                self.stringParser.decode(temp)
        if len(self.stringParser.getExpressionList()) == 0:
            self.lblStatus.setText("ERROR")
        else:
            self.lblStatus.setText("OK")
        return
    
    def clearAll(self):
        self.stringParser.reset()
        self.circuitSolver.reset()
        self.lblStatus.setText("ERROR")
        return

    def setUnknowns(self):
        self.stringParser.eraseUnk()
        temp = self.unkCreator.text()
        if(temp != ""):
            self.stringParser.setUnknowns(temp)
        else:
            self.lblStatus.setText("ERROR")
        return

    def resolve(self):
        if self.lblStatus.text() == "OK":
            self.circuitSolver.reset()
            self.circuitSolver.setEquations(self.stringParser.getExpressionList())
            self.circuitSolver.setUnknowns(self.stringParser.getUnknowns())
            self.circuitSolver.solveCircuit()
            if self.transferenceChkBox.checkState():
                if self.prettyViewButton.isChecked():
                    self.showTransferFunction(False)
                else:
                    self.showTransferFunction(True)
            if self.zInpChkBox.checkState():
                if self.prettyViewButton.isChecked():
                    self.showZInputFunction(False)
                else:
                    self.showZInputFunction(True)
            if self.zOutChkBox.checkState():
                if self.prettyViewButton.isChecked():
                    self.showZOutputFunction(False)
                else:
                    self.showZOutputFunction(True)
            if self.modPhaseChkBox.checkState():
                if self.prettyViewButton.isChecked():
                    self.showModPhaseFunction(False,True)
                else:
                    self.showModPhaseFunction(True,True)
            else:
                if self.prettyViewButton.isChecked():
                    self.showModPhaseFunction(False,False)
                else:
                    self.showModPhaseFunction(True,False)
            
        return

    def showTransferFunction(self, isLatex):
        temp = self.circuitSolver.getH()
        if isLatex:
            temp = sy.latex(temp)
        else:
            temp = sy.pretty(temp)
            temp = temp.replace('\n','<br/>')
        _translate = QtCore.QCoreApplication.translate
        self.transferenceResultTextEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"+ temp +"</p></body></html>"))
        return

    def showZInputFunction(self, isLatex):
        temp = self.circuitSolver.getZinp()
        if isLatex:
            temp = sy.latex(temp)
        else:
            temp = sy.pretty(temp)
            temp = temp.replace('\n','<br/>')
        _translate = QtCore.QCoreApplication.translate
        self.zInpResultTextEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"+temp+"</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        return

    def showZOutputFunction(self, isLatex):
        temp = self.circuitSolver.getZout()
        if isLatex:
            temp = sy.latex(temp)
        else:
            temp = sy.pretty(temp)
            temp = temp.replace('\n','<br/>')
        _translate = QtCore.QCoreApplication.translate
        self.zOutResultTextEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"+temp+"</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        return

    def showModPhaseFunction(self,isLatex, isMod):
        if isMod:
            temp = self.circuitSolver.getMod()
        else:
            temp = self.circuitSolver.getPhase()
        if isLatex:
            temp = sy.latex(temp)
        else:
            temp = sy.pretty(temp)
            temp = temp.replace('\n','<br/>')
        _translate = QtCore.QCoreApplication.translate
        self.modPhaseResultTextEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"+temp+"</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        return


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Logic(None)
    ui.show()
    sys.exit(app.exec_())
        
    
main()