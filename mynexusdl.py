import easyocr
import pyautogui
import time
import numpy as np
import cv2
import sys

# === 配置区域 ===
TARGET_TEXT_1 = "Download manually"
TARGET_TEXT_2 = "Slow download"
CONFIDENCE_THRESHOLD = 0.4 
USE_GPU = True

def init_reader():
    print(f"[System] 正在初始化 EasyOCR (GPU={USE_GPU})...")
    return easyocr.Reader(['en'], gpu=USE_GPU)

def find_and_click_lowest(reader, target_text, action_name):
    """
    识别所有匹配文本，并点击屏幕上位置最靠下的那一个
    """
    print(f"\n[Debug] 正在扫描屏幕寻找: '{target_text}' ...")
    
    screenshot = pyautogui.screenshot()
    image_np = np.array(screenshot)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    results = reader.readtext(image_bgr, detail=1)

    # 筛选出所有匹配的目标
    matches = []
    for (bbox, text, prob) in results:
        if target_text.lower() in text.lower() and prob >= CONFIDENCE_THRESHOLD:
            # 计算中心点和底边 Y 坐标
            (tl, tr, br, bl) = bbox
            center_x = int((tl[0] + br[0]) / 2)
            center_y = int((tl[1] + br[1]) / 2)
            bottom_y = br[1]
            matches.append({'text': text, 'pos': (center_x, center_y), 'bottom': bottom_y, 'prob': prob})
            print(f"[Debug] 候选目标: '{text}' (置信度: {prob:.2f}) 底部高度: {bottom_y}")

    if not matches:
        print(f"[Debug] 未找到匹配项: {target_text}")
        return False

    # === 核心逻辑：按底部 Y 坐标降序排列，取第一个（最下方的） ===
    matches.sort(key=lambda x: x['bottom'], reverse=True)
    best_match = matches[0]

    print(f"[Action] 确定目标: '{best_match['text']}' (最下方按钮)，执行点击: {best_match['pos']}")
    
    # 执行点击
    pyautogui.moveTo(best_match['pos'][0], best_match['pos'][1], duration=0.5)
    pyautogui.click()
    return True

def main():
    # 确保 CUDA 准备就绪
    reader = init_reader()
    
    print("="*40)
    print("脚本已启动。逻辑优化：将优先点击屏幕最下方的目标文本。")
    print("="*40)

    try:
        while True:
            # 第一步：点击 Manual Download
            if find_and_click_lowest(reader, TARGET_TEXT_1, "Step 1"):
                print("[Wait] 正在跳转下载选择页 (2s)...")
                time.sleep(2.5) # 稍微多给 0.5s 缓冲
                
                # 第二步：点击最下方的 Slow Download 按钮
                # 尝试最多 3 次，防止页面加载慢
                for i in range(3):
                    if find_and_click_lowest(reader, TARGET_TEXT_2, "Step 2"):
                        print("[Wait] 下载已触发，等待 5s 后开始下一轮...")
                        time.sleep(5)
                        break
                    else:
                        print(f"[Retry] 未检测到按钮，重试中 ({i+1}/3)...")
                        time.sleep(1.5)
            else:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n[System] 脚本已停止。")

if __name__ == "__main__":
    main()