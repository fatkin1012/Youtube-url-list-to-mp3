import os
import time
import random
import yt_dlp
from tqdm import tqdm
import subprocess

def rename_m4a_to_mp3(directory='downloads'):
    """
    Rename all .m4a files to .mp3 files in the specified directory
    """
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found!")
        return
    
    renamed_count = 0
    
    for filename in os.listdir(directory):
        if filename.lower().endswith('.m4a'):
            old_path = os.path.join(directory, filename)
            new_filename = filename[:-4] + '.mp3'  # Replace .m4a with .mp3
            new_path = os.path.join(directory, new_filename)
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"Error renaming {filename}: {e}")
    print(f"\nCompleted! Renamed {renamed_count} files from .m4a to .mp3\n")

def download_audio(url, output_path='downloads'):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best[height<=480]',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'extractaudio': False,
            'no_warnings': True,
            'quiet': True,
            'retries': 3,
            'socket_timeout': 30,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                print(f"\nDownloading: {title}")
                ydl.download([url])
                clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                if not clean_title:
                    clean_title = "Unknown"
                downloaded_files = [f for f in os.listdir(output_path) 
                                  if any(word in f.lower() for word in clean_title.lower().split()[:3]) 
                                  and not f.endswith('.part')]
                if downloaded_files:
                    downloaded_file = downloaded_files[0]
                    old_path = os.path.join(output_path, downloaded_file)
                    if not downloaded_file.endswith('.mp3'):
                        new_path = os.path.join(output_path, f"{clean_title}.mp3")
                        try:
                            os.rename(old_path, new_path)
                            print(f"Successfully downloaded and renamed: {clean_title}.mp3")
                        except Exception as e:
                            print(f"Successfully downloaded: {downloaded_file} (rename failed: {e})")
                    else:
                        print(f"Successfully downloaded: {downloaded_file}")
                else:
                    print(f"Downloaded successfully but couldn't find file for: {title}")
                time.sleep(random.uniform(1, 3))
                return True
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                return False
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def download_video(url, output_path='downloads'):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'no_warnings': True,
            'quiet': True,
            'retries': 3,
            'socket_timeout': 30,
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                print(f"\nDownloading video: {title}")
                ydl.download([url])
                print(f"Successfully downloaded video: {title}.mp4")
                time.sleep(random.uniform(1, 3))
                return True
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                return False
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def merge_video_audio(directory='downloads'):
    files = os.listdir(directory)
    videos = [f for f in files if f.endswith('.mp4')]
    audios = [f for f in files if f.endswith('.m4a') or f.endswith('.webm')]

    merged_count = 0
    for video in videos:
        base = os.path.splitext(video)[0]
        # 嘗試找同名音軌
        audio = None
        for ext in ['.m4a', '.webm']:
            candidate = base + ext
            if candidate in audios:
                audio = candidate
                break
        if audio:
            output = os.path.join(directory, f"{base}_merged.mp4")
            video_path = os.path.join(directory, video)
            audio_path = os.path.join(directory, audio)
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-c', 'copy',
                output
            ]
            print(f"合併 {video} + {audio} → {os.path.basename(output)}")
            subprocess.run(cmd, check=True)
            merged_count += 1
        else:
            print(f"找不到 {video} 對應的音軌，略過。")
    print(f"\n完成！共合併 {merged_count} 組視頻+音軌。")

def main():
    print("請選擇下載模式：")
    print("1. 音樂 (mp3)")
    print("2. 影片 (mp4)")
    mode = input("請輸入 1 或 2: ").strip()
    if mode not in ['1', '2']:
        print("輸入錯誤，請重新執行程式並選擇 1 或 2。")
        return
    print("請直接貼上 YouTube 網址（可多個，用空白或逗號分隔），或輸入文字檔路徑：")
    user_input = input().strip()
    urls = []
    if os.path.exists(user_input):
        with open(user_input, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]
    else:
        # 支援多個網址，空白或逗號分隔
        for part in user_input.replace(',', ' ').split():
            if part.startswith('http'):
                urls.append(part)
    if not urls:
        print("沒有找到任何有效的網址！")
        return
    print(f"\n找到 {len(urls)} 個網址")
    success_count = 0
    if mode == '1':
        for url in tqdm(urls, desc="音樂下載進度"):
            if download_audio(url):
                success_count += 1
        print(f"\n下載完成！成功下載 {success_count}/{len(urls)} 個音樂檔案")
        print("檔案已儲存在 'downloads' 資料夾中")
        rename_m4a_to_mp3('downloads')
    else:
        for url in tqdm(urls, desc="影片下載進度"):
            if download_video(url):
                success_count += 1
        print(f"\n下載完成！成功下載 {success_count}/{len(urls)} 部影片")
        print("影片已儲存在 'downloads' 資料夾中")
    merge_video_audio('downloads')

if __name__ == "__main__":
    main() 