# Python + Kivy / FFT Acquisition and Screen
#   Module : CéTI/IéTI
# --------------------------------------------------------------
#    Acquisition via Nucléo et Affichage FFT
# --------------------------------------------------------------
#    Auteur : Julien VILLEMEJANE
#    Date : 13/10/2020
# --------------------------------------------------------------
# main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import nucleo as nucB


class FFTErrorPopup():
    def __init__(self, texte):
        layout = GridLayout(cols=1, padding=10)
        popupLabel = Label(text=texte)
        closeButton = Button(text="Close",size_hint=(0.7, 0.2))
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)
        popup = Popup(title='Error',
                      content=layout,
                      size_hint=(0.8, 0.4))
        popup.open()
        closeButton.bind(on_press=popup.dismiss)


class FFTConfigDataWindow(Screen):
    btnStartAcq = ObjectProperty(None)

    def acquireDataNucleo(self):
        if myApp.nucleo.isConnected():
            myApp.sm.current = "acquisition"
            print("Nucleo OK")
        else:
            FFTErrorPopup('Nucleo not connected')

    def testNucleo(self):
        print("To do / Test USB")
        myApp.nucleo.connectToBoard()
        if myApp.nucleo.isConnected():
            myApp.screens[1].btnStartAcq.disabled = False
        

class FFTAcquisitionDataWindow(Screen):
    def processFFTData(self):
        myApp.sm.current = "fftplotting"
        print("FFT process")

    def backToConfig(self):
        myApp.sm.current = "config"
        print("Back to Config")


class FFTPlottingWindow(Screen):
    def backToData(self):
        myApp.sm.current = "acquisition"
        print("Back to Data")

    def backToConfig(self):
        myApp.sm.current = "config"
        print("Back to Config")


class FFTTestDataWindow(Screen):
    def backToData(self):
        myApp.sm.current = "acquisition"
        print("Back to Data")

    def backToConfig(self):
        myApp.sm.current = "config"
        print("Back to Config")


class FFTWindowManager(ScreenManager):
    pass


class MyMainApp(App):
    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)
        self.kv = Builder.load_file("fft.kv")

        self.sm = FFTWindowManager()

        self.screens = [FFTAcquisitionDataWindow(name="acquisition"),
                        FFTConfigDataWindow(name="config"),
                        FFTPlottingWindow(name="fftplotting"),
                        FFTTestDataWindow(name="testw")]
        for screen in self.screens:
            self.sm.add_widget(screen)

        self.sm.current = "config"
        self.screens[1].btnStartAcq.disabled = True
        self.nucleo = nucB.NucleoBoard()

    def build(self):
        return self.sm


myApp = MyMainApp()

if __name__ == "__main__":
    myApp.run()
