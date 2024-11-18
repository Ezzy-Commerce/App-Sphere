# Required Libraries
import pyperclip
import pygame
import logging
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pyttsx3
import psutil
import speech_recognition as sr
import pyautogui
import os
import random
import json
import time
import threading
import subprocess
import webbrowser
from typing import List

# Logging Configuration
logging.basicConfig(filename='assistant_log.log', level=logging.DEBUG)

# Initialize pygame for UI
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Enlarged for readability
pygame.display.set_caption("Alex - Your Personal Assistant")

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Task Categories for Scalability
task_categories = {
    'system': {
        'get_battery_status': lambda: get_battery_status(),
        'get_system_health': lambda: system_health(),
        'get_current_datetime': lambda: get_current_datetime(),
        'take_screenshot': lambda: take_screenshot(),
        'open_file_or_folder': lambda path: open_file_or_folder(path),
        'restart_computer': lambda: restart_computer(),
        'shut_down_computer': lambda: shut_down_computer(),
        'lock_computer': lambda: lock_computer(),
        'check_network_status': lambda: check_network_status(),
        'get_ip_address': lambda: get_ip_address(),
        'ping_server': lambda: ping_server('google.com'),
        'list_active_processes': lambda: list_active_processes(),
        'kill_process': lambda name: kill_process(name),
        'change_wallpaper': lambda path: change_wallpaper(path),
        'clear_cache': lambda: clear_cache(),
        'get_system_specs': lambda: get_system_specs(),
        'check_storage_usage': lambda: check_storage_usage(),
        'open_task_manager': lambda: open_task_manager(),
    },
    'communication': {
        'send_email': lambda to, subject, body: send_email(to, subject, body),
        'copy_to_clipboard': lambda text: copy_to_clipboard(text),
        'paste_from_clipboard': lambda: paste_from_clipboard(),
        'send_sms': lambda number, message: send_sms(number, message),
        'send_message_whatsapp': lambda number, message: send_message_whatsapp(number, message),
    },
    'entertainment': {
        'search_youtube': lambda query: search_youtube(query),
        'play_music': lambda file_path: play_music(file_path),
        'pause_music': lambda: pause_music(),
        'resume_music': lambda: resume_music(),
        'play_spotify_track': lambda track_name: play_spotify_track(track_name),
        'show_random_joke': lambda: show_random_joke(),
        'fetch_movie_details': lambda movie_name: fetch_movie_details(movie_name),
        'get_top_imdb_movies': lambda: get_top_imdb_movies(),
        'fetch_top_youtube_videos': lambda: fetch_top_youtube_videos(),
    },
    'utility': {
        'schedule_task': lambda task_name, time: schedule_task(task_name, time),
        'generate_password': lambda length: generate_password(length),
        'get_weather_forecast': lambda city: get_weather_forecast(city),
        'write_code_in_window': lambda code: write_code_in_window(code),
        'write_letter_in_window': lambda letter: write_letter_in_window(letter),
        'generate_qr_code': lambda text: generate_qr_code(text),
        'get_current_weather': lambda city: get_current_weather(city),
    },
    'file_management': {
        'create_folder': lambda path: create_folder(path),
        'perform_ocr_on_image': lambda image_path: perform_ocr_on_image(image_path),
        'download_file': lambda url: download_file(url),
        'upload_file_to_cloud': lambda path: upload_file_to_cloud(path),
        'manage_files_in_directory': lambda path: manage_files_in_directory(path),
    },
    'machine_learning': {
        'perform_image_recognition': lambda image_path: perform_image_recognition(image_path),
        'perform_sentiment_analysis': lambda text: perform_sentiment_analysis(text),
    },
    'web_interaction': {
        'fetch_news_for_keywords': lambda keywords: fetch_news_for_keywords(keywords),
        'get_latest_news': lambda: get_latest_news(),
        'search_google': lambda query: search_google(query),
        'open_website': lambda url: open_website(url),
        'scrape_data_from_url': lambda url: scrape_data_from_url(url),
    },
    'social_media': {
        'post_tweet': lambda content: post_tweet(content),
        'send_telegram_message': lambda content: send_telegram_message(content),
        'search_instagram_hashtags': lambda hashtag: search_instagram_hashtags(hashtag),
        'send_facebook_update': lambda content: send_facebook_update(content),
    }
}

# Function Definitions (Examples)

# System Management Functions
def get_battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged
    status = "Plugged in" if plugged else "Not plugged in"
    return f"Battery: {percent}% ({status})"

def system_health():
    return "System health is good."

def get_current_datetime():
    return f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    return "Screenshot taken."

def open_file_or_folder(path):
    if os.path.exists(path):
        os.startfile(path)
        return f"Opened {path}"
    else:
        return "Path not found."

def restart_computer():
    subprocess.run(["shutdown", "/r", "/t", "0"])
    return "Restarting computer..."

def shut_down_computer():
    subprocess.run(["shutdown", "/s", "/t", "0"])
    return "Shutting down computer..."

def lock_computer():
    subprocess.run("rundll32.exe user32.dll,LockWorkStation")
    return "Computer locked."

def check_network_status():
    response = os.system("ping google.com")
    if response == 0:
        return "Network is up."
    else:
        return "Network is down."

def get_ip_address():
    hostname = os.popen("hostname").read().strip()
    ip_address = os.popen(f"ipconfig getifaddr {hostname}").read().strip()
    return f"IP Address: {ip_address}"

def ping_server(server):
    response = os.system(f"ping {server}")
    if response == 0:
        return f"Ping to {server} successful."
    else:
        return f"Ping to {server} failed."

def list_active_processes():
    return [proc.info for proc in psutil.process_iter(['pid', 'name'])]

def kill_process(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if name.lower() in proc.info['name'].lower():
            proc.kill()
            return f"Process {name} killed."
    return f"No process named {name} found."

def change_wallpaper(path):
    try:
        subprocess.run(f"reg add HKCU\\Control Panel\\Desktop /v Wallpaper /t REG_SZ /d {path} /f")
        subprocess.run("RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters")
        return f"Wallpaper changed to {path}"
    except Exception as e:
        return f"Failed to change wallpaper: {e}"

def clear_cache():
    subprocess.run("del /q /f /s %TEMP%\\*")
    return "Cache cleared."

def get_system_specs():
    return f"CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%"

def check_storage_usage():
    disk = psutil.disk_usage('/')
    return f"Disk usage: {disk.percent}%"

def open_task_manager():
    subprocess.run("taskmgr")
    return "Task Manager opened."

# Communication Functions
def send_email(to, subject, body):
    from_email = "your_email@example.com"
    password = "your_password"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to, msg.as_string())
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {e}"

def copy_to_clipboard(text):
    pyperclip.copy(text)
    return "Text copied to clipboard."

def paste_from_clipboard():
    return pyperclip.paste()

def send_sms(number, message):
    # Placeholder for SMS sending functionality
    return f"SMS sent to {number}: {message}"

def send_message_whatsapp(number, message):
    # Placeholder for WhatsApp messaging
    return f"WhatsApp message sent to {number}: {message}"

# Entertainment Functions
def search_youtube(query):
    search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key=YOUR_YOUTUBE_API_KEY'
    response = requests.get(search_url)
    data = response.json()
    if 'items' not in data:
        return "No results found."
    video = data['items'][0]
    return f"Found video: {video['snippet']['title']} - Watch it here: https://youtu.be/{video['id']['videoId']}"

def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    return "Music started."

def pause_music():
    pygame.mixer.music.pause()
    return "Music paused."

def resume_music():
    pygame.mixer.music.unpause()
    return "Music resumed."

def play_spotify_track(track_name):
    # Placeholder for Spotify integration
    return f"Playing track {track_name} on Spotify."

def show_random_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don’t oysters donate to charity? Because they’re shellfish."
    ]
    return random.choice(jokes)

def fetch_movie_details(movie_name):
    return f"Fetching details for movie: {movie_name}."

def get_top_imdb_movies():
    return "Fetching top IMDb movies."

def fetch_top_youtube_videos():
    return "Fetching top YouTube videos."

# Utility Functions
def schedule_task(task_name, time):
    return f"Scheduled task: {task_name} at {time}."

def generate_password(length):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()'
    password = ''.join(random.choice(characters) for _ in range(length))
    return f"Generated password: {password}"

def get_weather_forecast(city):
    return f"Fetching weather forecast for {city}."

def write_code_in_window(code):
    return f"Writing code in window: {code}"

def write_letter_in_window(letter):
    return f"Writing letter: {letter}"

def generate_qr_code(text):
    return f"QR code generated for: {text}"

def get_current_weather(city):
    return f"Fetching current weather for {city}."

# File Management Functions
def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
        return f"Folder created at {path}."
    return "Folder already exists."

def perform_ocr_on_image(image_path):
    return f"Performing OCR on {image_path}."

def download_file(url):
    return f"Downloading file from {url}."

def upload_file_to_cloud(path):
    return f"Uploading file {path} to cloud."

def manage_files_in_directory(path):
    return f"Managing files in {path}."

# Machine Learning Functions
def perform_image_recognition(image_path):
    return f"Performing image recognition on {image_path}."

def perform_sentiment_analysis(text):
    return f"Performing sentiment analysis on text: {text}"

# Web Interaction Functions
def fetch_news_for_keywords(keywords):
    return f"Fetching news for keywords: {keywords}."

def get_latest_news():
    return "Fetching latest news."

def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searched Google for {query}."

def open_website(url):
    webbrowser.open(url)
    return f"Opened website: {url}"

def scrape_data_from_url(url):
    return f"Scraping data from {url}."

# Social Media Functions
def post_tweet(content):
    return f"Posting tweet: {content}"

def send_telegram_message(content):
    return f"Sending Telegram message: {content}"

def search_instagram_hashtags(hashtag):
    return f"Searching Instagram for hashtag: {hashtag}"

def send_facebook_update(content):
    return f"Sending Facebook update: {content}"
# System Management Functions
def manage_system_startup():
    return "Managing system startup programs."

def schedule_shutdown(time):
    subprocess.run(f"shutdown /s /t {time}")
    return f"System will shut down in {time} seconds."

def disable_sleep_mode():
    powercfg_command = "powercfg -change standby-timeout-ac 0"
    subprocess.run(powercfg_command)
    return "Sleep mode disabled."

def enable_sleep_mode():
    powercfg_command = "powercfg -change standby-timeout-ac 15"
    subprocess.run(powercfg_command)
    return "Sleep mode enabled."

def optimize_disk():
    subprocess.run("defrag C: /O")
    return "Disk optimized."

def create_restore_point():
    subprocess.run("powershell.exe -Command \"Checkpoint-Computer -Description 'Restore Point' -RestorePointType 'MODIFY_SETTINGS'\"")
    return "Restore point created."

def check_for_updates():
    return "Checking for system updates."

def uninstall_application(application_name):
    subprocess.run(f"wmic product where name='{application_name}' call uninstall")
    return f"{application_name} uninstalled."

# Communication Functions
def send_sms_via_email(phone_number, message, carrier_gateway="txt.att.net"):
    email = f"{phone_number}@{carrier_gateway}"
    send_email(email, "SMS", message)
    return f"SMS sent to {phone_number}"

def record_voice_message(duration=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Recording for {duration} seconds...")
        audio = recognizer.listen(source, timeout=duration)
    with open("voice_message.wav", "wb") as file:
        file.write(audio.get_wav_data())
    return "Voice message recorded."

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()
    return f"Spoken: {text}"

# Entertainment Functions
def play_youtube_video(query):
    search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key=YOUR_YOUTUBE_API_KEY'
    response = requests.get(search_url)
    data = response.json()
    video_id = data['items'][0]['id']['videoId']
    webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")
    return f"Playing YouTube video: {query}"

def search_movies_on_netflix(query):
    return f"Searching Netflix for: {query}"

def fetch_top_twitter_trends():
    return "Fetching top Twitter trends."

def find_meme_based_on_keyword(keyword):
    return f"Searching for memes related to: {keyword}"

def fetch_top_gifs():
    return "Fetching top trending GIFs."

# Utility Functions
def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return f"File extension: {extension}"

def convert_text_to_pdf(text, file_name="output.pdf"):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(file_name)
    return f"Text converted to PDF: {file_name}"

def calculate_factorial(number):
    return f"Factorial of {number} is {math.factorial(number)}"

def calculate_area_of_circle(radius):
    import math
    area = math.pi * radius ** 2
    return f"Area of the circle with radius {radius} is {area:.2f}"

def generate_unique_id():
    return str(uuid.uuid4())

# File Management Functions
def batch_rename_files(directory, prefix="file"):
    files = os.listdir(directory)
    for index, file in enumerate(files):
        new_name = f"{prefix}_{index + 1}{os.path.splitext(file)[1]}"
        os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
    return "Files renamed successfully."

def move_file(source, destination):
    if os.path.exists(source):
        os.rename(source, destination)
        return f"Moved file from {source} to {destination}."
    else:
        return "Source file does not exist."

def compress_files(directory):
    import zipfile
    zip_file = os.path.join(directory, "archive.zip")
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for file in os.listdir(directory):
            zipf.write(os.path.join(directory, file), arcname=file)
    return f"Files compressed to {zip_file}"

def extract_zip_file(zip_path, destination):
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(destination)
    return f"Extracted {zip_path} to {destination}"

def search_file_in_directory(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return f"Found {filename} at {os.path.join(root, filename)}"
    return f"{filename} not found in {directory}"

# Machine Learning Functions
def perform_object_detection(image_path):
    return f"Performing object detection on {image_path}"

def train_model_on_data(data_path):
    return f"Training model with data from {data_path}"

def predict_from_model(model, data):
    return f"Predicted result from model: {model} with data: {data}"

# Web Interaction Functions
def monitor_website_for_changes(url):
    return f"Monitoring {url} for changes."

def scrape_images_from_url(url):
    return f"Scraping images from {url}"

def get_seo_metrics_for_website(url):
    return f"Fetching SEO metrics for {url}"

def schedule_website_update(url, time):
    return f"Website update scheduled for {url} at {time}."

def download_image_from_url(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    return f"Image downloaded to {save_path}"

# Social Media Functions
def create_facebook_post(content):
    return f"Created Facebook post: {content}"

def share_instagram_story(content):
    return f"Shared Instagram story: {content}"

def send_linkedin_message(content, recipient):
    return f"Sent LinkedIn message to {recipient}: {content}"

def get_twitter_trends():
    return "Fetching Twitter trends."

def post_on_reddit(subreddit, content):
    return f"Posted on Reddit in {subreddit}: {content}"

def get_facebook_updates():
    return "Fetching latest Facebook updates."

def fetch_user_tweets(username):
    return f"Fetching tweets for user: {username}"

# Task Management Functions
def create_task(title, description):
    return f"Task created: {title} - {description}"

def update_task_status(task_id, status):
    return f"Task {task_id} updated to {status}"

def delete_task(task_id):
    return f"Task {task_id} deleted."

def assign_task_to_user(task_id, user):
    return f"Task {task_id} assigned to {user}"

def get_task_details(task_id):
    return f"Fetching details for task {task_id}"

def set_task_deadline(task_id, deadline):
    return f"Task {task_id} deadline set to {deadline}"

# AI-Related Functions
def train_model_on_data(data):
    return f"Training model with {data}."

def evaluate_model_performance(model):
    return f"Evaluating performance of model {model}."

def make_prediction_with_model(model, data):
    return f"Prediction made with model {model} using data: {data}"

def perform_sentiment_analysis_on_text(text):
    return f"Sentiment analysis result for text: {text}"

# System Monitoring and Automation Functions
def schedule_auto_restart(time):
    subprocess.run(f"shutdown /r /t {time}")
    return f"System restart scheduled in {time} seconds."

def automate_file_backup(source, destination):
    subprocess.run(f"robocopy {source} {destination}")
    return f"Automated file backup from {source} to {destination}"

def monitor_system_for_critical_conditions():
    return "Monitoring system for critical conditions."

def run_automation_script(script_path):
    subprocess.run(["python", script_path])
    return f"Automation script {script_path} executed."

# Machine Learning (Advanced)
def process_large_dataset(data_path):
    return f"Processing large dataset from {data_path}"

def visualize_data_distribution(data):
    return f"Visualizing data distribution for {data}"

def apply_data_transformation(data, transformation_type):
    return f"Applying {transformation_type} to data {data}"

def detect_anomalies_in_data(data):
    return f"Detecting anomalies in data {data}"

def optimize_model_hyperparameters(model, data):
    return f"Optimizing hyperparameters for model {model} using data {data}


# Utility Functions (Continued)
def convert_pdf_to_text(file_path):
    from PyPDF2 import PdfReader
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_audio_length(file_path):
    import wave
    with wave.open(file_path, 'rb') as file:
        frames = file.getnframes()
        rate = file.getframerate()
        duration = frames / float(rate)
    return f"Audio length: {duration:.2f} seconds"

def send_http_request(url, method='GET', params=None, headers=None):
    if method == 'GET':
        response = requests.get(url, params=params, headers=headers)
    elif method == 'POST':
        response = requests.post(url, data=params, headers=headers)
    return response.text

def get_url_title(url):
    from bs4 import BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return f"Title of the page: {soup.title.string}"

def get_file_metadata(file_path):
    import mimetypes
    mime_type, encoding = mimetypes.guess_type(file_path)
    return f"File metadata: Type: {mime_type}, Encoding: {encoding}"

def compress_directory(directory_path):
    import tarfile
    archive_path = f"{directory_path}.tar.gz"
    with tarfile.open(archive_path, 'w:gz') as archive:
        archive.add(directory_path, arcname=os.path.basename(directory_path))
    return f"Directory compressed to {archive_path}"

def decrypt_file(file_path, key):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    cipher = Cipher(algorithms.AES(key), modes.CBC(key[:16]), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data.decode('utf-8')

# File Management Functions (Continued)
def get_disk_space():
    disk = psutil.disk_usage('/')
    return f"Disk space used: {disk.percent}% of {disk.total // (1024 ** 3)} GB"

def get_recent_files(directory, count=5):
    files = sorted(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    recent_files = files[:count]
    return f"Recent files in {directory}: {', '.join(recent_files)}"

def search_files_by_extension(directory, extension):
    found_files = [f for f in os.listdir(directory) if f.endswith(extension)]
    return f"Files with {extension} extension: {', '.join(found_files) if found_files else 'No files found'}"

def get_file_size(file_path):
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
    return f"File size: {file_size:.2f} MB"

def get_files_by_size(directory, size_limit_mb):
    large_files = [f for f in os.listdir(directory) if os.path.getsize(os.path.join(directory, f)) > size_limit_mb * 1024 * 1024]
    return f"Files larger than {size_limit_mb} MB: {', '.join(large_files) if large_files else 'No large files found'}"

# Entertainment Functions (Continued)
def search_podcasts(query):
    return f"Searching podcasts for: {query}"

def fetch_top_podcasts():
    return "Fetching top podcasts."

def get_top_streaming_shows():
    return "Fetching top streaming shows."

def search_movies_by_genre(genre):
    return f"Searching for {genre} movies."

def play_video_from_file(file_path):
    os.system(f"start {file_path}")
    return f"Playing video: {file_path}"

def fetch_trending_topics():
    return "Fetching trending topics on social media."

# Social Media Functions (Continued)
def post_on_instagram(content):
    return f"Posted on Instagram: {content}"

def share_on_twitter(content):
    return f"Shared on Twitter: {content}"

def get_linkedin_updates():
    return "Fetching LinkedIn updates."

def send_instagram_message(content, recipient):
    return f"Sent Instagram message to {recipient}: {content}"

def get_youtube_trends():
    return "Fetching YouTube trends."

def post_on_snapchat(content):
    return f"Posted on Snapchat: {content}"

# System Management Functions (Continued)
def clear_system_logs():
    log_files = ['C:/Windows/System32/LogFiles/*.log']
    for file in log_files:
        os.remove(file)
    return "System logs cleared."

def optimize_startup():
    return "Optimized startup programs."

def create_system_report():
    system_info = {
        "CPU Usage": f"{psutil.cpu_percent()}%",
        "Memory Usage": f"{psutil.virtual_memory().percent}%",
        "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        "Network Status": check_network_status(),
        "IP Address": get_ip_address(),
    }
    return json.dumps(system_info, indent=4)

def monitor_system_health():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    if cpu > 80 or memory > 80 or disk > 80:
        return "Warning: System resources are under heavy load."
    return "System resources are stable."

def check_system_uptime():
    uptime = time.time() - psutil.boot_time()
    return f"System uptime: {uptime // 3600} hours {(uptime % 3600) // 60} minutes"

def check_for_resource_hog():
    processes = psutil.process_iter(['pid', 'name', 'cpu_percent'])
    hogs = [p.info for p in processes if p.info['cpu_percent'] > 80]
    return f"Processes using more than 80% CPU: {', '.join([p['name'] for p in hogs]) if hogs else 'None'}"

# Utility Functions (Continued)
def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return f"Total size of {directory}: {total_size / (1024 * 1024)} MB"

def send_file_via_email(to_email, file_path):
    from_email = "your_email@example.com"
    password = "your_password"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "File Attachment"
    attachment = open(file_path, 'rb')
    part = MIMEText(attachment.read(), 'plain')
    msg.attach(part)
    attachment.close()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        return f"File sent to {to_email}."
    except Exception as e:
        return f"Failed to send file: {e}"

def backup_files(directory, backup_location):
    import shutil
    shutil.copytree(directory, backup_location)
    return f"Backup completed from {directory} to {backup_location}"

def schedule_task_on_system(task_name, scheduled_time):
    current_time = datetime.now()
    wait_time = (scheduled_time - current_time).total_seconds()
    if wait_time > 0:
        time.sleep(wait_time)
        return f"Task '{task_name}' scheduled at {scheduled_time} executed."
    return f"Task '{task_name}' was scheduled in the past."

def get_system_info():
    return {
        "CPU": psutil.cpu_percent(),
        "Memory": psutil.virtual_memory().percent,
        "Disk": psutil.disk_usage('/').percent,
        "Uptime": check_system_uptime()
    }

# Social Media Functions (Continued)
def fetch_twitter_trends():
    return "Fetching top Twitter trends."

def fetch_instagram_trends():
    return "Fetching top Instagram trends."

def post_linkedin_update(content):
    return f"LinkedIn update posted: {content}"

def get_facebook_posts():
    return "Fetching recent Facebook posts."

def post_on_reddit(subreddit, content):
    return f"Posted on Reddit in {subreddit}: {content}"

def get_youtube_comments(video_id):
    return f"Fetching comments for YouTube video ID: {video_id}"

def send_linkedin_message(content, recipient):
    return f"Sent LinkedIn message to {recipient}: {content}"

# System Management Functions (Continued)
def restart_system():
    os.system('shutdown /r /t 0')  # Windows command for restart
    return "System is restarting."

def shutdown_system():
    os.system('shutdown /s /t 0')  # Windows command for shutdown
    return "System is shutting down."

def change_system_time(new_time):
    import subprocess
    subprocess.run(['date', new_time])
    return f"System time changed to {new_time}"

def update_system():
    os.system('apt-get update && apt-get upgrade -y')  # Linux command for system update
    return "System updated successfully."

def check_for_updates():
    import subprocess
    result = subprocess.run(['apt-get', 'update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def set_system_language(language):
    import subprocess
    subprocess.run(['sudo', 'update-locale', f'LANG={language}'])
    return f"System language set to {language}"

# File Management Functions (Continued)
def copy_file(src, dest):
    import shutil
    shutil.copy(src, dest)
    return f"File copied from {src} to {dest}"

def move_file(src, dest):
    import shutil
    shutil.move(src, dest)
    return f"File moved from {src} to {dest}"

def delete_file(file_path):
    os.remove(file_path)
    return f"File at {file_path} deleted."

def list_files_in_directory(directory):
    files = os.listdir(directory)
    return f"Files in {directory}: {', '.join(files)}"

def search_files_by_name(directory, name):
    files = [f for f in os.listdir(directory) if name.lower() in f.lower()]
    return f"Files containing '{name}': {', '.join(files) if files else 'No files found'}"

def extract_zip(file_path, extract_to):
    import zipfile
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return f"Extracted {file_path} to {extract_to}"

# Entertainment Functions (Continued)
def search_books_by_author(author):
    return f"Searching books by author: {author}"

def fetch_top_10_books():
    return "Fetching top 10 books."

def search_for_music_by_artist(artist):
    return f"Searching for music by artist: {artist}"

def fetch_top_music_charts():
    return "Fetching top music charts."

def search_games_by_genre(genre):
    return f"Searching for {genre} games."

def fetch_top_games():
    return "Fetching top games."

def watch_live_tv_channel(channel_name):
    return f"Watching live TV channel: {channel_name}"

# Network Functions (Continued)
def check_website_status(url):
    import requests
    try:
        response = requests.get(url)
        return f"Website {url} is {'online' if response.status_code == 200 else 'offline'}."
    except requests.exceptions.RequestException:
        return f"Website {url} is offline."

def get_ip_geolocation(ip_address):
    import requests
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url).json()
    return f"Geolocation for IP {ip_address}: {response.get('city', 'N/A')}, {response.get('country', 'N/A')}"

def monitor_network_traffic():
    import psutil
    network_stats = psutil.net_io_counters()
    return f"Sent: {network_stats.bytes_sent / (1024 * 1024):.2f} MB, Received: {network_stats.bytes_recv / (1024 * 1024):.2f} MB"

def check_network_latency(host='8.8.8.8'):
    import subprocess
    result = subprocess.run(['ping', '-c', '4', host], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def get_mac_address(interface='eth0'):
    import psutil
    net_if_addrs = psutil.net_if_addrs()
    if interface in net_if_addrs:
        for addr in net_if_addrs[interface]:
            if addr.family == psutil.AF_LINK:
                return f"MAC address of {interface}: {addr.address}"
    return f"Could not retrieve MAC address for {interface}"

# Social Media Functions (Continued)
def like_facebook_post(post_id):
    return f"Liked Facebook post with ID: {post_id}"

def like_instagram_post(post_id):
    return f"Liked Instagram post with ID: {post_id}"

def follow_on_twitter(username):
    return f"Followed Twitter user: {username}"

def follow_on_instagram(username):
    return f"Followed Instagram user: {username}"

def post_on_pinterest(board, content):
    return f"Posted on Pinterest board {board}: {content}"

def send_message_on_whatsapp(phone_number, message):
    return f"Sent WhatsApp message to {phone_number}: {message}"

def get_recent_snapchat_stories():
    return "Fetching recent Snapchat stories."

def post_to_reddit(subreddit, content):
    return f"Posted to {subreddit} subreddit: {content}"

# System Management Functions (Continued)
def set_system_timezone(timezone):
    import subprocess
    subprocess.run(['sudo', 'timedatectl', 'set-timezone', timezone])
    return f"System timezone set to {timezone}"

def check_cpu_temperature():
    import psutil
    return f"CPU Temperature: {psutil.sensors_temperatures()['coretemp'][0].current}°C"

def change_screen_resolution(width, height):
    import subprocess
    subprocess.run(['xrandr', '--output', 'HDMI-1', '--mode', f'{width}x{height}'])
    return f"Screen resolution set to {width}x{height}"

def check_running_processes():
    import psutil
    processes = psutil.process_iter(['pid', 'name', 'status'])
    process_list = [f"{p.info['name']} (PID: {p.info['pid']}) - {p.info['status']}" for p in processes]
    return f"Running processes:\n" + "\n".join(process_list)

def stop_process_by_pid(pid):
    import psutil
    try:
        process = psutil.Process(pid)
        process.terminate()
        return f"Process with PID {pid} stopped."
    except psutil.NoSuchProcess:
        return f"No process found with PID {pid}."

# File Management Functions (Continued)
def list_hidden_files(directory):
    hidden_files = [f for f in os.listdir(directory) if f.startswith('.')]
    return f"Hidden files in {directory}: {', '.join(hidden_files) if hidden_files else 'No hidden files found'}"

def create_symlink(source, link_name):
    os.symlink(source, link_name)
    return f"Created symlink {link_name} pointing to {source}"

def check_file_integrity(file_path, checksum):
    import hashlib
    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_hash = hashlib.sha256(file_data).hexdigest()
    return f"File integrity check: {'Passed' if file_hash == checksum else 'Failed'}"

def monitor_file_changes(directory):
    import time
    previous_snapshot = set(os.listdir(directory))
    while True:
        time.sleep(5)
        current_snapshot = set(os.listdir(directory))
        if current_snapshot != previous_snapshot:
            print(f"Changes detected in {directory}")
            previous_snapshot = current_snapshot

# Entertainment Functions (Continued)
def search_for_new_movies():
    return "Searching for new movie releases."

def get_top_rated_movies():
    return "Fetching top rated movies."

def search_for_tv_series():
    return "Searching for TV series."

def fetch_movie_reviews(movie_id):
    return f"Fetching reviews for movie ID: {movie_id}"

def rate_movie(movie_id, rating):
    return f"Rated movie ID {movie_id} with {rating} stars."

def fetch_favorite_movies():
    return "Fetching favorite movies."

# Network Management Functions (Continued)
def get_public_ip():
    import requests
    response = requests.get('https://api.ipify.org')
    return f"Public IP address: {response.text}"

def check_port_availability(host, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    return f"Port {port} on {host} is {'open' if result == 0 else 'closed'}."

def scan_network_for_devices():
    import os
    result = os.popen("arp -a").read()
    return f"Devices on the network:\n{result}"

def monitor_internet_speed():
    import speedtest
    st = speedtest.Speedtest()
    download_speed = st.download() / 1e6  # Mbps
    upload_speed = st.upload() / 1e6  # Mbps
    return f"Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps"

def set_proxy_configuration(proxy_url):
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    return f"Proxy set to {proxy_url}"

# Continue expanding based on your specific needs and functionalities...



# Required Libraries
import pyperclip
import pygame
import logging
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pyttsx3
import psutil
import speech_recognition as sr
import pyautogui
import os
import random
import json
import time
import threading
import subprocess
import webbrowser
from typing import List

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Constants for NewsAPI
NEWS_API_KEY = "d713ed585ef4422da53ce8d5f30d1f28"  # Replace with your actual API Key
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# Initialize Pygame for UI interactions
pygame.init()

# Utility Functions
def add(a, b):
    """ Adds two numbers. """
    return a + b

def subtract(a, b):
    """ Subtracts the second number from the first. """
    return a - b

def multiply(a, b):
    """ Multiplies two numbers. """
    return a * b

def divide(a, b):
    """ Divides the first number by the second, checks for division by zero. """
    if b != 0:
        return a / b
    else:
        return "Division by zero is not allowed."

# File handling functions
def write_to_file(filename, content):
    """ Writes content to a file with the specified filename. """
    with open(filename, 'w') as file:
        file.write(content)
    logging.info(f"Content written to {filename}")
    return f"Content written to {filename}"

def read_file(filename):
    """ Reads content from a file. """
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error("File not found.")
        return "File not found."

def delete_file(filename):
    """ Deletes a specified file. """
    try:
        os.remove(filename)
        logging.info(f"File {filename} deleted.")
        return f"File {filename} deleted."
    except FileNotFoundError:
        logging.error("File not found.")
        return "File not found."

# Web scraping with BeautifulSoup
def get_headlines(url):
    """ Fetches the latest headlines from a web page using BeautifulSoup. """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = [item.text for item in soup.find_all('h2')[:5]]
        logging.info("Headlines fetched successfully.")
        return headlines
    except Exception as e:
        logging.error(f"Error fetching headlines: {e}")
        return f"Error fetching headlines: {e}"

# News API integration
def fetch_news(country='us', category='technology'):
    """ Fetches top headlines using the News API. """
    try:
        params = {
            'country': country,
            'category': category,
            'apiKey': NEWS_API_KEY
        }
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        headlines = [article['title'] for article in articles]
        if headlines:
            logging.info("News fetched successfully.")
        else:
            logging.warning("No news articles found.")
        return headlines if headlines else ["No headlines found."]
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return [f"Error fetching news: {e}"]

# Data analysis example
def analyze_data(data):
    """ Analyzes a dataset and provides descriptive statistics. """
    try:
        df = pd.DataFrame(data)
        description = df.describe()
        logging.info("Data analysis complete.")
        return description
    except Exception as e:
        logging.error(f"Error analyzing data: {e}")
        return f"Error analyzing data: {e}"

# Plotting data using Matplotlib
def plot_data(x, y):
    """ Plots a graph using Matplotlib. """
    try:
        plt.plot(x, y, marker='o')
        plt.title("Sample Data Plot")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.grid(True)
        plt.show()
        logging.info("Plotting data completed.")
    except Exception as e:
        logging.error(f"Error plotting data: {e}")
        return f"Error plotting data: {e}"

# Directory management
def create_directory(directory):
    """ Creates a directory if it does not exist. """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directory {directory} created.")
        return f"Directory {directory} created."
    else:
        logging.warning(f"Directory {directory} already exists.")
        return f"Directory {directory} already exists."

def list_files(directory):
    """ Lists all files in the specified directory. """
    try:
        files = os.listdir(directory)
        logging.info(f"Files listed in {directory}.")
        return files
    except FileNotFoundError:
        logging.error("Directory not found.")
        return "Directory not found."

# Simple database management
class SimpleDatabase:
    """ A simple in-memory database to store and retrieve key-value pairs. """
    def __init__(self):
        self.data = {}

    def insert(self, key, value):
        """ Inserts a key-value pair into the database. """
        self.data[key] = value
        logging.info(f"Inserted {key}: {value}")
        return f"Inserted {key}: {value}"

    def retrieve(self, key):
        """ Retrieves a value by key from the database. """
        value = self.data.get(key, "Key not found.")
        logging.info(f"Retrieved {key}: {value}")
        return value

    def delete(self, key):
        """ Deletes a key-value pair from the database. """
        if key in self.data:
            del self.data[key]
            logging.info(f"Deleted {key}.")
            return f"Deleted {key}."
        else:
            logging.warning("Key not found.")
            return "Key not found."

    def show_all(self):
        """ Shows all the key-value pairs in the database. """
        logging.info("Showing all data.")
        return self.data

# Social media simulation
def post_to_twitter(message):
    """ Simulates posting a message to Twitter. """
    logging.info(f"Simulated post to Twitter: {message}")
    return f"Simulated post to Twitter: {message}"

def post_to_facebook(message):
    """ Simulates posting a message to Facebook. """
    logging.info(f"Simulated post to Facebook: {message}")
    return f"Simulated post to Facebook: {message}"

# Advanced text-to-speech function using pyttsx3
def speak(text):
    """ Speaks the given text using pyttsx3. """
    engine.setProperty('rate', 150)  # Adjust speech rate
    engine.setProperty('volume', 1)  # Full volume
    engine.setProperty('voice', 'english')  # Choose voice language

    engine.say(text)
    engine.runAndWait()

# Speech Recognition
def recognize_speech_from_microphone():
    """ Recognizes speech from the microphone. """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            print("Listening for command...")
            audio = recognizer.listen(source)
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except Exception as e:
        logging.error(f"Speech recognition error: {e}")
        return "Sorry, I did not understand that."

# Automating Mouse and Keyboard (pyautogui)
def automate_mouse_and_keyboard():
    """ Simulates mouse and keyboard actions. """
    pyautogui.alert('This is an automated alert from the system!')
    pyautogui.write('Automated text', interval=0.1)
    pyautogui.press('enter')
    logging.info("Mouse and keyboard actions automated.")

# Web Scraping - Example Function
def open_url(url):
    """ Opens a URL in the web browser. """
    webbrowser.open(url)
    logging.info(f"Opened URL: {url}")

# Pygame window for text editing and saving
def open_text_editor():
    """ Opens a Pygame window where the user can input text and save it to a file. """
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Text Editor - Write and Download")
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(50, 50, 700, 500)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        text += '\n'
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, pygame.Color('white'))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Save button
        button = pygame.Rect(650, 550, 100, 30)
        pygame.draw.rect(screen, pygame.Color('green'), button)
        save_text = font.render("Save", True, pygame.Color('white'))
        screen.blit(save_text, (655, 555))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                write_to_file("saved_text.txt", text)

        pygame.display.flip()
        clock.tick(30)

# Example usage for testing
if __name__ == "__main__":
    print(fetch_news())
    speak("Welcome to the enhanced AI text-to-speech system.")
    open_text_editor()
