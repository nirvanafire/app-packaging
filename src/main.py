#!/usr/bin/env python3
"""
PyQt6 Demo Application with WebEngine
A simple cross-platform GUI application with web browser
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton, QLineEdit, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView


def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和打包后环境"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时目录
        base_path = sys._MEIPASS
    else:
        # 开发环境
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("PyQt6 Web Browser")
        # 更大的默认窗口尺寸
        self.resize(1400, 900)
        self.setMinimumSize(800, 600)
        
        # 设置窗口图标
        icon_path = resource_path("icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout - 使用更紧凑的边距
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        central_widget.setLayout(layout)
        
        # 标题栏布局（更紧凑）
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # 小标题
        title = QLabel("🌐")
        title.setFont(QFont("Arial", 12))
        title.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(title)
        
        # URL 输入框（更宽）
        self.url_input = QLineEdit()
        self.url_input.setText("http://127.0.0.1:5000")
        self.url_input.setPlaceholderText("输入网址...")
        self.url_input.setFont(QFont("Arial", 11))
        self.url_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.url_input.setMinimumHeight(32)
        self.url_input.returnPressed.connect(self.navigate_to_url)
        header_layout.addWidget(self.url_input)
        
        # 紧凑的按钮
        for text, slot in [
            ("←", self.go_back),
            ("→", self.go_forward),
            ("⟳", self.go_home),
        ]:
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 11))
            btn.setMinimumWidth(36)
            btn.setMinimumHeight(32)
            btn.clicked.connect(slot)
            header_layout.addWidget(btn)
        
        layout.addLayout(header_layout)
        
        # Web Engine View（占据主要空间）
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("http://127.0.0.1:5000"))
        
        # 设置浏览器组件的尺寸策略，使其可以伸展
        self.web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Connect signals
        self.web_view.urlChanged.connect(self.update_url_bar)
        self.web_view.loadFinished.connect(self.on_load_finished)
        
        layout.addWidget(self.web_view, 1)  # stretch factor = 1，让浏览器占据更多空间
        
        # 紧凑的状态栏
        self.statusBar().setStyleSheet("font-size: 11px;")
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
        self.web_view.setUrl(QUrl("http://127.0.0.1:5000"))
        self.url_input.setText("http://127.0.0.1:5000")
    
    def update_url_bar(self, q):
        """Update URL bar when URL changes"""
        self.url_input.setText(q.toString())
    
    def on_load_finished(self, ok):
        """Handle load finished event"""
        if ok:
            self.statusBar().showMessage("加载完成")
        else:
            self.statusBar().showMessage("加载失败")


def main():
    # High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("PyQt6 WebBrowser")
    app.setOrganizationName("Demo")
    
    # 设置应用图标
    icon_path = resource_path("icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
