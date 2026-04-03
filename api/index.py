import json
import logging
import os
import sys
import threading
import time
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Import your existing modules
from byte import *
from important_zitado import *

# ================== CONFIG ==================
PROMO_TEXT = "Tg @THEROSHAN | Ig @THEROSHAN"
START_SPAM_DURATION = 18
WAIT_AFTER_MATCH_SECONDS = 20
START_SPAM_DELAY = 0.2

# ================== LOGGING ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global state
active_bots: Dict[str, Dict] = {}
app = FastAPI()

class StartBotRequest(BaseModel):
    team_code: str
    account_id: str
    password: str

class StopBotRequest(BaseModel):
    account_id: str

class BotStatusResponse(BaseModel):
    status: str
    message: str
    active_bots: Dict

# ================== BOT MANAGER CLASS ==================
class BotManager:
    def __init__(self, uid: str, password: str):
        self.uid = uid
        self.password = password
        self.running = False
        self.thread = None
        self.team_code = None
        self.key = None
        self.iv = None
        self.socket_client = None
        
    def start_bot(self, team_code: str):
        """Start the bot for a specific team code"""
        self.team_code = team_code
        self.running = True
        self.thread = threading.Thread(target=self._run_bot, daemon=True)
        self.thread.start()
        return f"Bot started for team {team_code}"
    
    def stop_bot(self):
        """Stop the bot"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        return "Bot stopped"
    
    def _run_bot(self):
        """Main bot loop"""
        try:
            # Login and get token
            token_data = self._login()
            if not token_data:
                logging.error(f"Login failed for {self.uid}")
                return
            
            # Connect to game servers
            self._connect_to_game(token_data)
            
            # Auto start loop
            while self.running:
                self._auto_start_cycle()
                
        except Exception as e:
            logging.error(f"Bot error: {e}")
        finally:
            self.running = False
    
    def _login(self):
        """Login to FreeFire"""
        # Import your existing FF_CLIENT login logic here
        # Simplified version:
        try:
            from app import FF_CLIENT
            client = FF_CLIENT(self.uid, self.password)
            # The login happens in __init__
            if client.key and client.iv:
                self.key = client.key
                self.iv = client.iv
                return True
        except Exception as e:
            logging.error(f"Login error: {e}")
        return False
    
    def _connect_to_game(self, token_data):
        """Connect to game servers"""
        # Your existing socket connection logic
        pass
    
    def _auto_start_cycle(self):
        """Single auto-start cycle"""
        if not self.running:
            return
        
        # Join team
        # Send start packet
        # Wait
        # Leave and repeat
        
        time.sleep(WAIT_AFTER_MATCH_SECONDS)

# ================== API ENDPOINTS ==================

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "FreeFire Auto Start Bot",
        "version": "1.0.0",
        "endpoints": {
            "/start": "POST - Start bot with team code",
            "/stop": "POST - Stop bot",
            "/status": "GET - Get bot status",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/start")
async def start_bot(request: StartBotRequest):
    """Start the bot with a team code"""
    try:
        account_id = request.account_id
        password = request.password
        team_code = request.team_code
        
        # Validate team code (only numbers)
        if not team_code.isdigit():
            raise HTTPException(status_code=400, detail="Team code must contain only numbers")
        
        # Check if bot already running for this account
        if account_id in active_bots and active_bots[account_id].running:
            return BotStatusResponse(
                status="already_running",
                message=f"Bot already running for account {account_id}",
                active_bots={aid: "running" for aid in active_bots}
            )
        
        # Create and start bot
        bot = BotManager(account_id, password)
        message = bot.start_bot(team_code)
        active_bots[account_id] = bot
        
        return BotStatusResponse(
            status="started",
            message=message,
            active_bots={aid: "running" for aid in active_bots}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Start bot error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop")
async def stop_bot(request: StopBotRequest):
    """Stop the bot for an account"""
    try:
        account_id = request.account_id
        
        if account_id not in active_bots:
            return BotStatusResponse(
                status="not_found",
                message=f"No active bot found for account {account_id}",
                active_bots={aid: "running" for aid in active_bots}
            )
        
        message = active_bots[account_id].stop_bot()
        del active_bots[account_id]
        
        return BotStatusResponse(
            status="stopped",
            message=message,
            active_bots={aid: "running" for aid in active_bots}
        )
        
    except Exception as e:
        logging.error(f"Stop bot error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Get all active bots status"""
    return BotStatusResponse(
        status="ok",
        message=f"{len(active_bots)} active bots",
        active_bots={aid: "running" for aid in active_bots}
    )

@app.get("/accounts")
async def list_accounts():
    """List available accounts from bot.txt"""
    try:
        with open("bot.txt", "r") as f:
            accounts = json.load(f)
        return {"accounts": list(accounts.keys())}
    except Exception as e:
        return {"accounts": [], "error": str(e)}
