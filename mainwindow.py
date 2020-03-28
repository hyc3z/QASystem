import csv

from PyQt5.QtGui import QPalette, QBrush, QPixmap, QIcon
from pandas import read_csv,DataFrame
from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
import pandas as pd
import numpy as np
import jieba
import jieba.analyse

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        palette=QPalette()
        # palette.setBrush(QPalette.Background,QBrush(QPixmap("background.png")))
        palette.setBrush(QPalette.Background,QBrush(QPixmap("back3.jpg")))
        # palette.setBrush(QPalette.Background,QBrush(QPixmap("back4.png")))
        self.setPalette(palette)
        self.setFixedSize(1450,780)

        self.setWindowIcon(QIcon("Q14.ico"))
        self.SEN_COS_VAL=0.0035
        self.n_clusters=7
        self.Jieba_topK=200
        self.TargetContext=""
        self.WTMC_content_words=[]
        self.GZXX_content_words=[]
        self.GZYY_content_words=[]
        self.YZ_content_words=[]
        self.JZCS_content_words=[]
        self.data=[]
        self.num_totalREC=0
        self.user_path='user_dict.txt'
        self.TargetContext_words_data=""
        self.searchResult=[]
    def treeFuzzShow(self,str_kuang,column_index):
        i=0
        for index in range(len(self.data)):
            # print(self.data[index])
            tmp_str=self.data[index][column_index]
            tmp_str=str(tmp_str)
            if str_kuang in tmp_str:
                print(str_kuang,tmp_str)
                self.showtable([self.data[index]])
                self.searchResult.append(self.data[index])
                self.top_TEN[i]=index
                i=i+1

    def showtable(self,items):
        tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        count=tableWidget.rowCount()

        for i in range(len(items)):
            item = items[i]
            tableWidget.insertRow(i+count)

            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                item.setToolTip(str(items[i][j]))
                tableWidget.setItem(i+count, j, item)
        # tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        tableWidget.horizontalHeader().setStretchLastSection(True)

    def delRow(self):
        tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        count=tableWidget.rowCount()
        for i in range(0,count)[::-1]:
            tableWidget.removeRow(i)
    def init(self):
        # self.init_button()
        self.setWindowTitle("相似质量问题查询,欢迎访问！")
        tmpdata=pd.read_csv("qms_ok.csv",encoding="gb2312")
        ans=[]
        tmp=[]
        for index in range(len(tmpdata)):
            tmp=[]
            tmp.append(tmpdata.loc[index][0])
            tmp.append(tmpdata.loc[index][1])
            tmp.append(tmpdata.loc[index][2])
            tmp.append(tmpdata.loc[index][3])
            tmp.append(tmpdata.loc[index][4])
            tmp.append(tmpdata.loc[index][5])
            tmp.append(tmpdata.loc[index][6])
            tmp.append(tmpdata.loc[index][7])
            ans.append(tmp)


            self.WTMC_content_words.append(jieba.analyse.extract_tags(str(tmpdata.loc[index][1]),topK=self.Jieba_topK))
            self.GZXX_content_words.append(jieba.analyse.extract_tags(str(tmpdata.loc[index][2]),topK=self.Jieba_topK))
            self.GZYY_content_words.append(jieba.analyse.extract_tags(str(tmpdata.loc[index][3]),topK=self.Jieba_topK))
            self.YZ_content_words.append(jieba.analyse.extract_tags(str(tmpdata.loc[index][4]),topK=self.Jieba_topK))
            self.JZCS_content_words.append(jieba.analyse.extract_tags(str(tmpdata.loc[index][5]),topK=self.Jieba_topK))
        self.showtable(ans)
        self.data=ans
        self.num_totalREC=len(ans)
        self.TargetContext_words_data=np.zeros(self.num_totalREC)
        self.top_TEN=np.zeros(self.num_totalREC,dtype=int)
        self.top_TEN_sava=np.zeros(self.num_totalREC,dtype=int)
        self.btnConnect()
    def similay_jaccard(self,list_word1,list_word2):
        """计算相似度的函数
           param list_word1 是一个jiaba分词后list
           param list_word2 是一个jiaba分词后list
           return list_word1和list_word2按照jaccard算法后得出的相似度jaccard_coefficient
        """
        grams_reference = set(list_word1)
        grams_model = set(list_word2)
        temp = 0
        for i in grams_reference:
            if i in grams_model:
                temp = temp + 1
        fenmu = len(grams_model) + len(grams_reference) - temp  # 并集 - 交集
        jaccard_coefficient = float(temp / fenmu)
        return jaccard_coefficient
    def contextSearch(self):
        plainTextEdit=self.findChild(QtWidgets.QPlainTextEdit,"plainTextEdit")
        TargetContent = plainTextEdit.toPlainText()
        self.delRow()
        self.searchResult=[]
        if TargetContent!="":
            TargetContent_words=jieba.analyse.extract_tags(TargetContent,topK=self.Jieba_topK)
            print(TargetContent_words)
            for index in range(self.num_totalREC):
                if self.checkbox2.isChecked() and self.checkbox3.isChecked()==False and self.checkbox4.isChecked()==False and self.checkbox5.isChecked()==False:
                    recordStrAdd_words = self.WTMC_content_words[index]

                    self.TargetContext_words_data[index]=self.similay_jaccard(recordStrAdd_words,TargetContent_words)
                    continue
                if self.checkbox2.isChecked()==False and self.checkbox3.isChecked() and self.checkbox4.isChecked() == False and self.checkbox5.isChecked() == False:

                    recordStrAdd_words=self.GZXX_content_words[index]

                    self.TargetContext_words_data[index]=self.similay_jaccard(recordStrAdd_words,TargetContent_words)
                    continue
                if self.checkbox2.isChecked()==False and self.checkbox3.isChecked() and self.checkbox4.isChecked() and self.checkbox5.isChecked() == False:
                    recordStrAdd_words=self.YZ_content_words[index]
                    self.TargetContext_words_data[index]=self.similay_jaccard(recordStrAdd_words,TargetContent_words)
                    continue
                if self.checkbox2.isChecked()==False and self.checkbox3.isChecked() == False and self.checkbox4.isChecked()  and self.checkbox5.isChecked():
                    recordStrAdd_words=self.JZCS_content_words[index]
                    self.TargetContext_words_data[index]=self.similay_jaccard(recordStrAdd_words,TargetContent_words)
                    continue
                recordStrAdd_words=[]

                if self.checkbox2.isChecked():

                    recordStrAdd_words[len(recordStrAdd_words):len(recordStrAdd_words)]=self.WTMC_content_words[index]

                if self.checkbox3.isChecked():
                    recordStrAdd_words[len(recordStrAdd_words):len(recordStrAdd_words)] =self.GZXX_content_words[index]
                if self.checkbox3.isChecked():
                    recordStrAdd_words[len(recordStrAdd_words):len(recordStrAdd_words)] =self.YZ_content_words[index]
                if self.checkbox4.isChecked():
                    recordStrAdd_words[len(recordStrAdd_words):len(recordStrAdd_words)] = self.JZCS_content_words[index]

                self.TargetContext_words_data[index]=self.similay_jaccard(recordStrAdd_words,TargetContent_words)

            array_view=np.zeros((self.num_totalREC,2))
            for index in range(self.num_totalREC):
                array_view[index,0]=self.TargetContext_words_data[index]
                array_view[index,1]=index
            data_view=pd.DataFrame(array_view,columns=["相似度","序号"])
            data_view.sort_values(by=["相似度"],ascending=False,inplace=True)

            data_view.loc[data_view["相似度"]>self.SEN_COS_VAL]
            CUSOR=0
            for index in range(len(self.top_TEN)):
                CUSOR=int(data_view.iloc[index,1])
                self.top_TEN[index]=CUSOR


            for index in range(len(self.top_TEN)):
                CUSOR=self.top_TEN[index]
                tmp=[]
                k8=""
                k1 = self.data[CUSOR][0]
                k2 = self.data[CUSOR][1]
                k3 = self.data[CUSOR][2]
                k4 = self.data[CUSOR][3]
                k5 = self.data[CUSOR][4]
                k6 = self.data[CUSOR][5]
                k7 = self.data[CUSOR][6]

                k8 = k8 + str(self.TargetContext_words_data[CUSOR])

                tmp.append(k1)
                tmp.append(k2)
                tmp.append(k3)
                tmp.append(k4)
                tmp.append(k5)
                tmp.append(k6)
                tmp.append(k7)
                tmp.append(k8)

                if self.TargetContext_words_data[CUSOR]>self.SEN_COS_VAL:
                    self.showtable([tmp])
                    self.searchResult.append(tmp)

                else:
                    continue
        else:
            print("语义查询为空")
            self.showtable(self.data)

    def fuzzSearch(self):
        plainTextEdit = self.findChild(QtWidgets.QPlainTextEdit, "plainTextEdit")
        TargetContent = plainTextEdit.toPlainText()
        self.delRow()
        self.searchResult=[]
        if self.checkbox1.isChecked():
            self.treeFuzzShow(TargetContent,0)
        if self.checkbox2.isChecked():
            self.treeFuzzShow(TargetContent,1)

        if self.checkbox3.isChecked():
            self.treeFuzzShow(TargetContent,2)
        if self.checkbox4.isChecked():
            self.treeFuzzShow(TargetContent, 3)
        if self.checkbox5.isChecked():
            self.treeFuzzShow(TargetContent, 4)
        if self.checkbox6.isChecked():
            self.treeFuzzShow(TargetContent, 5)

    def exportResult(self):
        with open("Results.csv","w",encoding="gb2312") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(['编号','问题名称','故障现象','故障原因','纠正','纠正措施','故障原因分类','相似度'])
            writer.writerows(self.searchResult)

    def importData(self):
        pass
    def btnConnect(self):
        self.checkbox1=self.findChild(QtWidgets.QCheckBox,"checkBox")
        self.checkbox2=self.findChild(QtWidgets.QCheckBox,"checkBox_2")
        self.checkbox3=self.findChild(QtWidgets.QCheckBox,"checkBox_3")
        self.checkbox4=self.findChild(QtWidgets.QCheckBox,"checkBox_4")
        self.checkbox5=self.findChild(QtWidgets.QCheckBox,"checkBox_5")
        self.checkbox6=self.findChild(QtWidgets.QCheckBox,"checkBox_6")
        self.checkbox7=self.findChild(QtWidgets.QCheckBox,"checkBox_7")
        btn1=self.findChild(QtWidgets.QPushButton,"pushButton")
        btn1.clicked.connect(self.contextSearch)
        btn2=self.findChild(QtWidgets.QPushButton,"pushButton_2")
        btn2.clicked.connect(self.fuzzSearch)
        btn3=self.findChild(QtWidgets.QPushButton,"pushButton_3")
        btn3.clicked.connect(self.exportResult)
        btn4=self.findChild(QtWidgets.QPushButton,"pushButton_4")
        btn4.clicked.connect(self.importData)
    def init_button(self):
        # btn1=self.findChild(QtWidgets.QPushButton,"pushButton")
        # btn1.setStyleSheet("QPushButton{color:black}"
        #             "QPushButton:hover{color:blue}"
        #             "QPushButton{background-color:lightgreen}"
        #             "QPushButton{border:2px}"
        #             "QPushButton{border-radius:10px}"
        #             "QPushButton{padding:2px 4px}"
        #             "QPushButton{font-family:'宋体';font-size:28px}"
        #                    )
        btn1 = self.findChild(QtWidgets.QPushButton, "pushButton")
        btn1.setStyleSheet("QPushButton{color:white}"
                           "QPushButton:hover{color:blue}"
                           "QPushButton{background-color:blue}"
                           "QPushButton{border:2px}"
                           "QPushButton{border-radius:10px}"
                           "QPushButton{padding:2px 4px}"
                           "QPushButton{font-family:'宋体';font-size:28px}"
                           )
        btn1 = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        btn1.setStyleSheet("QPushButton{color:black}"
                           "QPushButton:hover{color:blue}"
                           "QPushButton{background-color:lightgreen}"
                           "QPushButton{border:2px}"
                           "QPushButton{border-radius:10px}"
                           "QPushButton{padding:2px 4px}"
                           "QPushButton{font-family:'宋体';font-size:28px}"
                           )
        btn1 = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        btn1.setStyleSheet("QPushButton{color:black}"
                           "QPushButton:hover{color:blue}"
                           "QPushButton{background-color:lightgreen}"
                           "QPushButton{border:2px}"
                           "QPushButton{border-radius:10px}"
                           "QPushButton{padding:2px 4px}"
                           "QPushButton{font-family:'宋体';font-size:28px}"
                           )
        btn1 = self.findChild(QtWidgets.QPushButton, "pushButton_4")
        btn1.setStyleSheet("QPushButton{color:black}"
                           "QPushButton:hover{color:blue}"
                           "QPushButton{background-color:lightgreen}"
                           "QPushButton{border:2px}"
                           "QPushButton{border-radius:10px}"
                           "QPushButton{padding:2px 4px}"
                           "QPushButton{font-family:'宋体';font-size:28px}"
                           )
        # btn1 = self.findChild(QtWidgets.QCheckBox, "checkBox")
        # btn1.setStyleSheet("QCheckBox{color:GreenYellow}"
        #                    "QCheckBox:hover{color:blue}"
        #
        #                    "QCheckBox{border:0px}"
        #                    "QCheckBox{border-radius:7px}"
        #                    "QCheckBox{padding:0px 4px}"
        #                    "QCheckBox{font-family:'宋体';font-size:22px}"
        #                    )
        # btn1 = self.findChild(QtWidgets.QCheckBox, "checkBox_2")
        # btn1.setStyleSheet("QCheckBox{color:GreenYellow}"
        #                    "QCheckBox:hover{color:blue}"
        #
        #                    "QCheckBox{border:0px}"
        #                    "QCheckBox{border-radius:10px}"
        #                    "QCheckBox{padding:2px 4px}"
        #                    "QCheckBox{font-family:'宋体';font-size:20px}"
        #                    )
        # btn1 = self.findChild(QtWidgets.QCheckBox, "checkBox_3")
        # btn1.setStyleSheet("QCheckBox{color:GreenYellow}"
        #                    "QCheckBox:hover{color:blue}"
        #
        #                    "QCheckBox{border:0px}"
        #                    "QCheckBox{border-radius:10px}"
        #                    "QCheckBox{padding:2px 4px}"
        #                    "QCheckBox{font-family:'宋体';font-size:20px}"
        #                    )
        # btn1 = self.findChild(QtWidgets.QCheckBox, "checkBox_4")
        # btn1.setStyleSheet("QCheckBox{color:GreenYellow}"
        #                    "QCheckBox:hover{color:blue}"
        #
        #                    "QCheckBox{border:0px}"
        #                    "QCheckBox{border-radius:10px}"
        #                    "QCheckBox{padding:2px 4px}"
        #                    "QCheckBox{font-family:'宋体';font-size:20px}"
        #                    )
        # btn1 = self.findChild(QtWidgets.QCheckBox, "checkBox_5")
        # btn1.setStyleSheet("QCheckBox{color:GreenYellow}"
        #                    "QCheckBox:hover{color:blue}"
        #
        #                    "QCheckBox{border:0px}"
        #                    "QCheckBox{border-radius:7px}"
        #                    "QCheckBox{padding:0px 4px}"
        #                    "QCheckBox{font-family:'宋体';font-size:22px}"
        #                    )
        # btn1 = self.findChild(QtWidgets.QCheckBox, "checkBox_6")
        # btn1.setStyleSheet("QCheckBox{color:GreenYellow}"
        #                    "QCheckBox:hover{color:blue}"
        #
        #                    "QCheckBox{border:0px}"
        #                    "QCheckBox{border-radius:10px}"
        #                    "QCheckBox{padding:2px 4px}"
        #                    "QCheckBox{font-family:'宋体';font-size:20px}"
        #                    )
        #
        # btn1 = self.findChild(QtWidgets.QCheckBox, "checkBox_7")
        # btn1.setStyleSheet("QCheckBox{color:GreenYellow}"
        #                    "QCheckBox:hover{color:blue}"
        #                    "QCheckBox{border:0px}"
        #                    "QCheckBox{border-radius:7px}"
        #                    "QCheckBox{padding:0px 4px}"
        #                    "QCheckBox{font-family:'宋体';font-size:22px}"
        #                    )
        #
        # btn1 = self.findChild(QtWidgets.QLabel, "label")
        # btn1.setStyleSheet("QLabel{color:black}"
        #                    "QLabel:hover{color:blue}"
        #                    "QLabel{background-color:lightgreen}"
        #                    "QLabel{border:0px}"
        #                    "QLabel{border-radius:10px}"
        #                    "QLabel{padding:2px 4px}"
        #                    "QLabel{font-family:'宋体';font-size:26px}"
        #                    )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())