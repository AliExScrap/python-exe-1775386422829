import http.server
import socketserver
import webbrowser
import threading
import os
import time

# L'application AionMind COMPLÈTE
html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AionMind - Focus & Productivité</title>
    <style>
        :root {
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --accent: #00d2ff;
            --text: #ffffff;
        }

        body {
            margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            background-attachment: fixed; height: 100vh; display: flex;
            align-items: center; justify-content: center; color: var(--text); overflow: hidden;
        }

        .glass-container {
            width: 90%; max-width: 1000px; height: 80vh; background: var(--glass-bg);
            backdrop-filter: blur(15px); border: 1px solid var(--glass-border);
            border-radius: 20px; display: flex; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .sidebar { width: 250px; border-right: 1px solid var(--glass-border); padding: 2rem; display: flex; flex-direction: column; }
        .logo { font-size: 1.5rem; font-weight: bold; margin-bottom: 2rem; text-align: center; color: var(--accent); }
        nav { display: flex; flex-direction: column; gap: 1rem; }
        .nav-btn { background: transparent; border: 1px solid transparent; color: white; padding: 0.8rem; border-radius: 10px; cursor: pointer; transition: 0.3s; text-align: left; }
        .nav-btn.active { background: var(--glass-border); border-color: var(--accent); }
        .content { flex: 1; padding: 2rem; overflow-y: auto; }
        .app-section { animation: fadeIn 0.5s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        textarea { width: 100%; height: 300px; background: rgba(0,0,0,0.2); border: 1px solid var(--glass-border); border-radius: 10px; color: white; padding: 1rem; outline: none; resize: none; }
        .action-btn { background: var(--accent); border: none; color: #000; padding: 0.8rem 1.5rem; border-radius: 10px; cursor: pointer; font-weight: bold; margin-top: 1rem; }
        .timer-display { font-size: 5rem; font-weight: bold; text-align: center; margin: 2rem 0; text-shadow: 0 0 20px var(--accent); }
        .timer-controls { display: flex; justify-content: center; gap: 1rem; }
        .habit-input { display: flex; gap: 10px; margin-bottom: 1rem; }
        input[type="text"] { flex: 1; background: rgba(0,0,0,0.2); border: 1px solid var(--glass-border); padding: 0.8rem; border-radius: 10px; color: white; outline: none; }
        ul { list-style: none; padding: 0; }
        li { background: var(--glass-bg); padding: 1rem; margin-bottom: 0.5rem; border-radius: 10px; display: flex; justify-content: space-between; border: 1px solid var(--glass-border); }
        .delete-btn { background: rgba(255, 0, 0, 0.3); border: none; color: white; padding: 5px 10px; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="glass-container">
        <aside class="sidebar">
            <h1 class="logo">AionMind</h1>
            <nav>
                <button onclick="showSection('journal')" class="nav-btn active" id="btn-journal">Journal</button>
                <button onclick="showSection('pomodoro')" class="nav-btn" id="btn-pomodoro">Pomodoro</button>
                <button onclick="showSection('habits')" class="nav-btn" id="btn-habits">Habitudes</button>
            </nav>
        </aside>
        <main class="content">
            <section id="journal" class="app-section">
                <h2>Journal de Bord</h2>
                <textarea id="journal-input" placeholder="Comment se passe votre journée ?"></textarea>
                <button onclick="saveJournal()" class="action-btn">Sauvegarder</button>
            </section>
            <section id="pomodoro" class="app-section" style="display:none;">
                <h2>Pomodoro Timer</h2>
                <div class="timer-display" id="timer">25:00</div>
                <div class="timer-controls">
                    <button id="timer-toggle" onclick="toggleTimer()" class="action-btn">Démarrer</button>
                    <button onclick="resetTimer()" class="action-btn" style="background: rgba(255,255,255,0.2); color: white;">Reset</button>
                </div>
            </section>
            <section id="habits" class="app-section" style="display:none;">
                <h2>Suivi d'Habitudes</h2>
                <div class="habit-input">
                    <input type="text" id="new-habit" placeholder="Ex: Boire de l'eau...">
                    <button onclick="addHabit()" class="action-btn">Ajouter</button>
                </div>
                <ul id="habit-list"></ul>
            </section>
        </main>
    </div>
    <script>
        function showSection(id) {
            document.querySelectorAll('.app-section').forEach(s => s.style.display = 'none');
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(id).style.display = 'block';
            document.getElementById('btn-' + id).classList.add('active');
        }
        const journalInput = document.getElementById('journal-input');
        journalInput.value = localStorage.getItem('aion_journal') || '';
        function saveJournal() {
            localStorage.setItem('aion_journal', journalInput.value);
            alert('Journal sauvegardé !');
        }
        let timeLeft = 25 * 60; let timerId = null;
        function updateTimerDisplay() {
            const mins = Math.floor(timeLeft / 60); const secs = timeLeft % 60;
            document.getElementById('timer').textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        function toggleTimer() {
            if (timerId) { clearInterval(timerId); timerId = null; document.getElementById('timer-toggle').textContent = 'Reprendre'; }
            else { timerId = setInterval(() => { if (timeLeft > 0) { timeLeft--; updateTimerDisplay(); } else { clearInterval(timerId); alert('Temps écoulé !'); } }, 1000); document.getElementById('timer-toggle').textContent = 'Pause'; }
        }
        function resetTimer() { clearInterval(timerId); timerId = null; timeLeft = 25 * 60; updateTimerDisplay(); document.getElementById('timer-toggle').textContent = 'Démarrer'; }
        const habitList = document.getElementById('habit-list');
        let habits = JSON.parse(localStorage.getItem('aion_habits') || '[]');
        function renderHabits() {
            habitList.innerHTML = '';
            habits.forEach((habit, index) => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${habit}</span><button class="delete-btn" onclick="deleteHabit(${index})">X</button>`;
                habitList.appendChild(li);
            });
        }
        function addHabit() {
            const input = document.getElementById('new-habit');
            if (input.value) { habits.push(input.value); localStorage.setItem('aion_habits', JSON.stringify(habits)); input.value = ''; renderHabits(); }
        }
        function deleteHabit(index) { habits.splice(index, 1); localStorage.setItem('aion_habits', JSON.stringify(habits)); renderHabits(); }
        renderHabits();
    </script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

PORT = 8081 # Port différent pour éviter les conflits

def start_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}/index.html')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
