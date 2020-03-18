import os
import sys
import math
import vtk

from QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import (QApplication,
                               QWidget,
                               QSlider,
                               QVBoxLayout)

class QVolumeViewWidget(QWidget):
    def __init__(self, parent=None):
        super(QVolumeViewWidget, self).__init__(parent)
        # set up vtk pipeline and create vtkWidget
        self.renw = vtk.vtkRenderWindow()
        self.iren = vtk.vtkGenericRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renw)
        kw = {
              'rw':   self.renw,
              'iren': self.iren
              }
        self.vtkWidget = QVTKRenderWindowInteractor(parent, **kw)
        self.MainLayout = QVBoxLayout()
        self.MainLayout.addWidget(self.vtkWidget)
        self.setLayout(self.MainLayout)
        # self.vtkWidget = QVTKRenderWindowInteractor()
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)

        # add the orientation marker widget
        self.axes = vtk.vtkAxesActor()
        self.widget = vtk.vtkOrientationMarkerWidget()
        xyzLabels = ['R', 'A', 'S']
        self.axes.SetXAxisLabelText(xyzLabels[0])
        self.axes.SetYAxisLabelText(xyzLabels[1])
        self.axes.SetZAxisLabelText(xyzLabels[2])
        self.widget.SetOrientationMarker(self.axes)
        self.widget.SetInteractor(self.vtkWidget)
        self.widget.SetViewport(0.8, 0.0, 1, 0.3)
        self.widget.SetEnabled(True)
        self.widget.InteractiveOn()
        self.picker = vtk.vtkVolumePicker()


    def set_data_reader(self, reader):
        volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
        # volumeMapper.SetBlendModeToMaximumIntensity()
        volumeMapper.SetInputData(reader.GetOutput())
        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        self.ren.AddVolume(volume)

    def start_render(self):
        # start render and interactor
        self.vtkWidget.Initialize()
        self.vtkWidget.Start()
        self.ren.SetBackground(1,1,1)
        self.ren.ResetCamera()


if __name__ == '__main__':
    # raise the error log
    log_file = 'log.txt'
    with open(log_file, 'wb') as f:
        f.truncate()
    file_output_window = vtk.vtkFileOutputWindow()
    file_output_window.SetFileName(log_file)
    vtk.vtkFileOutputWindow.SetInstance(file_output_window)
    app = QApplication(sys.argv)
    SingleView = QVolumeViewWidget()
    file_name = "test_data.nii.gz"
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(file_name)
    reader.Update()
    SingleView.set_data_reader(reader)
    SingleView.start_render()
    SingleView.show()

    sys.exit(app.exec_())

