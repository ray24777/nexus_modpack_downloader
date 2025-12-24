下面是根据你给出的脚本内容整理生成的 **`README.md`**，适合直接放在项目根目录中使用。我在说明中保持了工程化、可维护的风格，并对关键逻辑做了清晰解释，方便你后续修改或交付他人使用。

---

# Vortex 整合包自动下载脚本

本项目是一个基于 **EasyOCR + PyAutoGUI** 的自动化脚本，用于在 Vortex/Nexus Mods 下载页面中**自动识别并点击下载按钮**，从而实现整合包的半自动/全自动下载流程。

脚本核心特点是：

> **当页面中存在多个相同文本按钮时，始终优先点击屏幕最下方的那个按钮**，以避免误点广告或无效区域。

---

## 功能特性

* 实时屏幕截图 + OCR 文本识别
* 使用 EasyOCR（支持 GPU 加速）
* 自动移动鼠标并点击目标按钮
* 优先选择页面中 **最下方** 的目标文本
* 自动重试，适应页面加载延迟


---

## 自动化流程说明

脚本会循环执行以下步骤：

1. **扫描屏幕**

   * 查找包含 `Download manually` 的按钮
   * 若存在多个，选择 **最下方** 的一个并点击

2. **等待页面跳转**

3. **再次扫描屏幕**

   * 查找包含 `Slow download` 的按钮
   * 同样只点击最下方的那个
   * 若页面加载较慢，最多重试 3 次

4. **等待下载触发完成**

5. **进入下一轮循环**

---

## 环境依赖

### Python 版本

* Python **3.8 及以上**（推荐 3.9 / 3.10）

### Python 库依赖

```bash
pip install easyocr pyautogui numpy opencv-python
```

#### 额外说明

* `EasyOCR` 默认使用 PyTorch
* 若启用 GPU，请确保：

  * 已正确安装 CUDA
  * PyTorch 支持 CUDA

---

## 配置参数说明

脚本顶部的 **配置区域** 可按需调整：

```python
TARGET_TEXT_1 = "Download manually"   # 第一步目标文本
TARGET_TEXT_2 = "Slow download"       # 第二步目标文本
CONFIDENCE_THRESHOLD = 0.4            # OCR 置信度阈值
USE_GPU = True                        # 是否启用 GPU
```

### 参数含义

* **TARGET_TEXT_1 / TARGET_TEXT_2**

  * 用于 OCR 匹配的关键文本
  * 支持模糊匹配（不区分大小写）

* **CONFIDENCE_THRESHOLD**

  * OCR 识别可信度阈值
  * 过低可能误点，过高可能漏检

* **USE_GPU**

  * `True`：使用 GPU 加速 OCR
  * `False`：仅使用 CPU（兼容性更好）

---

## 核心逻辑说明（重要）

### 为什么选择“最下方”的按钮？

在 Nexus / Vortex 下载页面中，常见问题包括：

* 同一文本出现多次
* OCR 可能识别到非真实按钮区域

解决方案：
**以按钮的底边 Y 坐标作为排序依据，始终选择 Y 最大的目标（即页面最下方）**

```python
matches.sort(key=lambda x: x['bottom'], reverse=True)
best_match = matches[0]
```

这样可以显著提高点击准确率。

---

## 使用方法

1. 打开 Vortex 中整合包下载页面，直到看到第一个 "Download manually" 后停止操作
2. 确保目标按钮可见（不要被窗口遮挡）
3. 运行脚本：

```bash
python auto_download.py
```

4. 脚本将自动开始识别并点击
5. 按 `Ctrl + C` 可随时停止脚本

---

## 注意事项

建议使用去广告插件移除 nexus 页面上的广告 banner，否则在打开的页面上，下载按钮可能需要向下滚动才能看到

---

## 常见问题排查

### 1️⃣ 找不到按钮

* 检查页面是否为英文
* 降低 `CONFIDENCE_THRESHOLD`（如 0.35）
* 确保按钮完全显示在屏幕内

### 2️⃣ GPU 报错

* 将 `USE_GPU = False`
* 确认 PyTorch CUDA 版本是否匹配

### 3️⃣ 点击位置偏移

* 检查系统 DPI 缩放（建议 100%）
* 避免多显示器混用不同缩放比例

---

## 免责声明

本脚本仅用于**个人自动化操作与学习研究用途**。
请遵守 Nexus Mods / Vortex 的用户协议，合理使用下载资源。


