from panda3d.core import *
from math import cos, sin, atan2, acos, sqrt
from direct.showbase.ShowBase import ShowBase


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.model = self.loader.load_model('teapot')
        self.model.reparent_to(self.render)
        self.setup_view()

    def setup_view(self):

        ## Camera step for changes
        self.camSpeed = .05
        self.camZoomStep = 5

        # Set up camera zoom
        self.accept('wheel_up', self.zoom_in)
        self.accept('wheel_down', self.zoom_out)



    # Functions for camera zoom
    def zoom_out(self):
        """Translate the camera along its local y axis to zoom out the view"""
        self.cam.set_y(self.cam, -self.camZoomStep)

    def zoom_in(self):
        """Translate the camera along its local y axis to zoom in the view"""
        self.cam.set_y(self.cam, self.camZoomStep)
        # In case we get past the camera pivot, we look at it again

    #        if (newCamPos-camPos).length() >= (self.camPivot-camPos).length():
    #            self.cam.lookAt(self.camPivot)




app = App()
app.run()