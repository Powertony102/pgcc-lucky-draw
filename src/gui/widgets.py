#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QPushButton, QLabel, QVBoxLayout, QWidget, 
                            QFrame, QGraphicsDropShadowEffect, QSizePolicy,
                            QSpinBox, QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QFont, QColor, QCursor, QPalette, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, pyqtProperty, QEasingCurve

class CustomButton(QPushButton):
    def __init__(self, text, parent=None, button_type="primary"):
        super().__init__(text, parent)
        
        # 基于类型设置不同样式
        if button_type == "primary":
            bg_color = "#4CAF50"
            hover_color = "#45a049"
            pressed_color = "#357a38"
        elif button_type == "danger":
            bg_color = "#f44336"
            hover_color = "#d32f2f"
            pressed_color = "#b71c1c"
        elif button_type == "neutral":
            bg_color = "#9e9e9e"
            hover_color = "#757575"
            pressed_color = "#616161"
        else:  # 默认为主要按钮
            bg_color = "#4CAF50"
            hover_color = "#45a049"
            pressed_color = "#357a38"
            
        # 使用更现代化的样式
        self.setStyleSheet(f"""
            QPushButton {{
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: {bg_color};
                border-radius: 8px;
                padding: 12px 20px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # 添加按钮点击动画效果
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setBlurRadius(15)
        self._shadow.setColor(QColor(0, 0, 0, 80))
        self._shadow.setOffset(0, 2)
        self.setGraphicsEffect(self._shadow)
        
    def enterEvent(self, event):
        # 鼠标悬停时放大效果
        self.anim = QPropertyAnimation(self, b"size")
        self.anim.setDuration(100)
        self.anim.setEndValue(QSize(int(self.width() * 1.05), int(self.height() * 1.05)))
        self.anim.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        # 鼠标离开时恢复原大小
        self.anim = QPropertyAnimation(self, b"size")
        self.anim.setDuration(100)
        self.anim.setEndValue(QSize(int(self.width() / 1.05), int(self.height() / 1.05)))
        self.anim.start()
        super().leaveEvent(event)
        
    def sizeHint(self):
        return QSize(200, 50)

class CustomLabel(QLabel):
    def __init__(self, text, parent=None, is_winner=False, is_title=False):
        super().__init__(text, parent)
        
        if is_title:
            # 标题样式
            self.setStyleSheet("""
                font-size: 32px;
                font-weight: bold;
                color: #2E7D32;
                padding: 10px;
            """)
            self.setAlignment(Qt.AlignCenter)
            
        elif is_winner:
            # 中奖者标签使用更大、更突出的样式
            self.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                color: #2E7D32;
                padding: 10px;
                background-color: #E8F5E9;
                border-radius: 10px;
                border: 2px solid #4CAF50;
            """)
            self.setAlignment(Qt.AlignCenter)
            
            # 添加阴影效果
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setColor(QColor(0, 0, 0, 60))
            shadow.setOffset(0, 3)
            self.setGraphicsEffect(shadow)
        else:
            # 普通标签样式
            self.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #333333;
                padding: 5px;
            """)

class WinnerCard(QFrame):
    """获奖者卡片 - 简化版，没有复杂动画"""
    def __init__(self, department, name, parent=None):
        super().__init__(parent)
        self.department = department
        self.name = name
        self.initUI()
        
    def initUI(self):
        self.setObjectName("winnerCard")
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)
        
        # 精美的获奖者卡片样式
        self.setStyleSheet("""
            #winnerCard {
                background-color: #f0faf0;
                border-radius: 15px;
                border: 2px solid #4CAF50;
                margin: 8px;
            }
            #winnerCard:hover {
                background-color: #e0f2e0;
                border: 2px solid #2E7D32;
            }
        """)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        # 布局
        layout = QVBoxLayout(self)
        
        # 部门标签
        dept_label = QLabel(self.department)
        dept_label.setAlignment(Qt.AlignCenter)
        dept_label.setFont(QFont("Arial", 14))
        dept_label.setStyleSheet("color: #666666;")
        
        # 获奖者名字标签
        name_label = QLabel(self.name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 20, QFont.Bold))
        name_label.setStyleSheet("color: #2E7D32; letter-spacing: 1px;")
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout.addWidget(dept_label)
        layout.addWidget(name_label)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 固定卡片尺寸
        self.setMinimumSize(200, 140)
        self.setMaximumSize(200, 140)

class DrawContainer(QWidget):
    """抽奖动画和结果展示容器 - 简化版，只有基本滚动效果"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        
        # 设置边距和间距
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # 增加整体样式
        self.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 20px;
        """)
        
        # 添加整体阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
    def update_display(self, participants):
        """更新抽奖展示 - 简单的滚动效果"""
        # 清空当前布局
        self.clear()
        
        # 没有数据时显示提示信息
        if not participants:
            empty_label = CustomLabel("开始抽奖后将在此处展示候选人", self)
            empty_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(empty_label, 0, 0, 1, 4)
            return
        
        # 计算行列数 (最多4列)
        cols = min(4, len(participants))
        rows = (len(participants) + cols - 1) // cols
        
        # 添加参与者卡片
        for i, (department, name) in enumerate(participants):
            row = i // cols
            col = i % cols
            
            # 创建卡片
            card = WinnerCard(department, name, self)
            self.layout.addWidget(card, row, col)
    
    def show_winners(self, winners):
        """显示中奖人员"""
        # 先清空当前布局
        self.clear()
        
        # 添加标题
        title = CustomLabel("🎉 恭喜以下人员中奖 🎉", self, is_title=True)
        self.layout.addWidget(title, 0, 0, 1, 4)
        
        # 没有中奖者时显示提示
        if not winners:
            empty_label = CustomLabel("没有中奖人员", self)
            empty_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(empty_label, 1, 0, 1, 4)
            return
        
        # 计算行列数 (最多4列)
        cols = min(4, len(winners))
        rows = (len(winners) + cols - 1) // cols
        
        # 添加中奖者卡片
        for i, (department, name) in enumerate(winners):
            row = (i // cols) + 1  # +1是因为第0行是标题
            col = i % cols
            
            # 创建卡片
            card = WinnerCard(department, name, self)
            self.layout.addWidget(card, row, col)
        
    def clear(self):
        """清除所有展示项目"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def set_animation_level(self, level):
        """设置动画强度级别 - 为了兼容保留此方法但不做实际操作"""
        pass

class NumberInputWidget(QWidget):
    def __init__(self, label_text="抽奖人数:", default_value=1, min_value=1, max_value=100, parent=None):
        super().__init__(parent)
        self.initUI(label_text, default_value, min_value, max_value)
        
    def initUI(self, label_text, default_value, min_value, max_value):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标签
        self.label = QLabel(label_text)
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: #2E7D32; font-weight: bold;")
        
        # 数字输入框
        self.number_input = QSpinBox()
        self.number_input.setValue(default_value)
        self.number_input.setMinimum(min_value)
        self.number_input.setMaximum(max_value)
        self.number_input.setFont(QFont("Arial", 14))
        self.number_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                color: #2E7D32;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background-color: #E8F5E9;
                border-radius: 3px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #4CAF50;
            }
        """)
        self.number_input.setFixedWidth(100)
        
        # 添加小部件到布局
        layout.addWidget(self.label)
        layout.addWidget(self.number_input)
        layout.addStretch()
        
    def value(self):
        return self.number_input.value()
        
    def setValue(self, value):
        self.number_input.setValue(value)
        
    def setEnabled(self, enabled):
        self.number_input.setEnabled(enabled)

class StatusWidget(QWidget):
    """状态信息展示组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout(self)
        
        # 轮次信息
        self.round_label = QLabel("当前轮数:")
        self.round_label.setFont(QFont("Arial", 14))
        self.round_label.setStyleSheet("color: #333333; font-weight: bold;")
        
        self.round_value = QLabel("0")
        self.round_value.setFont(QFont("Arial", 14))
        self.round_value.setStyleSheet("color: #2E7D32; font-weight: bold;")
        
        # 剩余人数信息
        self.remaining_label = QLabel("剩余人数:")
        self.remaining_label.setFont(QFont("Arial", 14))
        self.remaining_label.setStyleSheet("color: #333333; font-weight: bold;")
        
        self.remaining_value = QLabel("0")
        self.remaining_value.setFont(QFont("Arial", 14))
        self.remaining_value.setStyleSheet("color: #2E7D32; font-weight: bold;")
        
        # 添加到布局
        layout.addWidget(self.round_label)
        layout.addWidget(self.round_value)
        layout.addSpacing(30)
        layout.addWidget(self.remaining_label)
        layout.addWidget(self.remaining_value)
        layout.addStretch()
        
        # 设置整体样式
        self.setStyleSheet("""
            background-color: #f5f5f5;
            border-radius: 10px;
            padding: 10px;
        """)
        
    def update_status(self, round_num, remaining_count):
        """更新状态信息"""
        self.round_value.setText(str(round_num))
        self.remaining_value.setText(str(remaining_count))