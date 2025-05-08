#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
from typing import List, Tuple

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QFrame, QMessageBox, QSplitter, QTableWidget,
                           QTableWidgetItem, QHeaderView, QFileDialog)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

from src.gui.widgets import (CustomButton, CustomLabel, WinnerCard, DrawContainer,
                           NumberInputWidget, StatusWidget)
from src.models.lucky_draw_model import LuckyDrawModel

class MainWindow(QMainWindow):
    """抽奖程序主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化窗口属性
        self.setWindowTitle("幸运抽奖系统")
        self.setMinimumSize(1200, 800)
        
        # 初始化抽奖模型
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(script_dir, "data", "participants.csv")
        self.model = LuckyDrawModel(csv_path)
        
        # 抽奖状态
        self.is_drawing = False
        
        # 动画控制 - 使用简单的定时器
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_speed = 200  # 初始动画速度（毫秒）
        
        # 创建用户界面
        self.init_ui()
        
        # 更新状态信息
        self.update_status()
        
        # 显示欢迎信息
        self.display_welcome()
    
    def init_ui(self):
        """初始化用户界面"""
        # 创建中央部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 标题区域
        title_layout = QHBoxLayout()
        title = CustomLabel("幸运抽奖系统", self, is_title=True)
        title_layout.addStretch(1)
        title_layout.addWidget(title)
        title_layout.addStretch(1)
        main_layout.addLayout(title_layout)
        
        # 内容区域 - 使用分隔器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧控制面板
        left_panel = self.create_control_panel()
        
        # 右侧抽奖展示区域
        right_panel = self.create_draw_panel()
        
        # 添加到分隔器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 900])  # 设置初始分隔比例
        
        # 添加到主布局
        main_layout.addWidget(splitter, 1)
        
        # 底部区域 - 结果表格
        self.results_table = self.create_results_table()
        main_layout.addWidget(self.results_table)
    
    def create_control_panel(self) -> QWidget:
        """创建左侧控制面板"""
        panel = QFrame()
        panel.setObjectName("controlPanel")
        panel.setStyleSheet("""
            #controlPanel {
                background-color: #f8f8f8;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 控制区域标题
        control_title = CustomLabel("抽奖控制", panel)
        control_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(control_title)
        
        # 抽奖人数输入
        self.number_input = NumberInputWidget("本轮抽奖人数:", 1, 1, 100, panel)
        layout.addWidget(self.number_input)
        
        # 状态信息
        self.status_widget = StatusWidget(panel)
        layout.addWidget(self.status_widget)
        
        # 按钮区域
        buttons_layout = QHBoxLayout()
        
        # 开始抽奖按钮
        self.start_button = CustomButton("开始抽奖", panel, "primary")
        self.start_button.clicked.connect(self.start_draw)
        buttons_layout.addWidget(self.start_button)
        
        # 停止抽奖按钮
        self.stop_button = CustomButton("停止抽奖", panel, "danger")
        self.stop_button.clicked.connect(self.stop_draw)
        self.stop_button.setEnabled(False)
        buttons_layout.addWidget(self.stop_button)
        
        layout.addLayout(buttons_layout)
        
        # 重置按钮
        self.reset_button = CustomButton("重置抽奖", panel, "neutral")
        self.reset_button.clicked.connect(self.reset_draw)
        layout.addWidget(self.reset_button)
        
        # 导入名单按钮
        self.import_button = CustomButton("导入名单", panel, "neutral")
        self.import_button.clicked.connect(self.import_participants)
        layout.addWidget(self.import_button)
        
        # 帮助信息
        help_text = "提示: 点击'开始抽奖'后，系统将随机展示参与者，\n再点击'停止抽奖'确定本轮中奖人员。"
        help_label = CustomLabel(help_text, panel)
        help_label.setStyleSheet("""
            font-size: 14px;
            color: #666666;
            padding: 15px;
            background-color: #f0f0f0;
            border-radius: 10px;
        """)
        layout.addWidget(help_label)
        
        # 添加底部空间
        layout.addStretch(1)
        
        return panel
    
    def create_draw_panel(self) -> QWidget:
        """创建右侧抽奖展示区域"""
        panel = QFrame()
        panel.setObjectName("drawPanel")
        panel.setStyleSheet("""
            #drawPanel {
                background-color: #ffffff;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 抽奖展示区域标题
        draw_title = CustomLabel("抽奖展示区", panel)
        draw_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(draw_title)
        
        # 抽奖容器
        self.draw_container = DrawContainer(panel)
        layout.addWidget(self.draw_container, 1)
        
        return panel
    
    def create_results_table(self) -> QTableWidget:
        """创建结果表格"""
        table = QTableWidget(0, 3)  # 0行，3列
        table.setHorizontalHeaderLabels(["轮次", "部门", "姓名"])
        
        # 设置表格样式
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        
        # 设置表头
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        # 设置表格高度
        table.setMaximumHeight(200)
        
        # 设置交替行颜色
        table.setAlternatingRowColors(True)
        
        return table
    
    def update_status(self):
        """更新状态信息"""
        self.status_widget.update_status(
            self.model.current_round,
            self.model.get_remaining_count()
        )
    
    def display_welcome(self):
        """显示欢迎信息"""
        # 使用抽奖容器显示欢迎信息
        self.draw_container.clear()
        
        welcome_label = CustomLabel("欢迎使用幸运抽奖系统", self, is_title=True)
        welcome_label.setAlignment(Qt.AlignCenter)
        self.draw_container.layout.addWidget(welcome_label, 0, 0, 1, 4)
        
        instruction_label = CustomLabel("请设置抽奖人数并点击开始抽奖按钮", self)
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("font-size: 18px; color: #666666;")
        self.draw_container.layout.addWidget(instruction_label, 1, 0, 1, 4)
    
    def validate_input(self) -> bool:
        """验证用户输入"""
        try:
            count = self.number_input.value()
            if count <= 0:
                QMessageBox.warning(self, "输入错误", "抽奖人数必须大于0")
                return False
            
            if not self.model.can_draw(count):
                QMessageBox.warning(self, "输入错误", 
                                  f"剩余人数不足，当前只有{self.model.get_remaining_count()}人")
                return False
            
            return True
        except Exception as e:
            QMessageBox.warning(self, "输入错误", f"发生错误: {str(e)}")
            return False
    
    @pyqtSlot()
    def start_draw(self):
        """开始抽奖"""
        if not self.validate_input():
            return
        
        # 获取抽奖人数
        num_winners = self.number_input.value()
        
        # 更新界面状态
        self.is_drawing = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.reset_button.setEnabled(False)
        self.number_input.setEnabled(False)
        
        # 保存当前请求的中奖人数
        self.requested_winners = num_winners
        
        # 启动定时器实现滚动动画
        self.animation_speed = 150  # 初始150ms每次更新
        self.animation_timer.start(self.animation_speed)
    
    def update_animation(self):
        """更新抽奖动画（由定时器触发）- 简化版"""
        if not self.is_drawing:
            return
        
        # 获取随机参与者
        random_participants = self.model.get_random_names(self.requested_winners)
        if not random_participants:
            return
        
        # 更新UI显示 - 简单滚动效果
        self.draw_container.update_display(random_participants)
        
        # 动态调整动画速度
        if random.random() < 0.2:  # 有20%的概率改变速度
            # 在100-300ms之间变化速度
            self.animation_speed = random.randint(100, 300)
            self.animation_timer.setInterval(self.animation_speed)
    
    @pyqtSlot()
    def stop_draw(self):
        """停止抽奖"""
        if not self.is_drawing:
            return
        
        # 停止动画定时器
        self.animation_timer.stop()
        
        # 更新状态
        self.is_drawing = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(True)
        self.number_input.setEnabled(True)
        
        # 执行抽奖
        num_winners = self.requested_winners
        winners = self.model.draw(num_winners)
        
        # 显示中奖结果
        self.draw_container.show_winners(winners)
        
        # 更新结果表格
        self.update_results_table(winners)
        
        # 更新状态信息
        self.update_status()
        
        # 显示提示
        if winners:
            QMessageBox.information(self, "抽奖完成", 
                                  f"第{self.model.current_round}轮抽奖完成，共抽出{len(winners)}人")
    
    def update_results_table(self, winners: List[Tuple[str, str]]):
        """更新结果表格"""
        for department, name in winners:
            row_position = self.results_table.rowCount()
            self.results_table.insertRow(row_position)
            
            # 添加轮次
            round_item = QTableWidgetItem(f"第{self.model.current_round}轮")
            round_item.setTextAlignment(Qt.AlignCenter)
            self.results_table.setItem(row_position, 0, round_item)
            
            # 添加部门
            dept_item = QTableWidgetItem(department)
            self.results_table.setItem(row_position, 1, dept_item)
            
            # 添加姓名
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Arial", 10, QFont.Bold))
            name_item.setForeground(QColor("#2E7D32"))
            self.results_table.setItem(row_position, 2, name_item)
    
    @pyqtSlot()
    def reset_draw(self):
        """重置抽奖状态"""
        reply = QMessageBox.question(self, "确认重置", 
                                   "确定要重置抽奖状态吗？所有已抽奖记录将被清空。",
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 重置抽奖模型
            self.model.reset()
            
            # 清空结果表格
            self.results_table.setRowCount(0)
            
            # 显示欢迎信息
            self.display_welcome()
            
            # 更新状态信息
            self.update_status()
            
            QMessageBox.information(self, "重置完成", "抽奖状态已重置")
    
    def import_participants(self):
        """导入参与者名单"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择参与者名单", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            try:
                self.model.add_csv_path(file_path)
                self.model.load_participants()
                QMessageBox.information(self, "导入成功", "参与者名单已成功导入")
                self.update_status()
            except Exception as e:
                QMessageBox.critical(self, "导入失败", f"导入过程中发生错误: {str(e)}")