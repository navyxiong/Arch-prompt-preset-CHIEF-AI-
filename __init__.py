"""
ArchiPromptPreset - ComfyUI Node Package
建筑提示词预设选择器，支持为每个时间分类（日景/清晨/黄昏/夜景/阴天）独立选择效果
"""

from .archi_prompt_preset import ArchiPromptPreset

# ==============================================================================
# ComfyUI 节点注册（必须）
# ==============================================================================

# 节点类映射（用于 ComfyUI 内部识别和实例化）
NODE_CLASS_MAPPINGS = {
    "ArchiPromptPreset": ArchiPromptPreset,
}

# 节点显示名称映射（用于 ComfyUI 界面显示）
NODE_DISPLAY_NAME_MAPPINGS = {
    "ArchiPromptPreset": "🏢 Archi Prompt Preset",
}

# 可选：前端资源目录（如需自定义 JS/CSS 请取消注释并创建对应目录）
# WEB_DIRECTORY = "./web"

# 版本信息
__version__ = "1.2.0"

# 节点元数据（供 ComfyUI Manager 等工具使用）
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 加载成功提示（便于调试）
print(f"✅ Loaded ArchiPromptPreset v{__version__} - Multi-time selector with independent dropdowns")
