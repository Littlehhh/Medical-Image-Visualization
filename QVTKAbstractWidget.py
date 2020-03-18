import sys
import vtk

from PySide2.QtWidgets import QWidget

class QAbstractWidget(QWidget):
    def __init__(self, parent=None):
        super(QVolumeViewWidget, self).__init__(parent)
