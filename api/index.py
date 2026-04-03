from flask import Flask, render_template_string, request, jsonify
import json
import os
import time
from datetime import datetime

app = Flask(__name__)

# HTML Template - Clean Modern Dashboard
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FF Bot Dashboard | @THEROSHAN</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: #0f0f1a;
            color: #fff;
            overflow-x: hidden;
        }
        
        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            opacity: 0.1;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header */
        .header {
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 3em;
            margin-bottom: 10px;
        }
        
        h1 {
            font-size: 2.5em;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #888;
            font-size: 1.1em;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.08);
            border-color: rgba(102,126,234,0.5);
        }
        
        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
        }
        
        .stat-title {
            color: #888;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: 800;
            color: #667eea;
        }
        
        /* Control Panel */
        .control-panel {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .section-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #667eea;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102,126,234,0.4);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #f56565, #ed64a6);
            color: white;
        }
        
        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(245,101,101,0.4);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #48bb78, #38a169);
            color: white;
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #ed8936, #dd6b20);
            color: white;
        }
        
        /* Team Code Input */
        .team-input-group {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .team-input {
            flex: 1;
            padding: 12px 20px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: white;
            font-size: 1em;
            font-family: 'Inter', sans-serif;
        }
        
        .team-input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        /* Logs Section */
        .logs-section {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .logs-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .logs-container {
            background: #0a0a0f;
            border-radius: 15px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
        }
        
        .log-entry {
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-family: monospace;
        }
        
        .log-time {
            color: #667eea;
            margin-right: 15px;
        }
        
        .log-info {
            color: #48bb78;
        }
        
        .log-warning {
            color: #ed8936;
        }
        
        .log-error {
            color: #f56565;
        }
        
        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        
        .status-online {
            background: rgba(72,187,120,0.2);
            color: #48bb78;
            border: 1px solid #48bb78;
        }
        
        .status-offline {
            background: rgba(245,101,101,0.2);
            color: #f56565;
            border: 1px solid #f56565;
        }
        
        /* Scrollbar */
        .logs-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .logs-container::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        
        .logs-container::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 10px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .button-group {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
            }
            
            .team-input-group {
                flex-direction: column;
            }
            
            h1 {
                font-size: 1.8em;
            }
        }
        
        /* Loading Animation */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .loading {
            animation: pulse 1s infinite;
        }
        
        /* Tooltip */
        .tooltip {
            position: relative;
            display: inline-block;
        }
        
        .tooltip .tooltip-text {
            visibility: hidden;
            background: #333;
            color: #fff;
            text-align: center;
            padding: 5px 10px;
            border-radius: 6px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            white-space: nowrap;
            font-size: 12px;
        }
        
        .tooltip:hover .tooltip-text {
            visibility: visible;
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo">🎮</div>
            <h1>FreeFire Bot Dashboard</h1>
            <p class="subtitle">Real-time Bot Monitoring & Control Panel</p>
            <div style="margin-top: 20px;">
                <span class="status-badge status-online" id="botStatusBadge">● Bot Active</span>
            </div>
        </div>
        
        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-title">Active Teams</div>
                <div class="stat-value" id="activeTeams">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🚀</div>
                <div class="stat-title">Matches Started</div>
                <div class="stat-value" id="matchesStarted">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⏱️</div>
                <div class="stat-title">Uptime</div>
                <div class="stat-value" id="uptime">0h</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💾</div>
                <div class="stat-title">Memory Usage</div>
                <div class="stat-value" id="memory">0%</div>
            </div>
        </div>
        
        <!-- Control Panel -->
        <div class="control-panel">
            <div class="section-title">🎮 Bot Controls</div>
            
            <div class="team-input-group">
                <input type="text" class="team-input" id="teamCode" placeholder="Enter Team Code (e.g., 123456)" />
                <button class="btn btn-primary" onclick="startBot()">▶️ Start Bot</button>
            </div>
            
            <div class="button-group" style="margin-top: 20px;">
                <button class="btn btn-danger" onclick="stopBot()">⏹️ Stop Bot</button>
                <button class="btn btn-warning" onclick="restartBot()">🔄 Restart Bot</button>
                <button class="btn btn-success" onclick="refreshData()">🔄 Refresh Status</button>
                <button class="btn btn-primary" onclick="clearLogs()">🗑️ Clear Logs</button>
            </div>
        </div>
        
        <!-- Current Status -->
        <div class="control-panel">
            <div class="section-title">📊 Current Status</div>
            <div id="currentStatus">
                <p><strong>Current Team:</strong> <span id="currentTeam">None</span></p>
                <p><strong>Bot Status:</strong> <span id="botRunning">Idle</span></p>
                <p><strong>Last Action:</strong> <span id="lastAction">No actions yet</span></p>
            </div>
        </div>
        
        <!-- Logs Section -->
        <div class="logs-section">
            <div class="logs-header">
                <div class="section-title">📝 Live Logs</div>
                <button class="btn btn-primary" onclick="refreshLogs()" style="padding: 8px 20px;">🔄 Refresh</button>
            </div>
            <div class="logs-container" id="logs">
                <div class="log-entry">Waiting for logs...</div>
            </div>
        </div>
    </div>
    
    <script>
        let autoRefreshInterval;
        
        // Start auto-refresh
        function startAutoRefresh() {
            if (autoRefreshInterval) clearInterval(autoRefreshInterval);
            autoRefreshInterval = setInterval(() => {
                refreshData();
                refreshLogs();
            }, 5000);
        }
        
        // Refresh all data
        function refreshData() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('activeTeams').innerText = data.active_teams || 0;
                    document.getElementById('matchesStarted').innerText = data.matches_started || 0;
                    document.getElementById('uptime').innerText = data.uptime || '0h';
                    document.getElementById('memory').innerText = data.memory || '0%';
                    document.getElementById('currentTeam').innerText = data.current_team || 'None';
                    document.getElementById('botRunning').innerText = data.running ? 'Running' : 'Stopped';
                    
                    const statusBadge = document.getElementById('botStatusBadge');
                    if (data.running) {
                        statusBadge.className = 'status-badge status-online';
                        statusBadge.innerHTML = '● Bot Active';
                    } else {
                        statusBadge.className = 'status-badge status-offline';
                        statusBadge.innerHTML = '● Bot Inactive';
                    }
                })
                .catch(err => console.error('Error:', err));
        }
        
        // Refresh logs
        function refreshLogs() {
            fetch('/api/logs')
                .then(response => response.json())
                .then(data => {
                    const logsDiv = document.getElementById('logs');
                    if (data.logs && data.logs.length > 0) {
                        logsDiv.innerHTML = data.logs.map(log => `
                            <div class="log-entry">
                                <span class="log-time">[${log.time}]</span>
                                <span class="log-${log.level.toLowerCase()}">[${log.level}]</span>
                                <span>${log.message}</span>
                            </div>
                        `).join('');
                        logsDiv.scrollTop = logsDiv.scrollHeight;
                    } else {
                        logsDiv.innerHTML = '<div class="log-entry">No logs available</div>';
                    }
                })
                .catch(err => console.error('Error:', err));
        }
        
        // Start bot with team code
        function startBot() {
            const teamCode = document.getElementById('teamCode').value;
            if (!teamCode) {
                alert('Please enter a team code!');
                return;
            }
            
            fetch('/api/control', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'start', team_code: teamCode })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`Bot started for team ${teamCode}!`);
                    document.getElementById('lastAction').innerText = `Started bot for team ${teamCode}`;
                    refreshData();
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(err => alert('Error: ' + err));
        }
        
        // Stop bot
        function stopBot() {
            if (confirm('Are you sure you want to stop the bot?')) {
                fetch('/api/control', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'stop' })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Bot stopped!');
                        document.getElementById('lastAction').innerText = 'Stopped bot';
                        refreshData();
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(err => alert('Error: ' + err));
            }
        }
        
        // Restart bot
        function restartBot() {
            if (confirm('Restart the bot? This may take a few seconds.')) {
                fetch('/api/control', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'restart' })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Bot restarting...');
                        document.getElementById('lastAction').innerText = 'Restarted bot';
                        setTimeout(() => refreshData(), 3000);
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(err => alert('Error: ' + err));
            }
        }
        
        // Clear logs
        function clearLogs() {
            fetch('/api/control', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'clear_logs' })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Logs cleared!');
                    refreshLogs();
                }
            })
            .catch(err => alert('Error: ' + err));
        }
        
        // Initial load
        startAutoRefresh();
        refreshData();
        refreshLogs();
    </script>
</body>
</html>
'''

# Store bot state (in production, use a database)
bot_state = {
    'running': False,
    'current_team': None,
    'active_teams': 0,
    'matches_started': 0,
    'start_time': datetime.now(),
    'logs': []
}

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    uptime = (datetime.now() - bot_state['start_time']).total_seconds()
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    
    return jsonify({
        'running': bot_state['running'],
        'current_team': bot_state['current_team'],
        'active_teams': bot_state['active_teams'],
        'matches_started': bot_state['matches_started'],
        'uptime': f"{hours}h {minutes}m",
        'memory': '45'  # Placeholder
    })

@app.route('/api/logs')
def get_logs():
    # Get last 100 logs
    recent_logs = bot_state['logs'][-100:]
    return jsonify({'logs': recent_logs})

@app.route('/api/control', methods=['POST'])
def control_bot():
    data = request.json
    action = data.get('action')
    
    if action == 'start':
        team_code = data.get('team_code')
        bot_state['running'] = True
        bot_state['current_team'] = team_code
        bot_state['active_teams'] = 1
        
        # Add log
        bot_state['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'level': 'INFO',
            'message': f'Bot started for team {team_code}'
        })
        
        return jsonify({'success': True, 'message': f'Bot started for team {team_code}'})
    
    elif action == 'stop':
        bot_state['running'] = False
        bot_state['current_team'] = None
        bot_state['active_teams'] = 0
        
        bot_state['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'level': 'INFO',
            'message': 'Bot stopped by user'
        })
        
        return jsonify({'success': True, 'message': 'Bot stopped'})
    
    elif action == 'restart':
        bot_state['running'] = True
        bot_state['matches_started'] += 1
        
        bot_state['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'level': 'INFO',
            'message': 'Bot restarted'
        })
        
        return jsonify({'success': True, 'message': 'Bot restarted'})
    
    elif action == 'clear_logs':
        bot_state['logs'] = []
        return jsonify({'success': True, 'message': 'Logs cleared'})
    
    return jsonify({'success': False, 'error': 'Unknown action'})

# Vercel handler
app = app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
