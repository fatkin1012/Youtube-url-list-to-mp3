# YouTube Playlist MP3/MP4 批次下載工具

## 專案簡介
在旅行的時候會創造一個屬於這個旅行的 playlist，單獨下載每一首歌非常的沒效率，所以寫了個簡單的 script。

這個工具可以讓你從一個包含多個 YouTube 連結的文字檔，或直接貼上網址，批次下載所有歌曲或影片，並自動轉成 mp3 或 mp4 檔案，省時又方便！

---

## 功能特色
- 批次下載 YouTube 音樂（mp3）或影片（mp4）
- 支援直接貼上多個網址，或讀取文字檔
- 自動將音訊檔案轉為 mp3 副檔名
- 自動合併音軌與影片（需安裝 FFmpeg）
- 下載完成後自動整理檔案
- 下載的檔案不會被 git 追蹤（`downloads/` 已加入 `.gitignore`）

---

## 使用方式

1. **安裝必要套件**
   ```bash
   pip install yt-dlp tqdm
   ```
   - 若要自動合併音軌與影片，請另外安裝 [FFmpeg](https://ffmpeg.org/download.html) 並加入 PATH

2. **準備網址**
   - 你可以直接在程式提示時貼上多個 YouTube 連結（用空白或逗號分隔）
   - 或者準備一個文字檔，每一行放一個 YouTube 連結，例如：
     ```
     https://www.youtube.com/watch?v=xxxxxxx
     https://www.youtube.com/watch?v=yyyyyyy
     ```

3. **執行腳本**
   ```bash
   python youtube_downloader_ytdlp_simple.py
   ```
   - 選擇 1（音樂）或 2（影片）
   - 貼上網址或輸入檔案名稱

4. **下載完成**
   - 所有 mp3/mp4 檔案會自動存放在 `downloads` 資料夾
   - 若有音軌與影片分開，會自動合併成一個 mp4（需 FFmpeg）

---

## 注意事項
- 下載過程需要網路連線
- 若遇到下載失敗，請確認連結正確且可公開存取
- 若有部分檔案原始格式為 m4a，腳本會自動將其副檔名改為 mp3
- `downloads/` 資料夾已被 `.gitignore` 忽略，下載的檔案不會被 git 追蹤或推送

---

## 聯絡方式
有任何建議或問題，歡迎提出！ 