from googleapiclient.discovery import build
import pandas as pd
# Masukkan API Key YouTube Data API v3
API_KEY = 'AIzaSyDOTGgV6AIq_Y_04BMHhTt126oJmRzA1do'
# Fungsi untuk mendapatkan komentar dari YouTube
def get_comments(video_id):
    # Membuat service object untuk menggunakan API YouTube
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    # List untuk menyimpan komentar
    comments = []
    # Request untuk mendapatkan komentar dari video
    request = youtube.commentThreads().list(
    part='snippet',
    videoId=video_id,
    maxResults=100, # Bisa menambah jumlah maksimal per request
    textFormat="plainText"
    )
    # Loop untuk tarik semua komen (pagination menggunakan nextPageToken)
    while request:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comments.append({'author': author, 'comment': comment})
        
        # Cek apakah ada halaman berikutnya
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            )
        else:
            break
    return comments
#Contoh penggunaan untuk video tertentu
if __name__ == '__main__':
    video_id = 'KOgtICimh5E' # Ganti dengan ID video YouTube yang ingin di-crawl
    comments = get_comments(video_id)
    # Simpan hasil dalam bentuk DataFrame
    df = pd.DataFrame(comments)
    # Tampilkan hasilnya
    print(df)
    # Simpan ke dalam file CSV
    df.to_csv(f'youtube_comments_{video_id}.csv', index=False)
    print(f"Komentar berhasil disimpan ke youtube_comments_{video_id}.csv")