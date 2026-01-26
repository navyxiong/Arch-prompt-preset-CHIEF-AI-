"""
ArchiPromptPreset - ComfyUI Custom Node
建筑提示词预设选择器，支持多时间场景（日景、清晨、黄昏、夜景、阴天、雨雪天）
输出格式：prefix.custom_prompt.time_category.style.inner_prompt

GitHub: https://github.com/yourusername/ComfyUI-ArchiPromptPreset
"""

import os
import sys
from typing import Dict, Any

# 获取当前目录并添加到系统路径
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

# 导出 ComfyUI 所需的映射（必须）
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 节点加载信息
print(f"🔵 ArchiPromptPreset Node v{__version__} loaded successfully")
print(f"   Category: Architecture")
print(f"   Output format: prefix.custom_prompt.time.style.inner_prompt")
print(f"   Time options: 日景, 清晨, 黄昏, 夜景, 阴天, 雨雪天")
