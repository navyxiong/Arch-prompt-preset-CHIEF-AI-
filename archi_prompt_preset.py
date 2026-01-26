import json
import os
from typing import Dict, Any, Tuple, Optional

class ArchiPromptPreset:
    """
    ComfyUI Node: ArchiPromptPreset
    建筑提示词预设选择器，支持为每个时间分类独立选择效果，内置前缀开关及自定义提示词输入。
    适配二级嵌套 JSON 结构：{"日景": {"风格1（冷调）": {...}}, ...}
    
    输出格式：prefix.custom_prompt.time_category.style.inner_prompt
    注意：inner_prompt 从 presets.json 中提取，确保不会被 prefix 覆盖
    
    GitHub Repository: https://github.com/yourusername/ComfyUI-ArchiPromptPreset
    Version: 2.3.0
    """

    FIXED_PREFIX: str = (
        "Transform the image into a real-life photo according to the following requirements, "
        "strictly maintain the consistency of the image content, strictly maintain the consistency "
        "of the buildings and environment in the image, and do not change the shooting angle and "
        "composition of the image."
    )

    def __init__(self) -> None:
        """初始化节点"""
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """定义节点的输入参数和配置"""
        current_dir: str = os.path.dirname(os.path.realpath(__file__))
        json_path: str = os.path.join(current_dir, "presets.json")
        
        # 时间分类定义
        time_categories: list[str] = ["日景", "清晨", "黄昏", "夜景", "阴天", "雨雪天"]
        
        # 初始化每个时间的选项（默认为 ["无"]）
        time_options: Dict[str, list[str]] = {cat: ["无"] for cat in time_categories}
        
        # 从 JSON 加载实际风格选项
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data: Any = json.load(f)
                    if data and isinstance(data, dict):
                        for category, styles in data.items():
                            if category in time_options and isinstance(styles, dict):
                                # 在该时间分类下添加具体风格（保持原有顺序）
                                style_list: list[str] = list(styles.keys())
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
                "雨雪天": (time_options["雨雪天"], {
                    "default": "无",
                    "tooltip": "选择雨雪天效果，选'无'则跳过此分类"
                }),
                "custom_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "在此输入自定义提示词（可选），将追加到预设之后...",
                    "tooltip": "自定义提示词，将以英文符号.间隔追加到prefix之后"
                }),
            }
        }

    RETURN_TYPES: tuple[str] = ("STRING",)
    RETURN_NAMES: tuple[str] = ("final_prompt",)
    OUTPUT_TOOLTIPS: tuple[str] = ("最终提示词字符串，格式：prefix.custom_prompt.time.style.inner_prompt",)
    
    FUNCTION: str = "process_prompt"
    CATEGORY: str = "Architecture"
    DESCRIPTION: str = "建筑提示词预设选择器，输出按指定顺序用.连接的字符串，inner_prompt从JSON提取"

    def extract_all_text(self, data: Any) -> list[str]:
        """递归提取字典中所有的字符串值"""
        texts: list[str] = []
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

    def process_prompt(self, use_prefix: str, 日景: str, 清晨: str, 黄昏: str, 
                      夜景: str, 阴天: str, 雨雪天: str, custom_prompt: str) -> Tuple[str]:
        """
        处理用户选择，生成按指定顺序用"."连接的提示词字符串
        
        输出顺序：prefix → custom_prompt → time_category → style → inner_prompt
        空值将被跳过，避免多余的"."符号
        
        Args:
            use_prefix: 是否使用前缀 ("开" 或 "关")
            日景: 日景选项
            清晨: 清晨选项
            黄昏: 黄昏选项
            夜景: 夜景选项
            阴天: 阴天选项
            雨雪天: 雨雪天选项
            custom_prompt: 自定义提示词
            
        Returns:
            tuple: 包含单个字符串的元组，格式为 prefix.custom_prompt.time.style.inner_prompt
        """
        current_dir: str = os.path.dirname(os.path.realpath(__file__))
        json_path: str = os.path.join(current_dir, "presets.json")
        
        # 确定用户选择的时间和风格（按优先级：日景 > 清晨 > 黄昏 > 夜景 > 阴天 > 雨雪天）
        selected_time: Optional[str] = None
        selected_style: Optional[str] = None
        
        time_selections: Dict[str, str] = {
            "日景": 日景,
            "清晨": 清晨,
            "黄昏": 黄昏,
            "夜景": 夜景,
            "阴天": 阴天,
            "雨雪天": 雨雪天
        }
        
        # 找到第一个非"无"的选择
        for time_cat, style in time_selections.items():
            if style != "无" and not style.startswith("Error:"):
                selected_time = time_cat
                selected_style = style
                break
        
        # 初始化组件列表，按指定顺序添加
        components: list[str] = []
        
        # 1. 添加前缀（如果开启）
        if use_prefix == "开":
            prefix_text: str = self.FIXED_PREFIX.strip()
            if prefix_text:
                components.append(prefix_text)
        
        # 2. 添加自定义提示词（如果存在）
        custom_text: str = custom_prompt.strip() if custom_prompt else ""
        if custom_text:
            components.append(custom_text)
        
        # 3-5. 处理时间和风格相关的内容
        if selected_time is not None:
            # 3. 添加时间分类
            components.append(selected_time)
            
            # 4. 添加风格名称
            if selected_style:
                components.append(selected_style)
            
            # 5. 加载并添加内嵌提示词（关键修复）
            inner_prompt_text: str = self._load_inner_prompt(
                json_path, selected_time, selected_style
            )
            if inner_prompt_text:
                components.append(inner_prompt_text)
        
        # 用 "." 连接所有组件
        final_output: str = ".".join(components)
        
        return (final_output,)
    
    def _load_inner_prompt(self, json_path: str, time_cat: str, style: str) -> str:
        """
        从 presets.json 加载指定时间分类和风格的内嵌提示词
        
        Args:
            json_path: JSON文件路径
            time_cat: 时间分类
            style: 风格名称
            
        Returns:
            str: 内嵌提示词内容，加载失败返回空字符串
        """
        if not os.path.exists(json_path):
            return ""
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data: Any = json.load(f)
                
                # 验证数据结构
                if time_cat not in data or not isinstance(data[time_cat], dict):
                    print(f"[ArchiPromptPreset] Category '{time_cat}' not found or invalid in JSON")
                    return ""
                
                if style not in data[time_cat]:
                    print(f"[ArchiPromptPreset] Style '{style}' not found in category '{time_cat}'")
                    return ""
                
                entry = data[time_cat][style]
                
                # 提取内嵌提示词内容
                if isinstance(entry, str):
                    return entry.strip()
                elif isinstance(entry, dict):
                    # 优先查找 "prompt" 字段
                    if "prompt" in entry:
                        return entry["prompt"].strip()
                    else:
                        # 递归提取所有文本并拼接
                        all_texts = self.extract_all_text(entry)
                        return ", ".join(all_texts) if all_texts else ""
                else:
                    print(f"[ArchiPromptPreset] Invalid entry type for '{time_cat}.{style}'")
                    return ""
                    
        except Exception as e:
            print(f"[ArchiPromptPreset] Error loading inner prompt: {e}")
            return ""


# ==============================================================================
# ComfyUI 节点注册（必须包含，用于识别和映射）
# ==============================================================================
NODE_CLASS_MAPPINGS: Dict[str, type] = {
    "ArchiPromptPreset": ArchiPromptPreset
}

NODE_DISPLAY_NAME_MAPPINGS: Dict[str, str] = {
    "ArchiPromptPreset": "🏢 Archi Prompt Preset"
}

__version__: str = "2.3.0"
print(f"✅ Loaded ArchiPromptPreset v{__version__} - Fixed inner_prompt extraction")
