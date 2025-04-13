from instagrapi import Client
import telegram
import time
import os
from datetime import datetime

TELEGRAM_BOT_TOKEN = "7742995778:AAHBI3J_2kn0BFX23LobJK7RTBQT_H_0Z5MM"
TELEGRAM_CHAT_ID = "1715637799"
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

cl = Client()
cl.login("tkhanmm95Suuuu", "your_instagram_password_here") # عوض نکن، بعداً خودت تو Render وارد می‌کنی
target_username = "target_instagram_page_here" # عوض نکن، بعداً خودت تو Render وارد می‌کنی
user_id = cl.user_id_from_username(target_username)

os.makedirs("temp", exist_ok=True)
processed_stories = set()
processed_posts = set()

def send_to_telegram(file_path=None, message=None, media_type=None):
    try:
        if file_path and media_type == "photo":
            with open(file_path, "rb") as f:
                bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=f, caption=message)
        elif file_path and media_type == "video":
            with open(file_path, "rb") as f:
                bot.send_video(chat_id=TELEGRAM_CHAT_ID, video=f, caption=message)
        elif file_path and media_type == "text":
            with open(file_path, "r", encoding="utf-8") as f:
                bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=f, caption=message)
        elif message:
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"ارسال شد: {message}")
    except Exception as e:
        print(f"خطا در ارسال به تلگرام: {e}")

def check_and_save_content():
    try:
        print(f"چک کردن محتوا در {datetime.now()}")
        stories = cl.user_stories(user_id)
        for story in stories:
            if story.pk not in processed_stories:
                file_path = f"temp/story_{story.pk}"
                if story.media_type == 1:
                    file_path += ".jpg"
                    cl.photo_download(story.pk, folder="temp")
                    send_to_telegram(file_path=file_path, message=f"استوری جدید: {story.pk}", media_type="photo")
                elif story.media_type == 2:
                    file_path += ".mp4"
                    cl.video_download(story.pk, folder="temp")
                    send_to_telegram(file_path=file_path, message=f"استوری جدید: {story.pk}", media_type="video")
                processed_stories.add(story.pk)

        posts = cl.user_medias(user_id, amount=10)
        for post in posts:
            if post.pk not in processed_posts:
                file_path = f"temp/post_{post.pk}"
                if post.media_type == 1:
                    file_path += ".jpg"
                    cl.photo_download(post.pk, folder="temp")
                    send_to_telegram(file_path=file_path, message=f"پست جدید: {post.pk}", media_type="photo")
                elif post.media_type == 2:
                    file_path += ".mp4"
                    cl.video_download(post.pk, folder="temp")
                    send_to_telegram(file_path=file_path, message=f"پست جدید: {story.pk}", media_type="video")
                comments = cl.media_comments(post.pk)
                if comments:
                    comment_file = f"temp/comments_{post.pk}.txt"
                    with open(comment_file, "w", encoding="utf-8") as f:
                        for comment in comments:
                            f.write(f"{comment.user.username}: {comment.text}\n")
                    send_to_telegram(file_path=comment_file, message=f"کامنت‌های پست {post.pk}", media_type="text")
                processed_posts.add(post.pk)

    except Exception as e:
        print(f"خطا: {e}")
        cl.login("tkhanmm95Suuuu", "your_instagram_password_here")

while True:
    check_and_save_content()
    time.sleep(15)
