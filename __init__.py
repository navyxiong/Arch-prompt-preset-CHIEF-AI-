"""
ArchiPromptPreset - ComfyUI Custom Node
建筑提示词预设选择器，支持多时间场景（日景、清晨、黄昏、夜景、阴天、雨雪天）
"""

import os
import sys

# 获取当前目录
current_dir = os.path.dirname(os.path.realpath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 导入节点类和映射
from .archi_prompt_preset import (
    ArchiPromptPreset,
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS,
    __version__
)

# 导出 ComfyUI 所需的映射
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 节点加载信息
print(f"🔵 ArchiPromptPreset Node v{__version__} loaded successfully")
print(f"   Categories: Architecture")
print(f"   Time options: 日景, 清晨, 黄昏, 夜景, 阴天, 雨雪天")
