from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QSlider,QPushButton, QLabel, QFileDialog, QHBoxLayout, QTextEdit, QCheckBox)
from PyQt5.QtCore import Qt
import sys
from ImageCompressor import ImageCompressor

class CompressorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Compressor")
        self.setGeometry(100, 100, 500, 400)
        self.setMaximumSize(800, 640) 
        self.selected_files = []
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        #Create titlee label
        title_label = QLabel("Image Compressor")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Create horizontal layout for text area and buttons
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        # Create text area for showing selected files
        filelayout = QVBoxLayout()
        h_layout.addLayout(filelayout)
        self.files_text = QTextEdit()
        self.files_text.setReadOnly(True)
        filelayout.addWidget(QLabel("Selected Files:"))
        filelayout.addWidget(self.files_text)

        # Create vertical layout for buttons
        button_layout = QVBoxLayout()
        h_layout.addLayout(button_layout)
        
        # Create select files button
        self.select_btn = QPushButton("Select Images")
        self.select_btn.clicked.connect(self.select_files)
        button_layout.addWidget(self.select_btn)

        # Create remove all files button
        self.remove_btn = QPushButton("Remove All")
        self.remove_btn.clicked.connect(self.remove_files)
        button_layout.addWidget(self.remove_btn)

        self.openfolder_check = QCheckBox("Open folder of images")
        button_layout.addWidget(self.openfolder_check)
        

        #Create horizontal layout for quality slider and file format
        h_layout2 = QHBoxLayout()
        layout.addLayout(h_layout2)

        # Create vertical layout for choosing quality
        self.qualitybox = QVBoxLayout()
        h_layout2.addLayout(self.qualitybox)

        # Create vertical layout for choosing file format
        self.formatbox = QVBoxLayout()
        h_layout2.addLayout(self.formatbox)

        # Create format selection combo box
        self.formatbox.addWidget(QLabel("Output Format:"))
        self.formatbox.addWidget(QLabel("JPG"))

        # Create quality slider
        quality_label = QLabel("Compression Quality:")
        self.qualitybox.addWidget(quality_label)

        init_quality = 85
        # Create quality slider
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(0)
        self.quality_slider.setMaximum(95)
        self.quality_slider.setValue(init_quality)
        self.quality_slider.setTickPosition(QSlider.TicksBelow)
        self.quality_slider.setTickInterval(5)

        self.quality_value = QLabel(f"Quality value (arbitary, not percentage): {init_quality}")
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        self.qualitybox.addWidget(self.quality_value)
        self.qualitybox.addWidget(self.quality_slider)
        
        # Create compress button
        self.compress_btn = QPushButton("Compress Images")
        self.compress_btn.clicked.connect(self.compress_images)
        layout.addWidget(self.compress_btn)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.gif)"
        )
        if files:
            self.selected_files = files
            self.files_text.setText("\n".join(files))

    def remove_files(self):
        self.selected_files = []
        self.files_text.clear()
    
    def update_quality_label(self, value):
        self.quality_value.setText(f"Quality value (arbitary, not percentage): {value}")
    
    def compress_images(self):
        if not self.selected_files:
            self.status_label.setText("Please select images first!")
            return
        
        quality = self.quality_slider.value()
        if quality == 0:
            quality = 1
        compressor = ImageCompressor(self.selected_files, quality, self.openfolder_check.isChecked())
        try:
            time = compressor.compress()
            self.status_label.setText(f"Compression completed successfully! ({round(time,2)} seconds)".format(time))
        except Exception as e:
            self.status_label.setText(f"Error during compression: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = CompressorGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
