import json
import os

class JsonPromptLoader:
    """
    A ComfyUI custom node that loads prompts from a JSON file 
    and prepends a fixed prefix string.
    """
    
    # ============================================================
    # [CONFIGURATION]
    # Edit this string to change the fixed prefix for all outputs.
    # ============================================================
    FIXED_PREFIX = "Transform the image into a real-life photo according to the following requirements, strictly maintain the consistency of the image content, strictly maintain the consistency of the buildings and environment in the image, and do not change the shooting angle and composition of the image."
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input ports of the node.
        Reads keys from 'presets.json' to populate the dropdown menu.
        """
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        # Default option if JSON is missing or empty
        preset_keys = ["None"]
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        # Sort keys to make the list easier to read
                        preset_keys = sorted(list(data.keys()))
            except Exception as e:
                print(f"[JsonPromptLoader] Error loading presets.json: {e}")
        else:
            print(f"[JsonPromptLoader] Warning: presets.json not found at {json_path}")
        
        return {
            "required": {
                "preset": (preset_keys, ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt_text",)
    FUNCTION = "load_prompt"
    CATEGORY = "Architecture Nodes"

    def load_prompt(self, preset):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(current_dir, "presets.json")
        
        selected_prompt = ""
        
        # Load the selected prompt from JSON
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if preset in data:
                        # Support both direct string and object with "prompt" key
                        entry = data[preset]
                        if isinstance(entry, dict):
                            selected_prompt = entry.get("prompt", "")
                        elif isinstance(entry, str):
                            selected_prompt = entry
                        
                        # Logging for debugging
                        # print(f"[JsonPromptLoader] Selected: {preset}")
            except Exception as e:
                print(f"[JsonPromptLoader] Error reading entry: {e}")
        
        # Combine Fixed Prefix + Selected Prompt
        # Check if prefix exists and is not empty
        if self.FIXED_PREFIX and self.FIXED_PREFIX.strip():
            if selected_prompt:
                final_prompt = f"{self.FIXED_PREFIX}, {selected_prompt}"
            else:
                # If preset is empty, just return the prefix
                final_prompt = self.FIXED_PREFIX
        else:
            final_prompt = selected_prompt
            
        return (final_prompt,)

# Node Export Configurations
NODE_CLASS_MAPPINGS = {
    "JsonPromptLoader": JsonPromptLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JsonPromptLoader": "🏗️ Arch Prompt Selector"
}
