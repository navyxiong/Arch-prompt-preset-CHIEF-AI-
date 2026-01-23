import json
import os

class ArchiPromptPreset:
    """
    ComfyUI Node: ArchiPromptPreset
    建筑提示词预设选择器，支持为每个时间分类独立选择效果，内置前缀开关及自定义提示词输入。
    适配二级嵌套 JSON 结构：{"日景": {"风格1（冷调）": {...}}, ...}
    """

    FIXED_PREFIX = "Transform the image into a real-life photo according to the following requirements, strictly maintain the consistency of the image content, strictly maintain the consistency of the buildings and environment in the image, and do not change the shooting angle and composition of the image."

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        # 默认时间分类
        time_categories = ["日景", "清晨", "黄昏", "夜景", "阴天"]
        
        # 初始化每个时间的选项（默认为 ["无"]）
        time_options = {cat: ["无"] for cat in time_categories}
        
        # 从 JSON 加载实际风格选项
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data and isinstance(data, dict):
                        for category, styles in data.items():
                            if category in time_options and isinstance(styles, dict):
                                # 在该时间分类下添加具体风格（保持原有顺序）
                                style_list = list(styles.keys())
                                if style_list:
                                    time_options[category] = ["无"] + style_list
                                else:
                                    time_options[category] = ["无", "Error: Empty category"]
                    else:
                        time_options = {cat: ["无", "Error: Invalid JSON"] for cat in time_categories}
            except Exception as e:
                print(f"[ArchiPromptPreset] JSON Load Error: {e}")
                time_options = {cat: ["无", f"Error: {str(e)}"] for cat in time_categories}
        else:
            time_options = {cat: ["无", "Error: presets.json not found"] for cat in time_categories}
        
        return {
            "required": {
                "use_prefix": (["开", "关"], {
                    "default": "开", 
                    "tooltip": "开启后自动添加内置提示词前缀"
                }),
                "日景": (time_options["日景"], {
                    "default": "无",
                    "tooltip": "选择日景效果，选'无'则跳过此分类"
                }),
                "清晨": (time_options["清晨"], {
                    "default": "无",
                    "tooltip": "选择清晨效果，选'无'则跳过此分类"
                }),
                "黄昏": (time_options["黄昏"], {
                    "default": "无",
                    "tooltip": "选择黄昏效果，选'无'则跳过此分类"
                }),
                "夜景": (time_options["夜景"], {
                    "default": "无",
                    "tooltip": "选择夜景效果，选'无'则跳过此分类"
                }),
                "阴天": (time_options["阴天"], {
                    "default": "无",
                    "tooltip": "选择阴天效果，选'无'则跳过此分类"
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
    DESCRIPTION = "建筑提示词预设选择器（每个时间独立下拉选择，默认为无）"

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

    def process_prompt(self, use_prefix, 日景, 清晨, 黄昏, 夜景, 阴天, custom_prompt):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        # 确定用户选择了哪个时间和风格（按优先级：日景 > 清晨 > 黄昏 > 夜景 > 阴天）
        selected_time = None
        selected_style = None
        
        time_selections = {
            "日景": 日景,
            "清晨": 清晨,
            "黄昏": 黄昏,
            "夜景": 夜景,
            "阴天": 阴天
        }
        
        # 找到第一个非"无"的选择
        for time_cat, style in time_selections.items():
            if style != "无" and not style.startswith("Error:"):
                selected_time = time_cat
                selected_style = style
                break
        
        # 如果没有选择任何效果，返回空或仅自定义内容
        if selected_time is None:
            if custom_prompt and custom_prompt.strip():
                return (custom_prompt.strip(),)
            return ("",)
        
        selected_content = ""
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 二级嵌套结构访问：data[selected_time][selected_style]
                    if selected_time in data and isinstance(data[selected_time], dict):
                        if selected_style in data[selected_time]:
                            entry = data[selected_time][selected_style]
                        else:
                            print(f"[ArchiPromptPreset] Style '{selected_style}' not found in '{selected_time}'")
                            return (custom_prompt.strip() if custom_prompt else "",)
                    else:
                        print(f"[ArchiPromptPreset] Category '{selected_time}' not found in JSON")
                        return (custom_prompt.strip() if custom_prompt else "",)
                    
                    # 处理找到的内容
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
                return (custom_prompt.strip() if custom_prompt else "",)
        
        # 构建最终输出
        parts = []
        
        # 1. 添加前缀（如果开启）
        if use_prefix == "开":
            prefix = self.FIXED_PREFIX.strip()
            if prefix:
                parts.append(prefix)
        
        # 2. 添加预设内容（包含时间和风格信息）
        if selected_content:
            parts.append(selected_content.strip())
        
        # 3. 添加自定义提示词
        if custom_prompt and custom_prompt.strip():
            parts.append(custom_prompt.strip())
        
        # 组合（使用逗号+空格分隔）
        final_output = ", ".join(parts) if parts else ""
        
        return (final_output,)

# ==============================================================================
# ComfyUI 节点注册（必须包含，用于识别和映射）
# ==============================================================================
NODE_CLASS_MAPPINGS = {
    "ArchiPromptPreset": ArchiPromptPreset
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ArchiPromptPreset": "🏢 Archi Prompt Preset"
}

__version__ = "1.2.0"
print(f"✅ Loaded ArchiPromptPreset v{__version__} - Multi-time selector with independent dropdowns")
