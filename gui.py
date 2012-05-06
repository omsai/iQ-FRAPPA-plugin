"""
Qt Form for selecting iQImage
"""

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ImageListWindow(QDialog):

    def __init__(self, parent=None):
        super(ImageListWindow, self).__init__(parent)

        try:
            from imagedisk import iQImageDisk
            id = iQImageDisk()
            names = id.titles()
        except ImportError:
            names = ['frappa pa405',
                     'micropoint 365',
                     'mosaic gfp']

        # window title
        self.setWindowTitle("Select iQ Image")

        # view widget
        self.listView = QListView()
        self.sourceModel = QStandardItemModel(len(names), 1)
        i = 0
        for name in names:
            item = QStandardItem(name)
            self.sourceModel.setItem(i, item)
            i += 1
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.sourceModel)
        self.listView.setModel(self.proxyModel)

        # filter widgets
        self.filterLabel = QLabel("Find:")
        self.filterLineEdit = QLineEdit()

        # set layout
        grid = QGridLayout()
        grid.addWidget(self.filterLabel, 0, 0)
        grid.addWidget(self.filterLineEdit, 0, 1)
        grid.addWidget(self.listView, 1, 1)
        self.setLayout(grid)

        # set initial state
        self.filterLineEdit.setText("")

        # signals
        self.connect(self.filterLineEdit,
                     SIGNAL("textChanged(const QString&)"), self.filterList)

    def filterList(self):
        for index in range(self.proxyModel.rowCount()):
            print self.sourceModel.data(self.proxyModel.index(index, 0))

        regExp = QRegExp(self.filterLineEdit.text(),
                                Qt.CaseInsensitive, QRegExp.Wildcard)
        self.proxyModel.setFilterRegExp(regExp)

    def submit(self):
        print("clicked!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    imageListWindow = ImageListWindow()
    imageListWindow.show()
    app.exec_()
