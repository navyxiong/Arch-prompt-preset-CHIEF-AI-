# Arch-prompt-preset-CHIEF-AI

A simple yet powerful custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that allows you to load prompt presets from a JSON file.

It also features a built-in **Fixed Prefix** system, perfect for keeping consistent quality tags (e.g., "masterpiece, 8k") across all your generations.

## Features
- 📂 Load prompts from an external `presets.json` file.
- 🔒 **Fixed Prefix**: Automatically adds a defined string to the beginning of every prompt.
- 📝 Easy to edit and manage huge prompt libraries.

## Installation

1. Clone this repository into your `ComfyUI/custom_nodes/` folder:
   ```bash
   cd ComfyUI/custom_nodes/
   git clone [https://github.com/YOUR_USERNAME/ComfyUI-JSON-Prompt-Loader.git](https://github.com/YOUR_USERNAME/ComfyUI-JSON-Prompt-Loader.git)
