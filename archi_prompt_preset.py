import json
import os

class ArchiPromptPreset:
    """
    ComfyUI Node: archi_prompt_preset
    Loads keys from presets.json and adds a fixed built-in prefix.
    Supports both simple "prompt" key and nested dictionary structures.
    """

    # ==============================================================================
    # 🛠️ [配置区] 内置固定提示词
    # ==============================================================================
    FIXED_PREFIX = "Transform the image into a real-life photo according to the following requirements, strictly maintain the consistency of the image content, strictly maintain the consistency of the buildings and environment in the image, and do not change the shooting angle and composition of the image."

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        preset_keys = ["Error: presets.json not found"]
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        preset_keys = sorted(list(data.keys()))
                    else:
                        preset_keys = ["Error: JSON is empty"]
            except Exception as e:
                # 这里会捕捉 JSON 语法错误并显示在菜单里
                print(f"[ArchiPromptPreset] JSON Load Error: {e}")
                preset_keys = [f"Error: {str(e)}"]
        
        return {
            "required": {
                "preset_key": (preset_keys, ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    
    FUNCTION = "process_prompt"
    CATEGORY = "Architecture"

    # 辅助函数：递归提取字典中所有的字符串值
    def extract_all_text(self, data):
        texts = []
        if isinstance(data, dict):
            for value in data.values():
                texts.extend(self.extract_all_text(value))
        elif isinstance(data, list):
            for item in data:
                texts.extend(self.extract_all_text(item))
        elif isinstance(data, str):
            # 排除空字符串
            if data.strip():
                texts.append(data.strip())
        return texts

    def process_prompt(self, preset_key):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        selected_content = ""
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 检查是不是报错信息
                    if preset_key.startswith("Error:"):
                        print(f"[ArchiPromptPreset] Cannot process prompt because of JSON error.")
                        return (self.FIXED_PREFIX,)

                    if preset_key in data:
                        entry = data[preset_key]
                        
                        # logic update: 智能判断
                        if isinstance(entry, str):
                            selected_content = entry
                        elif isinstance(entry, dict):
                            # 1. 优先找 "prompt" 字段
                            if "prompt" in entry:
                                selected_content = entry["prompt"]
                            else:
                                # 2. 如果没有 prompt 字段，就把里面所有的值拼起来（适应你的JSON结构）
                                all_texts = self.extract_all_text(entry)
                                selected_content = ", ".join(all_texts)
                                
                    else:
                        print(f"[ArchiPromptPreset] Key '{preset_key}' not found.")
            except Exception as e:
                print(f"[ArchiPromptPreset] Runtime Error: {e}")
        
        # 拼接逻辑
        prefix = self.FIXED_PREFIX.strip()
        content = selected_content.strip()
        
        final_output = ""
        if prefix and content:
            final_output = f"{prefix}, {content}"
        elif prefix:
            final_output = prefix
        else:
            final_output = content
            
        return (final_output,)

NODE_CLASS_MAPPINGS = {
    "ArchiPromptPreset": ArchiPromptPreset
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ArchiPromptPreset": "archi_prompt_preset"
}
