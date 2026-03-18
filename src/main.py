#!/usr/bin/env python3
"""
PyQt6 Demo Application with WebEngine
A simple cross-platform GUI application with web browser
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton, QLineEdit, QHBoxLayout, QToolBar,
    QMessageBox
)
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("PyQt6 Web Browser Demo")
        self.setMinimumSize(QSize(1024, 768))
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("🌐 PyQt6 WebEngine 演示")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # URL bar with buttons
        url_bar_layout = QHBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setText("https://www.baidu.com")
        self.url_input.setPlaceholderText("输入网址...")
        self.url_input.returnPressed.connect(self.navigate_to_url)
        url_bar_layout.addWidget(self.url_input)
        
        btn_go = QPushButton("前往")
        btn_go.clicked.connect(self.navigate_to_url)
        url_bar_layout.addWidget(btn_go)
        
        btn_back = QPushButton("←后退")
        btn_back.clicked.connect(self.go_back)
        url_bar_layout.addWidget(btn_back)
        
        btn_forward = QPushButton("前进→")
        btn_forward.clicked.connect(self.go_forward)
        url_bar_layout.addWidget(btn_forward)
        
        btn_home = QPushButton("🏠首页")
        btn_home.clicked.connect(self.go_home)
        url_bar_layout.addWidget(btn_home)
        
        layout.addLayout(url_bar_layout)
        
        # Web Engine View
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://www.baidu.com"))
        
        # Connect signals
        self.web_view.urlChanged.connect(self.update_url_bar)
        self.web_view.loadFinished.connect(self.on_load_finished)
        
        layout.addWidget(self.web_view)
        
        # Status bar
        self.statusBar().showMessage("就绪")
        
        # Set initial focus
        self.url_input.setFocus()
    
    def navigate_to_url(self):
        """Navigate to the URL entered in the input"""
        url = self.url_input.text().strip()
        if not url:
            return
        
        # Add https:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        self.web_view.setUrl(QUrl(url))
        self.statusBar().showMessage(f"正在加载: {url}")
    
    def go_back(self):
        """Go back in history"""
        if self.web_view.history().canGoBack():
            self.web_view.back()
    
    def go_forward(self):
        """Go forward in history"""
        if self.web_view.history().canGoForward():
            self.web_view.forward()
    
    def go_home(self):
        """Go to home page"""
        self.web_view.setUrl(QUrl("https://www.baidu.com"))
        self.url_input.setText("https://www.baidu.com")
    
    def update_url_bar(self, q):
        """Update URL bar when URL changes"""
        self.url_input.setText(q.toString())
    
    def on_load_finished(self, ok):
        """Handle load finished event"""
        if ok:
            self.statusBar().showMessage("加载完成")
        else:
            self.statusBar().showMessage("加载失败")
            QMessageBox.warning(self, "加载错误", "无法加载网页，请检查网络连接")


def main():
    # High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("PyQt6 WebBrowser")
    app.setOrganizationName("Demo")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
