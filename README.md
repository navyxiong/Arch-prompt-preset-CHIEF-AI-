# ComfyUI Archi-prompt-preset

A streamlined custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) designed for efficient prompt management. 

It allows you to select prompt presets from an external JSON file via a dropdown menu, while automatically enforcing a built-in **Fixed Prefix** (e.g., quality tags) to ensure consistent output quality.

![Node Screenshot](https://via.placeholder.com/600x200?text=Archi-prompt-preset+Screenshot)
*(You can replace this link with a screenshot of your node)*

## ✨ Features

- **JSON-Based Management**: Load unlimited prompt presets from `presets.json`.
- **Dropdown Interface**: Automatically reads keys from the JSON file and displays them in a user-friendly dropdown menu.
- **Built-in Fixed Prefix**: Automatically prepends a hardcoded string (e.g., "masterpiece, best quality, 8k") to every prompt, ensuring consistent style across all generations.
- **Hot-Reloading (Values)**: You can tweak the prompt text in the JSON file without restarting ComfyUI (Note: Adding *new* keys requires a restart).

## 📥 Installation

1. Navigate to your ComfyUI `custom_nodes` directory:
   ```bash
   cd ComfyUI/custom_nodes/git clone [https://github.com/YOUR_USERNAME/ComfyUI-Archi-prompt-preset.git](https://github.com/YOUR_USERNAME/ComfyUI-Archi-prompt-preset.git)
