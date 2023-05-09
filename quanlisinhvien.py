from PySide6 import QMainWindow,QApplication, QTableWidgetItem,QMessageBox
from ui_untitled import Ui_MainWindow
from PySide6.QtGui import QIcon,QColor
from PySide6.QtCore import QTimer
import xml.dom.minidom as xdm
import xml.etree.ElementTree as xee
from PySide6.QtXml import QDomDocument
import datetime
import random


class Qlsv(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic=Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.tableWidget.setColumnCount(6)
        self.uic.tableWidget.setHorizontalHeaderLabels(["Masv","Tênsv","Khoa","Lớp","GPA","Địa chỉ"])

       
        self.count=0
        self.uic.btnshow.clicked.connect(self.showeml)  
        self.uic.tableWidget.cellClicked.connect(self.clickshow)
        self.uic.btnadd.clicked.connect(self.addstudent) 
        self.uic.btndelete.clicked.connect(self.deletesv)
        self.uic.btnupdate.clicked.connect(self.updatesv)
        self.uic.btntk.clicked.connect(self.search)
        self.time=QTimer()
        self.timelabel=QTimer()
        
        self.time.timeout.connect(self.time1)
        self.timelabel.timeout.connect(self.slowlabel)
        self.timelabel.timeout.connect(self.whilecolor)
        self.time.start(1000)
    
        self.timelabel.start(250)

    def showeml(self):
        tree = xee.parse('student.xml')
        root=tree.getroot()
        self.uic.tableWidget.setRowCount(len(list(root)))
        for row,student in enumerate(root):
             self.uic.tableWidget.setItem(row,0,QTableWidgetItem(student.find("masv").text))
             self.uic.tableWidget.setItem(row,1,QTableWidgetItem(student.find("tensv").text))
             self.uic.tableWidget.setItem(row,2,QTableWidgetItem(student.find("khoa").text))
             self.uic.tableWidget.setItem(row,3,QTableWidgetItem(student.find("lop").text))
             self.uic.tableWidget.setItem(row,4,QTableWidgetItem(student.find("gpa").text))
             self.uic.tableWidget.setItem(row,5,QTableWidgetItem(student.find("diachi").text))
    def time1(self):
        dt=datetime.datetime.now()
        self.uic.datetime.setText(dt.strftime("%Y-%m-%d %H:%M:%S"))
    def clickshow(self,row,column):
        self.uic.lineEdit_2.setText(self.uic.tableWidget.item(row,0).text())
        self.uic.lineEdit_3.setText(self.uic.tableWidget.item(row,1).text())
        self.uic.lineEdit_4.setText(self.uic.tableWidget.item(row,2).text())
        self.uic.lineEdit_5.setText(self.uic.tableWidget.item(row,3).text())
        self.uic.lineEdit_6.setText(self.uic.tableWidget.item(row,4).text())
        self.uic.lineEdit_7.setText(self.uic.tableWidget.item(row,5).text())
    def addstudent(self):
        tree = xee.parse('student.xml')
        root=tree.getroot()
        newstudent=xee.Element('student')
        news_masv=xee.SubElement(newstudent,"masv")
        news_masv.text=self.uic.lineEdit_2.text()
        news_tensv=xee.SubElement(newstudent,"tensv")
        news_tensv.text=self.uic.lineEdit_3.text()
        news_khoa=xee.SubElement(newstudent,"khoa")
        news_khoa.text=self.uic.lineEdit_4.text()
        news_lop=xee.SubElement(newstudent,"lop")
        news_lop.text=self.uic.lineEdit_5.text()
        news_gpa=xee.SubElement(newstudent,"gpa")
        news_gpa.text=self.uic.lineEdit_6.text()
        news_diachi=xee.SubElement(newstudent,"diachi")
        news_diachi.text=self.uic.lineEdit_7.text()
        if self.uic.lineEdit_2.text()=="":
            QMessageBox.information(self, "Thông báo", "vui lòng nhập dữ liêu")
        else:
            root.append(newstudent)
            tree.write("student.xml")
            QMessageBox.information(self, "Thông báo", "Đã thêm sinh viên có mã sinh viên là %s thành công"%(self.uic.lineEdit_2.text()))
        self.showeml()
    def search(self):
        tree = xee.parse('student.xml')
        root=tree.getroot()
        student=root.findall("student")
        list_search=[]
        for i in student:
            if self.uic.edittk.text() in i.find("masv").text:
                list_search.append(i)

        print(list_search)
        self.uic.tableWidget.setRowCount(len(list_search))
        for row,student in enumerate(list_search):
            self.uic.tableWidget.setItem(row,0,QTableWidgetItem(student.find("masv").text))
            self.uic.tableWidget.setItem(row,1,QTableWidgetItem(student.find("tensv").text))
            self.uic.tableWidget.setItem(row,2,QTableWidgetItem(student.find("khoa").text))
            self.uic.tableWidget.setItem(row,3,QTableWidgetItem(student.find("lop").text))
            self.uic.tableWidget.setItem(row,4,QTableWidgetItem(student.find("gpa").text))
            self.uic.tableWidget.setItem(row,5,QTableWidgetItem(student.find("diachi").text))

    def updatesv(self):
        tree = xee.parse('student.xml')
        root=tree.getroot().findall("student")
        for student in root:
            if self.uic.lineEdit_2.text()==student.find("masv").text:
               print(student)
               student.find("tensv").text=self.uic.lineEdit_3.text()
               student.find("khoa").text=self.uic.lineEdit_4.text()
               student.find("lop").text=self.uic.lineEdit_5.text()
               student.find("gpa").text=self.uic.lineEdit_6.text()
               student.find("diachi").text=self.uic.lineEdit_7.text()

               print(student.find("tensv").text)
               
              
               
        tree.write("student.xml")
        QMessageBox.information(self, "Thông báo", "Đã sửa sinh viên có mã sinh viên là %s thành công"%(self.uic.lineEdit_2.text()))
        
        self.showeml()
        



    def deletesv(self):
        tree = xee.parse('student.xml')
        masv=self.uic.lineEdit_2.text()
        
     
        root=tree.getroot()
        for student in root.findall("student"):
            masv1=student.find("masv").text
            if masv==masv1:
                root.remove(student)
                
        tree.write("student.xml")
        QMessageBox.information(self, "Thông báo", "Đã xóa sinh viên có mã sinh viên là %s thành công"%(masv))
        self.showeml()
            
    # Xóa nút sinh viên đó khỏi nút gốc của tài liệu XML
    def slowlabel(self):
        text="ỨNG DỤNG XML VÀO HỆ THỐNG QUẢN LÍ SINH VIÊN"
        if self.count<len(text)+1:
            self.uic.label.setText(text[:self.count])
            self.count+=1
        else:
            self.count=0
    def whilecolor(self):
        r=random.randint(0,255)
        b=random.randint(0,255)
        g=random.randint(0,255)
        color=QColor.fromHsv(r,b,g)
        self.uic.label.setStyleSheet("color:"+color.name())


if __name__=="__main__":
    import sys
    App=QApplication(sys.argv)
    ql=Qlsv()
    ql.show()
    sys.exit(App.exec_())