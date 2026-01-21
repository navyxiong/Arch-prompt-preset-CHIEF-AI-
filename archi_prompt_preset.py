import json
import os

class ArchiPromptPreset:
    """
    ComfyUI Node: archi_prompt_preset
    Loads keys from presets.json and adds a fixed built-in prefix.
    """

    # ==============================================================================
    # 🛠️ [配置区] 内置固定提示词 (Built-in Fixed Prompt)
    # 修改这里的字符串，它将永远出现在输出文本的最前面。
    # ==============================================================================
    FIXED_PREFIX = "Transform the image into a real-life photo according to the following requirements, strictly maintain the consistency of the image content, strictly maintain the consistency of the buildings and environment in the image, and do not change the shooting angle and composition of the image."

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点输入：读取 presets.json 并生成下拉菜单
        """
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        # 默认列表
        preset_keys = ["Error: presets.json not found"]
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        # 排序 Key
                        preset_keys = sorted(list(data.keys()))
                    else:
                        preset_keys = ["Error: JSON is empty"]
            except Exception as e:
                print(f"[ArchiPromptPreset] JSON Load Error: {e}")
                preset_keys = [f"Error: {str(e)}"]
        
        return {
            "required": {
                # 下拉菜单：界面上显示的 Keys
                "preset_key": (preset_keys, ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    
    FUNCTION = "process_prompt"
    # 分类路径，你可以根据喜好修改，比如改成 "Architecture"
    CATEGORY = "Architecture"

    def process_prompt(self, preset_key):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        selected_content = ""
        
        # 1. 读取 JSON 内容
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if preset_key in data:
                        entry = data[preset_key]
                        if isinstance(entry, dict):
                            selected_content = entry.get("prompt", "")
                        elif isinstance(entry, str):
                            selected_content = entry
                    else:
                        print(f"[ArchiPromptPreset] Key '{preset_key}' not found.")
            except Exception as e:
                print(f"[ArchiPromptPreset] Runtime Error: {e}")
        
        # 2. 拼接逻辑
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

# 节点注册映射
NODE_CLASS_MAPPINGS = {
    "ArchiPromptPreset": ArchiPromptPreset
}

# 这里决定了在 ComfyUI 界面上显示的名字
NODE_DISPLAY_NAME_MAPPINGS = {
    "ArchiPromptPreset": "archi_prompt_preset"
}
