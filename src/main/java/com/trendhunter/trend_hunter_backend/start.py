import subprocess, time, webbrowser, os

BASE = os.path.dirname(os.path.abspath(__file__))

# 1. Backend (fenêtre séparée)
subprocess.Popen("mvnw.cmd spring-boot:run", cwd=BASE, shell=True,
                 creationflags=subprocess.CREATE_NEW_CONSOLE)

# 2. On attend qu'il démarre
print("Attente du backend (20s)...")
time.sleep(20)

# 3. Scraper
scraper = os.path.join(BASE, "src", "main", "java", "com", "trendhunter",
                       "trend_hunter_recolteur", "trend_scraper.py")
subprocess.Popen(f'python "{scraper}"', shell=True,
                 creationflags=subprocess.CREATE_NEW_CONSOLE)

# 4. Frontend
index = os.path.join(BASE, "src", "main", "java", "com", "trendhunter",
                     "trend_hunter_frontend", "index.html")
webbrowser.open(index)