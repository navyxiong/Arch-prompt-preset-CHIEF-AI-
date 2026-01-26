# 🏢 ArchiPromptPreset - ComfyUI 建筑提示词预设节点

一个专为建筑可视化工作流设计的 ComfyUI 自定义节点，支持两级菜单选择（时间+效果）、内置提示词前缀开关及自定义文本输入。

## ✨ 功能特性

- **🎛️ 两级联动菜单**：第一级选择时间（日景/清晨/黄昏/夜景/阴天/雨雪天），第二级选择具体效果风格
- **🔘 前缀开关控制**：可选择是否自动添加内置的建筑摄影标准提示词前缀
- **📝 自定义输入**：支持追加自定义提示词，灵活补充特定需求
- **🗂️ 智能内容提取**：自动解析 JSON 中的嵌套字典结构，提取所有文本内容拼接为提示词
- **⚡ 实时预览**：节点输出完整的组合提示词，可直接连接至 CLIP Text Encode

## 📦 安装方法

### 方式一：直接克隆（推荐）

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yourusername/ArchiPromptPreset.git

### 方式二：手动安装

1. 下载本仓库所有文件
2. 将文件夹重命名为 `ArchiPromptPreset`
3. 移动至 `ComfyUI/custom_nodes/` 目录下
4. 确保文件结构如下：
ComfyUI/custom_nodes/ArchiPromptPreset/
├── __init__.py
├── archi_prompt_preset.py
├── presets.json
└── README.md
重启 ComfyUI

