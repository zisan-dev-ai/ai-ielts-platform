from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
import time
from typing import Dict, Any, List, Optional
from database import get_db, init_db

class KeyPoolHealthChecker:
    """Manages multi-key pools per provider, health status, key rotation, and rate-limit recovery."""

    @staticmethod
    def seed_credentials_from_env():
        """Reads env variables and seeds ai_providers and ai_credentials into DB."""
        init_db()
        conn = get_db()
        cursor = conn.cursor()

        providers = [
            ("gemini", "Google Gemini"),
            ("deepseek", "DeepSeek V3/R1"),
            ("openai", "OpenAI GPT-4o"),
            ("claude", "Claude 3.5 Sonnet"),
            ("grok", "xAI Grok"),
            ("custom", "Custom AI")
        ]

        for pid, pname in providers:
            cursor.execute("INSERT OR IGNORE INTO ai_providers (id, name, is_enabled, priority) VALUES (?, ?, 1, 1)", (pid, pname))
            
            env_key = f"{pid.upper()}_API_KEYS"
            keys_str = os.getenv(env_key, "")
            if keys_str:
                keys = [k.strip() for k in keys_str.split(",") if k.strip()]
                for k in keys:
                    masked = k[:6] + "..." + k[-4:] if len(k) > 10 else "***"
                    cursor.execute("""
                        INSERT OR IGNORE INTO ai_credentials 
                        (provider_id, api_key_masked, api_key, status, latency_ms, error_count)
                        VALUES (?, ?, ?, 'Active', 0, 0)
                    """, (pid, masked, k))

        conn.commit()
        conn.close()

    @staticmethod
    def get_active_credential(provider_id: str) -> Optional[Dict[str, Any]]:
        """Returns the healthiest active credential for a given provider."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, provider_id, api_key, status, latency_ms, error_count 
            FROM ai_credentials 
            WHERE provider_id = ? AND status = 'Active' 
            ORDER BY error_count ASC, latency_ms ASC 
            LIMIT 1
        """, (provider_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def report_success(cred_id: int, latency_ms: int):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ai_credentials 
            SET latency_ms = ?, error_count = 0, last_used_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (latency_ms, cred_id))
        conn.commit()
        conn.close()

    @staticmethod
    def report_failure(cred_id: int, status_code: int = 500):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT error_count FROM ai_credentials WHERE id = ?", (cred_id,))
        row = cursor.fetchone()
        err_cnt = (dict(row).get("error_count", 0) + 1) if row else 1
        
        new_status = "Active"
        if status_code == 429:
            new_status = "Rate Limited"
        elif err_cnt >= 5:
            new_status = "Error"

        cursor.execute("""
            UPDATE ai_credentials 
            SET error_count = ?, status = ?, last_used_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (err_cnt, new_status, cred_id))
        conn.commit()
        conn.close()
