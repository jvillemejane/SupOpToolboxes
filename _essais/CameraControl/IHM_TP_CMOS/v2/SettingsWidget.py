# Libraries to import
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication, QGroupBox, QSlider, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import sys

class Settings_Widget(QWidget):
    """
    Widget used to set our less important options.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of our widget.
        """
        super().__init__()
        self.setWindowTitle("Settings")

        # Creating the main layout
        layout = QVBoxLayout()
        
        # Creating and adding our settings
        self.AOISettingX = Setting_Widget_Int(settingLabel = " AOI X ")
        self.AOISettingY = Setting_Widget_Int(settingLabel = " AOI Y ")
        self.AOISettingWidth = Setting_Widget_Int(settingLabel = " AOI Width ")
        self.AOISettingHeight = Setting_Widget_Int(settingLabel = " AOI Height ")

        layout.addWidget(self.AOISettingX)
        layout.addWidget(self.AOISettingY)
        layout.addWidget(self.AOISettingWidth)
        layout.addWidget(self.AOISettingHeight)
        self.setLayout(layout)

    def AOIXGetValue(self):
        """
        Method used to get the value of AOI X.

        Returns:
            int: value of AOI X.
        """
        return self.AOISettingX.getValue()
    
    def AOIYGetValue(self):
        """
        Method used to get the value of AOI Y.

        Returns:
            int: value of AOI Y.
        """
        return self.AOISettingY.getValue()
    
    def AOIWidthGetValue(self):
        """
        Method used to get the value of AOI Width.

        Returns:
            int: value of AOI Width.
        """
        return self.AOISettingWidth.getValue()
    
    def AOIHeightGetValue(self):
        """
        Method used to get the value of AOI Height.

        Returns:
            int: value of AOI Height.
        """
        return self.AOISettingHeight.getValue()

class Setting_Widget_Int(QWidget):
    """
    Our sub-setting widget.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, settingLabel, minimumValue = 0, maximumValue = 100, initialisationValue = 50):
        """
        Initialisation of our setting widget.

        Args:
            settingLabel (str): name of the setting box
            minimumValue (int, optional): minimum value of the setting. Defaults to 0.
            maximumValue (int, optional): maximum value of the setting. Defaults to 100.
            initialisationValue (int, optional): base value of the setting. Defaults to 50.
        """
        super().__init__()
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(minimumValue)
        self.slider.setMaximum(maximumValue)
        self.slider.setValue(initialisationValue)
        self.selectionLabel = settingLabel

        group_box = QGroupBox(self.selectionLabel)
        layout = QGridLayout()

        # Create a layout
        line_label_layout = QGridLayout()

        # Create a line widget and place it into the grid layout
        self.line = QLineEdit(self)
        line_label_layout.addWidget(self.line, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        self.line.textChanged.connect(self.linetextValueChanged)
        self.slider.valueChanged.connect(self.sliderValueChanged)

        # Create a label widget and place it into the grid layout
        self.labelValue = QLabel(self.selectionLabel +"= " + str(initialisationValue))
        line_label_layout.addWidget(self.labelValue, 0, 1, 1, 1) # row = 0, column = 1, rowSpan = 1, columnSpan = 1

        layout.addWidget(self.slider, 0, 0, 1, 4) # row = 0, column = 0, rowSpan = 1, columnSpan = 4
        layout.addLayout(line_label_layout, 1, 0, 1, 4) # row = 1, column = 0, rowSpan = 1, columnSpan = 4

        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 0 <=> QHBoxLayout or V
        self.setLayout(main_layout)

    def linetextValueChanged(self, text):
        """
        Method used to set the self.value, self and the labelValue text each time the line is triggered.

        Args:
            text (str): string that'll be converted in float to changed the important values.
        """
        self.value = int(text)
        self.labelValue.setText(self.selectionLabel + "= " + str(text))
        self.slider.setValue(int(text))

    def sliderValueChanged(self, value):
        """
        Method used to set the self.value and and the labelValue text each time the slider is triggered.

        Args:
            value (int): useful value of the slider.
        """
        self.value = value
        self.labelValue.setText(self.selectionLabel + "= "+ str(value))

    def getValue(self):
        """
        Method used to get the value of the slider.

        Returns:
            int: value of the slider.
        """
        return self.slider.value()

    def setValue(self, value):
        """
        Method used to get the value of the slider.

        Args:
            value (int):  useful value of the slider.

        Raises:
            ValueError: Out of bounds.
        """
        if value < self.slider.minimum() or value > self.slider.maximum():
            raise ValueError("Value is out of range")
        self.slider.setValue(value)

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Settings_Widget()
    window.show()

    sys.exit(app.exec_())