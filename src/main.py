#!/usr/bin/env python3
"""
PyQt6 Demo Application
A simple cross-platform GUI application
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("PyQt6 Demo App")
        self.setMinimumSize(QSize(400, 300))
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title label
        title = QLabel("🎉 PyQt6 跨平台应用演示")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Info text
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText("点击按钮查看系统信息...")
        layout.addWidget(self.text_edit)
        
        # Buttons
        btn_info = QPushButton("📊 显示系统信息")
        btn_info.clicked.connect(self.show_info)
        layout.addWidget(btn_info)
        
        btn_about = QPushButton("ℹ️ 关于")
        btn_about.clicked.connect(self.show_about)
        layout.addWidget(btn_about)
        
        btn_quit = QPushButton("❌ 退出")
        btn_quit.clicked.connect(self.close)
        layout.addWidget(btn_quit)
    
    def show_info(self):
        """Show system information"""
        import platform
        import sys
        
        info = f"""系统信息:
━━━━━━━━━━━━━━━━━━━━━━━━
操作系统: {platform.system()}
系统版本: {platform.version()}
架构: {platform.machine()}
处理器: {platform.processor()}
Python版本: {platform.python_version()}
━━━━━━━━━━━━━━━━━━━━━━━━
可执行文件路径: {sys.executable}
当前工作目录: {sys.path[0] if sys.path else 'N/A'}
"""
        self.text_edit.setText(info)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "关于",
            "PyQt6 Demo App v1.0.0\n\n"
            "一个简单的跨平台GUI应用程序演示\n"
            "支持 Windows, macOS (Intel & Apple Silicon), Linux\n\n"
            "使用 PyQt6 构建"
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用Fusion风格，跨平台一致性更好
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
