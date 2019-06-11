from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox,QCheckBox
import MySQLdb as sql
import pandas as pd
from pandasModel import PandasModel


host=""
user=""
password=""
database = ""


class MainWindow(QtWidgets.QWidget):

  def __init__(self,ui_base,parent=None):
    super(MainWindow, self).__init__(parent)
    layout = QtWidgets.QVBoxLayout()
    self.instance =uic.loadUi(ui_base)
    layout.addWidget(self.instance)
    self.setLayout(layout)

    self.setWindowTitle("Cedar") 
    self.showMaximized()


    self.instance.loadButton.clicked.connect(self.loadDatabase)
    self.instance.populateButton.clicked.connect(self.populate_rows)
    # self.instance.labelColLineEdit.clicked.connect(self.highlight_label_col)
    self.instance.searchButton.clicked.connect(self.populate_rows)

    self.checkboxes = []

  def loadDatabase(self):
    successful_connection=False
    try:
        connection = sql.connect(host, user, password, database)
        # QMessageBox.about(self, 'Connection', 'Database Connected Successfully')
        successful_connection=True
    except sql.Error as e:
        QMessageBox.about(self, 'Connection', 'Failed To Connect Database')


    if successful_connection:
      cursor = connection.cursor()
      cursor.execute(f"USE {database}")
      cursor.execute("SHOW TABLES")


      tables_and_count={}
      for (table_name,) in cursor:
        cursor.execute(f"select count(*) from {table_name}")  
        n_rows = cursor.fetchall()
        tables_and_count[table_name] = n_rows
        # print(f"{table_name}: {n_rows}")
      row = 0
      column = 0
      for key,value in tables_and_count.items():
        label = key+" ("+str(value[0][0])+")"
        checkbox = QCheckBox(label)
        checkbox.setObjectName(key+"_table_checkbox")
        checkbox.setChecked(True)
        self.instance.tableGrid.addWidget(checkbox,row,column)
        self.checkboxes.append(key)
        column+=1
        if column==8:
          row+=1
          column=0

  def populate_rows(self):


    self.search_term = self.instance.searchEdit.text()

    from_date="01-01-2018"
    to_date="01-01-2019"

    successful_connection=False
    try:
        connection = sql.connect(host, user, password, database)
        # QMessageBox.about(self, 'Connection', 'Database Connected Successfully')
        successful_connection=True
    except sql.Error as e:
        QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
    
    if successful_connection:
      checked_tables=[]

      for child in self.instance.findChildren(QCheckBox):
        if "table_checkbox" in child.objectName():
          if child.isChecked():
            checked_tables.append(child.objectName())

      for key in checked_tables:
        if self.search_term:
          sql_select_query = ("SELECT * FROM {table} WHERE MATCH (Headline,Description)"
          " AGAINST ('{keywords}' IN NATURAL LANGUAGE MODE)").format(table=key.replace("_table_checkbox",""),keywords=self.search_term)
        else:
          sql_select_query = ("SELECT * FROM {table} LIMIT 100 ").format(table=key.replace("_table_checkbox",""))
        dataframe = pd.read_sql(sql_select_query, con=connection)
        model = PandasModel(dataframe)
        self.instance.tableView.setModel(model)


  # def highlight_label_col(self):





