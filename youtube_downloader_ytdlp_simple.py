import os
import time
import random
import yt_dlp
from tqdm import tqdm

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
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Configure yt-dlp options for direct audio download
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best[height<=480]',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'writethumbnail': False,
            'writeinfojson': False,
            'writedescription': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': True,
            'extractaudio': False,
            'no_warnings': True,
            'quiet': True,
            'retries': 3,
            'socket_timeout': 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            try:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                print(f"\nDownloading: {title}")
                
                # Download the audio
                ydl.download([url])
                
                # Clean title for filename
                clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                if not clean_title:
                    clean_title = "Unknown"
                
                # Find the downloaded file and rename to .mp3 if needed
                downloaded_files = [f for f in os.listdir(output_path) 
                                  if any(word in f.lower() for word in clean_title.lower().split()[:3]) 
                                  and not f.endswith('.part')]
                
                if downloaded_files:
                    downloaded_file = downloaded_files[0]  # Take the first match
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
                
                # Add delay to avoid rate limiting
                time.sleep(random.uniform(1, 3))
                
                return True
                
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                return False
            
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def main():
    # Get input file path from user
    input_file = input("請輸入包含 YouTube 網址的文字檔路徑: ")
    
    # Check if file exists
    if not os.path.exists(input_file):
        print("找不到指定的文件！")
        return
    
    # Read URLs from file
    with open(input_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file if line.strip()]
    
    print(f"\n找到 {len(urls)} 個網址")
    
    # Create progress bar
    success_count = 0
    for url in tqdm(urls, desc="下載進度"):
        if download_audio(url):
            success_count += 1
    
    print(f"\n下載完成！成功下載 {success_count}/{len(urls)} 個檔案")
    print("檔案已儲存在 'downloads' 資料夾中")

    # Rename all .m4a files to .mp3 after download
    rename_m4a_to_mp3('downloads')

if __name__ == "__main__":
    main() 