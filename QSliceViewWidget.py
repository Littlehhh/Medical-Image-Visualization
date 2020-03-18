import sys
import vtk

from QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import (QDesktopWidget,
                               QApplication,
                               QWidget,
                               QSlider,
                               QVBoxLayout)


class QSliceViewWidget(QWidget):
    """
    sagittal
    coronal
    transverse
    """
    def __init__(self, orientation='transverse', parent=None):
        super(QSliceViewWidget, self).__init__(parent)
        # set up vtk pipeline and create vtkWidget
        colors = vtk.vtkNamedColors()
        self.orientation = orientation
        self.viewer = vtk.vtkImageViewer2()
        self.orientations = {'coronal':    0,
                             'sagittal':   1,
                             'transverse': 2}
        self.viewer.SetSliceOrientation(self.orientations[self.orientation])
        # get&set the camera
        self.camera = self.viewer.GetRenderer().GetActiveCamera()
        ras = [[-1.0, 0.0, 0.0],
               [0.0, 1.0, 0.0],
               [0.0, 0.0, -1.0]]
        self.camera.SetPosition(ras[self.orientations[self.orientation]])
        self.camera.ParallelProjectionOn()
        self.iren = vtk.vtkGenericRenderWindowInteractor()
        self.iren.SetRenderWindow(self.viewer.GetRenderWindow())
        kw = {
              'rw':   self.viewer.GetRenderWindow(),
              'iren': self.iren
              }
        self.vtkWidget = QVTKRenderWindowInteractor(parent, **kw)

        # create QSlider
        self.sliderWidget = QSlider(Qt.Horizontal)
        # create the MainLayout of the whole widget
        self.MainLayout = QVBoxLayout()
        self.MainLayout.addWidget(self.sliderWidget)
        self.MainLayout.addWidget(self.vtkWidget)
        self.setLayout(self.MainLayout)
        # set the signal and slot
        self.sliderWidget.valueChanged.connect(self.slider_changed)

    def set_data_reader(self, reader, use_port=False):
        self.viewer.SetInputData(reader.GetOutput())
        matrix = reader.GetSFormMatrix()
        self.viewer.GetImageActor().PokeMatrix(matrix)

    def slider_offset(self, offset):
        self.sliderWidget.setMaximum(self.viewer.GetSliceMax())
        self.sliderWidget.setMinimum(self.viewer.GetSliceMin())
        mid = (self.viewer.GetSliceMax()-self.viewer.GetSliceMin())/2
        self.sliderWidget.setValue(mid)

    def start_render(self):
        # initiate slider
        self._init_slider()

        # set InteractorStyle
        interactor_style = vtk.vtkInteractorStyleImage()
        self.vtkWidget.SetInteractorStyle(interactor_style)

        # start render and interactor
        self.vtkWidget.Initialize()
        self.vtkWidget.Start()
        # set camera
        self.viewer.GetRenderer().ResetCamera()

    def _init_slider(self):
        self.sliderWidget.setMaximum(self.viewer.GetSliceMax())
        self.sliderWidget.setMinimum(self.viewer.GetSliceMin())
        mid = (self.viewer.GetSliceMax()-self.viewer.GetSliceMin())/2
        self.sliderWidget.setValue(mid)

    # signal and slot
    def slider_changed(self):
        self.viewer.SetSlice(self.sliderWidget.value())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # raise the error log
    log_file = 'log.txt'
    with open(log_file, 'wb') as f:
        f.truncate()
    file_output_window = vtk.vtkFileOutputWindow()
    file_output_window.SetFileName(log_file)
    vtk.vtkFileOutputWindow.SetInstance(file_output_window)
    # 'coronal': 0,
    # 'sagittal': 1,
    # 'transverse': 2
    SingleView = QSliceViewWidget(orientation='coronal')
    file_name = "test_data.nii.gz"
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(file_name)
    reader.Update()

    SingleView.set_data_reader(reader)
    SingleView.start_render()
    SingleView.resize(QSize(800, 600))
    SingleView.show()

    sys.exit(app.exec_())

