#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFontDatabase
from src.gui.main_window import MainWindow

def main():
    """程序入口函数"""
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 设置应用程序图标和名称
    app.setApplicationName("幸运抽奖系统")
    # app.setWindowIcon(QIcon("assets/icon.png"))  # 如果有图标可以取消注释
    
    # 加载字体（如果需要特殊字体）
    # font_id = QFontDatabase.addApplicationFont("assets/fonts/some_font.ttf")
    
    # 设置样式表
    # with open("assets/styles/style.qss", "r") as f:
    #     app.setStyleSheet(f.read())
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    # 确保当前工作目录正确
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()