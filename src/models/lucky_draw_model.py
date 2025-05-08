#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import random
from typing import List, Tuple, Dict, Optional

class LuckyDrawModel:
    """抽奖数据模型，处理抽奖逻辑和数据"""
    
    def __init__(self, csv_path: str):
        """初始化抽奖管理器
        
        Args:
            csv_path: 参与者CSV文件路径
        """
        self.csv_path = csv_path
        self.participants = []  # 所有参与者
        self.remaining = []     # 剩余未抽中参与者
        self.winners = []       # 已抽中参与者
        self.current_round = 0  # 当前轮数
        
        # 加载参与者数据
        self.load_participants()
    
    def load_participants(self) -> bool:
        """从CSV文件加载参与者数据
        
        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            if not os.path.exists(self.csv_path):
                return False
            
            df = pd.read_csv(self.csv_path)
            
            # 检查必要的列是否存在
            if 'department' not in df.columns or 'name' not in df.columns:
                return False
            
            # 将数据转换为列表格式 [(department, name), ...]
            self.participants = list(zip(df['department'].tolist(), df['name'].tolist()))
            self.remaining = self.participants.copy()
            return True
        except Exception as e:
            print(f"加载参与者数据出错: {e}")
            return False
    
    def reset(self) -> None:
        """重置抽奖状态，恢复所有候选人"""
        self.remaining = self.participants.copy()
        self.winners = []
        self.current_round = 0
    
    def can_draw(self, num_winners: int) -> bool:
        """检查是否可以进行当前轮抽奖
        
        Args:
            num_winners: 当前轮要抽取的人数
            
        Returns:
            bool: 如果剩余人数足够，返回True，否则返回False
        """
        return len(self.remaining) >= num_winners
    
    def draw(self, num_winners: int) -> List[Tuple[str, str]]:
        """执行抽奖
        
        Args:
            num_winners: 要抽取的获奖者数量
            
        Returns:
            List[Tuple[str, str]]: 包含部门和姓名的获奖者列表
        """
        if not self.can_draw(num_winners):
            return []
        
        # 从剩余参与者中随机抽取
        current_winners = random.sample(self.remaining, num_winners)
        
        # 更新剩余参与者和获奖者列表
        for winner in current_winners:
            self.remaining.remove(winner)
            self.winners.append(winner)
        
        # 更新轮数
        self.current_round += 1
        
        # 保存本轮结果
        self.save_results(current_winners)
        
        return current_winners
    
    def save_results(self, winners: List[Tuple[str, str]]) -> None:
        """保存抽奖结果到CSV文件
        
        Args:
            winners: 当前轮的获奖者列表
        """
        output_dir = os.path.join(os.path.dirname(self.csv_path), "..", "..", "output")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f"round_{self.current_round}.csv")
        
        # 创建DataFrame并保存
        df = pd.DataFrame(winners, columns=['department', 'name'])
        df.to_csv(output_path, index=False, encoding='utf-8')
    
    def get_remaining_count(self) -> int:
        """获取剩余未抽奖人数
        
        Returns:
            int: 剩余人数
        """
        return len(self.remaining)
    
    def get_random_names(self, count: int) -> List[Tuple[str, str]]:
        """获取随机的参与者，用于动画展示
        
        Args:
            count: 要获取的随机参与者数量
            
        Returns:
            List[Tuple[str, str]]: 随机参与者列表 (部门, 姓名)
        """
        if not self.remaining or count <= 0:
            return []
        
        # 从剩余参与者中随机抽取
        sample_size = min(count, len(self.remaining))
        return random.sample(self.remaining, sample_size)