import json
import os

class ArchiPromptPreset:
    """
    ComfyUI Node: ArchiPromptPreset
    建筑提示词预设选择器，支持两级菜单（时间+效果）、内置前缀开关及自定义提示词输入。
    适配二级嵌套 JSON 结构：{"日景": {"风格1（冷调）": {...}}, ...}
    """

    FIXED_PREFIX = "Transform the image into a real-life photo according to the following requirements, strictly maintain the consistency of the image content, strictly maintain the consistency of the buildings and environment in the image, and do not change the shooting angle and composition of the image."

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        # 默认时间分类（第一级）
        time_categories = ["日景", "清晨", "黄昏", "夜景", "阴天"]
        style_effects = ["请先选择时间分类"]
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data and isinstance(data, dict):
                        # 二级嵌套结构：收集所有分类下的所有风格
                        all_styles = set()
                        for category, styles in data.items():
                            if isinstance(styles, dict):
                                for style_key in styles.keys():
                                    all_styles.add(style_key)
                        
                        if all_styles:
                            style_effects = sorted(list(all_styles))
                        else:
                            style_effects = ["Error: No valid styles found"]
                    else:
                        style_effects = ["Error: JSON format invalid"]
            except Exception as e:
                print(f"[ArchiPromptPreset] JSON Load Error: {e}")
                style_effects = [f"Error: {str(e)}"]
        else:
            style_effects = ["Error: presets.json not found"]
        
        return {
            "required": {
                "use_prefix": (["开", "关"], {
                    "default": "开", 
                    "tooltip": "开启后自动添加内置提示词前缀"
                }),
                "time_category": (time_categories, {
                    "default": "日景", 
                    "tooltip": "选择时间分类（第一级）"
                }),
                "style_effect": (style_effects, {
                    "tooltip": "选择具体效果（第二级），需与上方时间对应"
                }),
                "custom_prompt": ("STRING", {
                    "multiline": True, 
                    "default": "", 
                    "placeholder": "在此输入自定义提示词（可选），将追加到预设之后...",
                    "tooltip": "自定义追加的提示词内容"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    OUTPUT_TOOLTIPS = ("组合后的完整提示词（前缀+预设+自定义）",)
    
    FUNCTION = "process_prompt"
    CATEGORY = "Architecture"
    DESCRIPTION = "建筑提示词预设选择器（两级菜单：时间+效果，支持前缀开关与自定义输入）"

    def extract_all_text(self, data):
        """递归提取字典中所有的字符串值"""
        texts = []
        if isinstance(data, dict):
            for value in data.values():
                texts.extend(self.extract_all_text(value))
        elif isinstance(data, list):
            for item in data:
                texts.extend(self.extract_all_text(item))
        elif isinstance(data, str):
            if data.strip():
                texts.append(data.strip())
        return texts

    def process_prompt(self, use_prefix, time_category, style_effect, custom_prompt):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        selected_content = ""
        
        # 检查是否为错误状态
        if style_effect.startswith("Error:"):
            print(f"[ArchiPromptPreset] Cannot process prompt: {style_effect}")
            return (custom_prompt.strip() if custom_prompt else "",)
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 二级嵌套结构访问：data[time_category][style_effect]
                    if time_category in data and isinstance(data[time_category], dict):
                        if style_effect in data[time_category]:
                            entry = data[time_category][style_effect]
                        else:
                            print(f"[ArchiPromptPreset] Style '{style_effect}' not found in category '{time_category}'")
                            entry = None
                    else:
                        # 回退：尝试扁平结构（兼容旧格式）
                        flat_key = time_category + style_effect
                        if flat_key in data:
                            entry = data[flat_key]
                            print(f"[ArchiPromptPreset] Warning: Using legacy flat key '{flat_key}'")
                        else:
                            print(f"[ArchiPromptPreset] Category '{time_category}' not found or invalid structure")
                            entry = None
                    
                    # 处理找到的内容
                    if entry is not None:
                        if isinstance(entry, str):
                            selected_content = entry
                        elif isinstance(entry, dict):
                            # 优先找 "prompt" 字段
                            if "prompt" in entry:
                                selected_content = entry["prompt"]
                            else:
                                # 递归提取所有文本并拼接
                                all_texts = self.extract_all_text(entry)
                                selected_content = ", ".join(all_texts)
                                
            except Exception as e:
                print(f"[ArchiPromptPreset] Runtime Error: {e}")
                selected_content = ""
        
        # 构建最终输出
        parts = []
        
        # 1. 添加前缀（如果开启）
        if use_prefix == "开":
            prefix = self.FIXED_PREFIX.strip()
            if prefix:
                parts.append(prefix)
        
        # 2. 添加预设内容
        if selected_content:
            parts.append(selected_content.strip())
        
        # 3. 添加自定义提示词
        if custom_prompt and custom_prompt.strip():
            parts.append(custom_prompt.strip())
        
        # 组合（使用逗号+空格分隔）
        final_output = ", ".join(parts) if parts else ""
        
        return (final_output,)

NODE_CLASS_MAPPINGS = {
    "ArchiPromptPreset": ArchiPromptPreset
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ArchiPromptPreset": "Archi Prompt Preset"
}
