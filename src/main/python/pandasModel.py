from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QAbstractItemModel
from PyQt5.QtGui import QBrush,QColor
import pandas as pd

class PandasModel(QtCore.QAbstractTableModel): 

    def __init__(self, df = pd.DataFrame(),editable_column=False, parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self.editable_column = editable_column
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role == Qt.BackgroundRole:
            if self.editable_column!=False:
                if index.column() == self.editable_column:
                    return QBrush(QColor(152,251,152))
        elif role != Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))


    def flags(self, index):
        flags = super(PandasModel, self).flags(index)

        if self.editable_column!=False:
            if index.column() in (int(self.editable_column),):
                flags |= Qt.ItemIsEditable
            else:
                flags &= Qt.ItemIsSelectable
        return flags


    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.at[row,col]=value
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()