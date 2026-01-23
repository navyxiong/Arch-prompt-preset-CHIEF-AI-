import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "ArchiPromptPreset.CascadingDropdown",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "ArchiPromptPreset") return;
        
        // 保存原始 onNodeCreated
        const onNodeCreated = nodeType.prototype.onNodeCreated;
        
        nodeType.prototype.onNodeCreated = function() {
            const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : this;
            
            // 获取时间分类和风格效果的 widget
            const timeWidget = this.widgets.find(w => w.name === "time_category");
            const styleWidget = this.widgets.find(w => w.name === "style_effect");
            
            if (!timeWidget || !styleWidget) return r;
            
            // 从节点定义中获取选项映射
            const timeOptions = nodeData.input.required.time_category[0];
            const stylesMap = {};
            
            // 尝试从配置中读取（如果 ComfyUI 传递了完整数据）
            if (nodeData.input.required.style_effect && 
                nodeData.input.required.style_effect[0]) {
                // 保存初始选项作为默认
                stylesMap["default"] = [...nodeData.input.required.style_effect[0]];
            }
            
            // 从后端获取完整的映射关系（通过 hidden inputs 或直接访问文件）
            // 这里我们采用前端动态请求的方式
            this.fetchStyleMapping = async () => {
                try {
                    const response = await fetch('/extensions/ArchiPromptPreset/presets_mapping');
                    if (response.ok) {
                        const data = await response.json();
                        return data;
                    }
                } catch (e) {
                    console.log("[ArchiPromptPreset] Using fallback mapping");
                }
                return null;
            };
            
            // 更新风格选项的函数
            const updateStyleOptions = (selectedTime) => {
                // 从全局变量或缓存获取映射（如果后端提供了）
                const mapping = window.archiPromptMapping || {};
                const availableStyles = mapping[selectedTime] || [];
                
                if (availableStyles.length > 0) {
                    styleWidget.options.values = availableStyles;
                    // 如果当前选中的值不在新列表中，重置为第一个
                    if (!availableStyles.includes(styleWidget.value)) {
                        styleWidget.value = availableStyles[0];
                    }
                }
            };
            
            // 监听时间变化
            timeWidget.callback = (value) => {
                updateStyleOptions(value);
                // 触发重绘
                if (this.graph) {
                    this.graph.change();
                }
            };
            
            // 初始化
            setTimeout(() => {
                updateStyleOptions(timeWidget.value);
            }, 100);
            
            return r;
        };
    },
    
    // 另一种方式：通过节点配置传递映射关系
    async getCustomWidgets(nodeType, nodeData) {
        if (nodeData.name !== "ArchiPromptPreset") return;
        
        // 读取 presets.json 并建立映射
        try {
            const response = await fetch('custom_nodes/ArchiPromptPreset/presets.json');
            const data = await response.json();
            
            // 存储到全局供回调使用
            window.archiPromptMapping = {};
            for (const [category, styles] of Object.entries(data)) {
                if (typeof styles === 'object' && !Array.isArray(styles)) {
                    window.archiPromptMapping[category] = Object.keys(styles);
                }
            }
        } catch (e) {
            console.error("[ArchiPromptPreset] Failed to load presets mapping:", e);
        }
    }
});
