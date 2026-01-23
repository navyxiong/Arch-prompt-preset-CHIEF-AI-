"""
ArchiPromptPreset - ComfyUI Node Package
建筑提示词预设选择器，支持两级联动菜单（时间+效果）
"""

from .archi_prompt_preset import ArchiPromptPreset
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.realpath(__file__))

# 注册前端资源目录（关键！）
WEB_DIRECTORY = os.path.join(current_dir, "web")

NODE_CLASS_MAPPINGS = {
    "ArchiPromptPreset": ArchiPromptPreset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ArchiPromptPreset": "🏢 Archi Prompt Preset",
}

__version__ = "1.1.0"

print(f"🎯 Loaded ArchiPromptPreset v{__version__} - 支持两级联动菜单")
