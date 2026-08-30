"""
网易云音乐自动刷歌脚本
=====================
模拟键盘操作，自动在网易云音乐桌面客户端中播放歌曲。
每首歌播放指定秒数后自动切换下一首。

使用方法：
1. 打开网易云音乐桌面客户端并登录
2. 进入你要刷的专辑/歌单页面
3. 手动设置播放速度为 2x（在播放栏上点击倍速按钮）
4. 点击播放第一首歌
5. 运行本脚本
6. 按 Esc 键可随时停止脚本

依赖安装：
    pip install pyautogui keyboard
"""

import time
import sys
import threading
import os

try:
    import pyautogui
except ImportError:
    print("❌ 缺少 pyautogui，请运行: pip install pyautogui")
    sys.exit(1)

try:
    import keyboard
except ImportError:
    print("❌ 缺少 keyboard，请运行: pip install keyboard")
    sys.exit(1)


# ======================== 配置区 ========================
SONG_CONTENT_SECONDS = 45   # 每首歌需要播放的歌曲内容秒数
PLAYBACK_SPEED = 2.0        # 播放倍速（需手动在网易云中设置）
PLAY_SECONDS = SONG_CONTENT_SECONDS / PLAYBACK_SPEED  # 实际等待时间 = 22.5s
SWITCH_DELAY = 1.5           # 切歌后等待加载的秒数
# ========================================================

# 全局停止标志
stop_event = threading.Event()


def on_esc():
    """按下 Esc 时触发停止"""
    stop_event.set()


def wait_interruptible(seconds: float) -> bool:
    """
    可中断的等待。返回 True 表示正常等待完毕，False 表示被中断。
    """
    return not stop_event.wait(timeout=seconds)


def format_time(total_seconds) -> str:
    """将秒数格式化为 mm:ss"""
    total_seconds = int(total_seconds)
    m, s = divmod(total_seconds, 60)
    return f"{m:02d}:{s:02d}"


def print_banner():
    """打印启动横幅"""
    print()
    print("╔══════════════════════════════════════════════╗")
    print("║     🎵  网易云音乐 · 自动刷歌脚本  🎵      ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  歌曲内容 {:>3d}s × {:.0f}倍速 → 实际等待 {:.1f}s     ║".format(
        SONG_CONTENT_SECONDS, PLAYBACK_SPEED, PLAY_SECONDS))
    print("║  按 Esc 键随时停止                           ║")
    print("╚══════════════════════════════════════════════╝")
    print()


def print_checklist():
    """打印启动前检查清单"""
    print("🔍 启动前请确认以下事项：")
    print("   ✅  网易云音乐桌面客户端已打开并登录")
    print("   ✅  已进入目标专辑/歌单页面")
    print("   ✅  已手动设置播放倍速为 2x")
    print("   ✅  第一首歌已经开始播放")
    print()


def next_track():
    """
    发送系统"下一首"媒体键（VK_MEDIA_NEXT_TRACK）。
    媒体键是 OS 级别的事件，网易云无论前台/后台/最小化都能响应。
    """
    import ctypes
    VK_MEDIA_NEXT_TRACK = 0xB0
    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP = 0x0002
    ctypes.windll.user32.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)


def play_pause():
    """
    发送系统"播放/暂停"媒体键（VK_MEDIA_PLAY_PAUSE）。
    """
    import ctypes
    VK_MEDIA_PLAY_PAUSE = 0xB3
    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP = 0x0002
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)


def run(total_songs: int):
    """主循环：依次播放并切换歌曲"""
    # 注册 Esc 键停止
    keyboard.on_press_key("esc", lambda _: on_esc())

    completed = 0
    start_time = time.time()

    for i in range(1, total_songs + 1):
        if stop_event.is_set():
            break

        # —— 倒计时播放 ——
        elapsed_song = 0
        print(f"\n▶  正在播放第 {i}/{total_songs} 首", end="", flush=True)
        while elapsed_song < PLAY_SECONDS:
            if stop_event.is_set():
                break
            remaining = PLAY_SECONDS - elapsed_song
            # 每秒刷新一次进度
            step = min(1, remaining)
            if not wait_interruptible(step):
                break
            elapsed_song += step
            # 进度条
            pct = elapsed_song / PLAY_SECONDS
            bar_len = 25
            filled = int(bar_len * pct)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"\r▶  第 {i}/{total_songs} 首  [{bar}] {elapsed_song:.0f}/{PLAY_SECONDS}s", end="", flush=True)

        if stop_event.is_set():
            break

        completed += 1

        # —— 切换下一首 ——
        if i < total_songs:
            next_track()
            print(f"  ✅ 完成，切换下一首...")
            if not wait_interruptible(SWITCH_DELAY):
                break
        else:
            print(f"  ✅ 完成！")

    # —— 汇总 ——
    total_time = time.time() - start_time
    print("\n")
    print("═" * 46)
    if stop_event.is_set():
        print(f"⏹  手动停止！已完成 {completed}/{total_songs} 首")
    else:
        print(f"🎉 全部完成！共播放 {completed} 首歌")
    print(f"⏱  总耗时 {format_time(int(total_time))}")
    saved_time = completed * (3 * 60)  # 假设平均每首歌 3 分钟
    print(f"💡 相比手动播放，大约节省了 {format_time(saved_time)}")
    print("═" * 46)


def main():
    # 需要管理员权限来使用 keyboard 全局热键（Windows）
    print_banner()
    print_checklist()

    # 用户输入歌曲数
    while True:
        try:
            raw = input("🎶 请输入要刷的歌曲数量（输入 0 退出）: ").strip()
            total_songs = int(raw)
            if total_songs == 0:
                print("👋 已退出。")
                return
            if total_songs < 0:
                print("   ⚠️  请输入正整数。")
                continue
            break
        except ValueError:
            print("   ⚠️  请输入有效的数字。")

    # 倒计时提示
    print(f"\n🚀 即将开始刷 {total_songs} 首歌，预计耗时 {format_time(total_songs * (PLAY_SECONDS + int(SWITCH_DELAY)))}。")
    print("   请确保网易云音乐正在播放第一首歌...\n")
    for countdown in range(5, 0, -1):
        if stop_event.is_set():
            print("\n👋 已取消。")
            return
        print(f"   ⏳ {countdown} 秒后开始...", end="\r", flush=True)
        time.sleep(1)
    print(" " * 30, end="\r")  # 清除倒计时行

    run(total_songs)


if __name__ == "__main__":
    main()
