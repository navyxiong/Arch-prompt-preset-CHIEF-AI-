"""
ArchiPromptPreset - ComfyUI Node Package
建筑提示词预设选择器，支持两级菜单（时间+效果）、内置前缀开关及自定义提示词输入
"""

from .archi_prompt_preset import ArchiPromptPreset

# ==============================================================================
# ComfyUI 节点注册（必须）
# ==============================================================================

# 节点类映射（用于 ComfyUI 内部识别）
NODE_CLASS_MAPPINGS = {
    "ArchiPromptPreset": ArchiPromptPreset,
}

# 节点显示名称映射（用于界面显示）
NODE_DISPLAY_NAME_MAPPINGS = {
    "ArchiPromptPreset": "🏢 Archi Prompt Preset",
}

# 可选：前端资源目录（如果有自定义 JS/CSS）
# WEB_DIRECTORY = "./web"

# 可选：版本信息
__version__ = "1.0.0"

# 可选：节点列表导出（供 ComfyUI Manager 等工具使用）
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 打印加载信息（可选，用于调试）
print(f"🎯 Loaded ArchiPromptPreset v{__version__} - Architecture Prompt Preset Selector")
