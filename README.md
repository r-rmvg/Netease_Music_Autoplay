# Netease Music Auto Player

一个用于网易云音乐 Windows 桌面客户端的自动切歌脚本。脚本会按照设定的播放时长等待，并通过全局快捷键切换到下一首歌曲。

## 功能

- 自定义要播放的歌曲数量
- 按设定时长自动切换下一首
- 在终端显示播放进度和耗时
- 随时按 `Esc` 停止

## 环境要求

- Windows
- Python 3.9 或更高版本
- 网易云音乐桌面客户端

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

1. 打开网易云音乐桌面客户端并登录。
2. 进入要播放的专辑或歌单。
3. 手动将播放速度设为 `2x`。
4. 播放第一首歌。
5. 运行脚本：

   ```bash
   python netease_auto_play.py
   ```

6. 输入要播放的歌曲数量。运行期间可按 `Esc` 停止。

## 配置

可以在 `netease_auto_play.py` 顶部调整以下参数：

- `SONG_CONTENT_SECONDS`：每首歌需要播放的内容秒数
- `PLAYBACK_SPEED`：网易云音乐中手动设置的播放倍速
- `SWITCH_DELAY`：切歌后的加载等待时间

## 注意事项

- 脚本使用网易云音乐的全局快捷键 `Ctrl+Right` 切换下一首。
- Windows 可能要求以管理员身份运行终端，才能监听全局 `Esc` 按键。
- 请遵守网易云音乐的服务条款，仅将本项目用于个人学习和自动化实践。

