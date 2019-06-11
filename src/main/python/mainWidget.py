from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox,QCheckBox,QHeaderView
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
    self.ui =uic.loadUi(ui_base)
    layout.addWidget(self.ui)
    self.setLayout(layout)

    self.setWindowTitle("Cedar") 
    self.showMaximized()


    self.ui.loadButton.clicked.connect(self.loadDatabase)
    self.ui.populateButton.clicked.connect(self.populate_rows)
    # self.ui.labelColLineEdit.clicked.connect(self.highlight_label_col)
    self.ui.searchButton.clicked.connect(self.populate_rows)
    self.ui.hideColLineEdit.textChanged.connect(self.hideColumns)
    self.ui.resizeRowsButton.clicked.connect(self.resizeRows)

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
        self.ui.tableGrid.addWidget(checkbox,row,column)
        self.checkboxes.append(key)
        column+=1
        if column==8:
          row+=1
          column=0

  def populate_rows(self):


    self.search_term = self.ui.searchEdit.text()
    self.search_cols = self.ui.searchFromCols.text()

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

      for child in self.ui.findChildren(QCheckBox):
        if "table_checkbox" in child.objectName():
          if child.isChecked():
            checked_tables.append(child.objectName())

      for key in checked_tables:
        if self.search_term:
          sql_select_query = ("SELECT * FROM {table} WHERE MATCH {search_cols}"
          " AGAINST ('{keywords}' IN NATURAL LANGUAGE MODE)").format(table=key.replace("_table_checkbox",""),keywords=self.search_term,search_cols=self.search_cols)
        else:
          sql_select_query = ("SELECT * FROM {table} LIMIT 100 ").format(table=key.replace("_table_checkbox",""))
        dataframe = pd.read_sql(sql_select_query, con=connection)
        self.model = PandasModel(dataframe)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

  def hideColumns(self):
    try:
      n_cols = self.model.columnCount()
      all_cols =  [i for i in range(0,n_cols)]
      cols_to_hide = []
      cols_from_line = self.ui.hideColLineEdit.text().split(",")
      for i in cols_from_line:
        try:
          cols_to_hide.append(int(i.strip()))
        except:
          pass
      for c in all_cols:
        if c in cols_to_hide:
          self.ui.tableView.setColumnHidden(int(c), True);
        else:
          self.ui.tableView.setColumnHidden(int(c), False);
    except:
      pass

  def resizeRows(self):
    self.ui.tableView.resizeRowsToContents();
