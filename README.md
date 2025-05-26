# YouTube Playlist MP3 批次下載工具

## 專案簡介
在旅行的時候會創造一個屬於這個旅行的 playlist，單獨下載每一首歌非常的沒效率，所以寫了個簡單的 script。

這個工具可以讓你從一個包含多個 YouTube 連結的文字檔，批次下載所有歌曲並自動轉成 mp3 檔案，省時又方便！

---

## 功能特色
- 批次下載 YouTube 音樂
- 自動將音訊檔案轉為 mp3 副檔名
- 支援多數 YouTube 影片音樂格式
- 下載完成後自動整理檔案

---

## 使用方式

1. **安裝必要套件**
   ```bash
   pip install yt-dlp tqdm
   ```

2. **準備一個文字檔**
   - 每一行放一個 YouTube 連結，例如：
     ```
     https://www.youtube.com/watch?v=xxxxxxx
     https://www.youtube.com/watch?v=yyyyyyy
     ```

3. **執行腳本**
   ```bash
   python youtube_downloader_ytdlp_simple.py
   ```
   - 輸入剛剛準備的文字檔檔名（例如：`example_urls.txt`）

4. **下載完成**
   - 所有 mp3 檔案會自動存放在 `downloads` 資料夾

---

## 注意事項
- 下載過程需要網路連線
- 若遇到下載失敗，請確認連結正確且可公開存取
- 若有部分檔案原始格式為 m4a，腳本會自動將其副檔名改為 mp3

---

## 聯絡方式
有任何建議或問題，歡迎提出！ 