from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QHBoxLayout)
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QPalette, QColor, QLinearGradient, QBrush, QIntValidator, QDesktopServices
from urllib.parse import urlparse
import sys
import programX


class Worker(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, url, start_page, end_page, folder):
        super().__init__()
        self.url = url
        self.start_page = start_page
        self.end_page = end_page
        self.folder = folder

    def run(self):
        try:
            programX.main_function(self.url, self.start_page, self.end_page, self.folder, self.log_function)
        except Exception as e:
            self.log_function(f"Error occurred: {str(e)}")

    def log_function(self, message):
        self.log_signal.emit(message)


class GlassmorphicApp(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.initUI()

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()

    def initUI(self):
        # Get the screen dimensions
        app = QApplication.instance()
        screen = app.primaryScreen()
        width, height = screen.size().width(), screen.size().height()
        window_width, window_height = 1200, 900

        self.setWindowTitle("ProjectX GUI")
        self.setGeometry((width - window_width) // 2, (height -
                         window_height) // 2, window_width, window_height)

        # Background color
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#a1c4fd"))
        gradient.setColorAt(1.0, QColor("#c2e9fb"))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Main layout
        self.main_layout = QVBoxLayout(self)

        # Welcome Screen
        self.welcome_label = QLabel("Welcome to ProjectX", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 32px; color: #fff;")
        self.main_layout.addWidget(self.welcome_label)

        # Fade out animation for the welcome screen
        self.fade_out_animation = QPropertyAnimation(
            self.welcome_label, b"windowOpacity")
        # Set fade-out duration to 1.5 seconds
        self.fade_out_animation.setDuration(1500)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)

        # Timer to trigger the fade out after 2 seconds
        QTimer.singleShot(2000, self.fadeOutWelcome)

    def fadeOutWelcome(self):
        self.fade_out_animation.finished.connect(self.loadMainScreen)
        self.fade_out_animation.start()

    def loadMainScreen(self):
        self.welcome_label.hide()

        # Create a glassmorphic content area
        self.glass_area = QWidget(self)
        self.glass_area.setStyleSheet(""" 
            background: rgba(255, 255, 255, 0.2); 
            border-radius: 15px; 
            padding: 20px; 
        """)
        self.main_layout.addWidget(self.glass_area)

        # Set layout for the glass area
        glass_layout = QVBoxLayout(self.glass_area)

        # Title
        self.title = QLabel("Project X", self.glass_area)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(
            "font-size: 40px; font-weight: bold; color: #0089a4; padding: 10px; background: transparent;")
        self.title.setFixedHeight(70)
        glass_layout.addWidget(self.title)

        # URL input area
        self.url_input = QLineEdit(self.glass_area)
        self.url_input.setPlaceholderText("Enter URL")
        self.url_input.setStyleSheet(
            "border: 2px dotted #00b4d8; background: transparent;")
        self.url_input.setFixedHeight(70)
        glass_layout.addWidget(self.url_input)

        # Page input areas on the same line
        page_layout = QHBoxLayout()
        page_layout.setSpacing(20)

        self.start_page = QLineEdit(self.glass_area)
        self.start_page.setPlaceholderText("Start Page")
        self.start_page.setValidator(QIntValidator(
            1, 999))  # Only accept integer input
        self.start_page.setStyleSheet(
            "border: 2px dotted #00b4d8; background: transparent;")
        self.start_page.setFixedHeight(70)
        page_layout.addWidget(self.start_page)

        self.end_page = QLineEdit(self.glass_area)
        self.end_page.setPlaceholderText("End Page")
        self.end_page.setValidator(QIntValidator(
            1, 999))  # Only accept integer input
        self.end_page.setStyleSheet(
            "border: 2px dotted #00b4d8; background: transparent;")
        self.end_page.setFixedHeight(70)
        page_layout.addWidget(self.end_page)

        glass_layout.addLayout(page_layout)

        # Folder Selection
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(20)

        self.folder_btn = QPushButton("Choose Folder", self.glass_area)
        self.folder_btn.setFixedHeight(70)
        self.folder_btn.clicked.connect(self.selectFolder)
        folder_layout.addWidget(self.folder_btn)

        # Folder path display
        self.folder_path_display = QLineEdit(self.glass_area)
        self.folder_path_display.setPlaceholderText(
            "Selected folder will appear here...")
        self.folder_path_display.setStyleSheet(
            "border: 2px dotted #00b4d8; background: transparent;")
        self.folder_path_display.setFixedHeight(70)
        folder_layout.addWidget(self.folder_path_display)

        glass_layout.addLayout(folder_layout)

        # Detailed Button
        self.submit_btn = QPushButton("Start Process", self.glass_area)
        self.submit_btn.clicked.connect(self.onSubmit)
        self.submit_btn.setStyleSheet("""
            background-color: #00b4d8;
            border-radius: 10px;
            color: #fff;
            padding: 10px;
            font-size: 16px;
            height: 70px;
        """)
        glass_layout.addWidget(self.submit_btn)

        # Hidden Terminal-like Output Area
        self.output_area = QTextEdit(self.glass_area)
        self.output_area.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.7);
            color: #00ff00;
            font-family: 'Courier New';
            font-size: 16px;
            border: none;
        """)

        self.output_area.setReadOnly(True)
        self.output_area.hide()
        self.output_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        glass_layout.addWidget(self.output_area)


        # Container to hold the post-download buttons
        self.post_download_buttons = QWidget(self.glass_area)
        self.post_download_buttons.hide()  # Hidden initially
        self.post_buttons_layout = QHBoxLayout(self.post_download_buttons)  # Changed to QHBoxLayout

        # Adding space before the first button for better alignment
        self.post_buttons_layout.addStretch(1)

        button_width = 150  # Set equal width for all buttons

        # Button to open folder in explorer
        self.open_folder_btn = QPushButton("Open Folder", self.post_download_buttons)
        self.open_folder_btn.setFixedWidth(button_width)  # Set fixed width
        self.open_folder_btn.setStyleSheet(self.submit_btn.styleSheet())  # Same style as submit button
        self.open_folder_btn.clicked.connect(self.openFolder)
        self.post_buttons_layout.addWidget(self.open_folder_btn)

        # Spacer between buttons
        self.post_buttons_layout.addSpacing(20)

        # Button to download more (reset the UI)
        self.download_more_btn = QPushButton("Download More", self.post_download_buttons)
        self.download_more_btn.setFixedWidth(button_width)  # Set fixed width
        self.download_more_btn.setStyleSheet(self.submit_btn.styleSheet())  # Same style
        self.download_more_btn.clicked.connect(self.resetUI)
        self.post_buttons_layout.addWidget(self.download_more_btn)

        # Spacer between buttons
        self.post_buttons_layout.addSpacing(20)

        # Button to exit the app
        self.exit_btn = QPushButton("Exit", self.post_download_buttons)
        self.exit_btn.setFixedWidth(button_width)  # Set fixed width
        self.exit_btn.setStyleSheet(self.submit_btn.styleSheet())  # Same style
        self.exit_btn.clicked.connect(self.closeApp)
        self.post_buttons_layout.addWidget(self.exit_btn)

        # Adding space after the last button for better alignment
        self.post_buttons_layout.addStretch(1)

        # Add post_download_buttons to the main layout, but it is hidden initially
        self.main_layout.addWidget(self.post_download_buttons)

    def openFolder(self):
        folder = self.folder_path_display.text()
        if folder:
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path_display.setText(folder)

    def resetUI(self):
        self.output_area.clear()
        self.output_area.hide()
        self.post_download_buttons.hide()

        # Show all input fields and buttons again
        for x in self.glass_area.children():
            if x.isWidgetType() and x not in [self.output_area, self.post_download_buttons]:
                x.show()

        # Clear input fields
        self.url_input.clear()
        self.start_page.clear()
        self.end_page.clear()
        self.folder_path_display.clear()

    def closeApp(self):
        self.close()

    def onSubmit(self):
        self.submit_btn.setEnabled(False)
        self.output_area.show()

        # Get inputs
        url = self.url_input.text()
        start_page = self.start_page.text()
        end_page = self.end_page.text()
        folder = self.folder_path_display.text()

        if not url or not self.is_valid_url(url):
            self.output_area.append("Please enter a valid URL.")
            return
        if not start_page.isdigit() or not end_page.isdigit():
            self.output_area.append("Start and End pages must be valid integers.")
            return
        if int(start_page) > int(end_page):
            self.output_area.append("Start Page cannot be greater than End Page.")
            return
        if not folder:
            self.output_area.append("Please select a folder.")
            return

        
        # Show title and terminal only
        for x in self.glass_area.children():
            if x.isWidgetType() and x not in [self.title, self.output_area]:
                x.hide()
        
        self.output_area.clear()
        self.output_area.append("Process started...")

        # Start worker thread
        self.worker = Worker(url, int(start_page), int(end_page), folder)
        self.worker.log_signal.connect(self.log_to_gui)
        self.worker.finished.connect(self.showPostDownloadButtons)
        self.worker.start()

    def is_valid_url(self, url):
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])

    def showPostDownloadButtons(self):
        self.post_download_buttons.show()

    def log_to_gui(self, message):
        if "error" in message.lower() or "fail" in message.lower() or "details" in message.lower():
            self.output_area.setTextColor(QColor("red"))
        else:
            self.output_area.setTextColor(QColor("#00ff00"))

        self.output_area.append(message)
        self.output_area.verticalScrollBar().setValue(self.output_area.verticalScrollBar().maximum())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GlassmorphicApp()
    ex.show()
    sys.exit(app.exec_())
