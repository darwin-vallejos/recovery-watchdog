"""
models.py

Database models for multi-tenant SaaS
"""

from datetime import datetime, timedelta
from typing import Optional
import sqlite3
import hashlib
import secrets


class Database:
    """Simple SQLite database for SaaS"""
    
    def __init__(self, db_path: str = "recovery_watchdog.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Organizations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                api_key TEXT UNIQUE NOT NULL,
                tier TEXT DEFAULT 'free',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                trial_ends_at TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                organization_id INTEGER,
                role TEXT DEFAULT 'member',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (organization_id) REFERENCES organizations(id)
            )
        """)
        
        # Agents table (installed monitoring agents)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL,
                agent_id TEXT UNIQUE NOT NULL,
                hostname TEXT,
                last_seen TIMESTAMP,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (organization_id) REFERENCES organizations(id)
            )
        """)
        
        # Metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                coherence REAL,
                recovery_margin REAL,
                alert_level TEXT,
                cpu_usage REAL,
                mem_usage REAL,
                error_rate REAL,
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
            )
        """)
        
        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL,
                agent_id TEXT NOT NULL,
                alert_level TEXT NOT NULL,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                acknowledged BOOLEAN DEFAULT 0,
                FOREIGN KEY (organization_id) REFERENCES organizations(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_organization(self, name: str, tier: str = 'trial') -> dict:
        """Create new organization with API key"""
        api_key = f"rwk_{secrets.token_urlsafe(32)}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Trial ends in 30 days
        trial_ends = datetime.now() + timedelta(days=30)
        
        cursor.execute("""
            INSERT INTO organizations (name, api_key, tier, trial_ends_at)
            VALUES (?, ?, ?, ?)
        """, (name, api_key, tier, trial_ends))
        
        org_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': org_id,
            'name': name,
            'api_key': api_key,
            'tier': tier
        }
    
    def verify_api_key(self, api_key: str) -> Optional[dict]:
        """Verify API key and return organization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, tier, is_active
            FROM organizations
            WHERE api_key = ? AND is_active = 1
        """, (api_key,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'tier': row[2],
                'is_active': row[3]
            }
        return None
    
    def register_agent(self, organization_id: int, hostname: str) -> str:
        """Register new monitoring agent"""
        agent_id = f"agent_{secrets.token_urlsafe(16)}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agents (organization_id, agent_id, hostname, last_seen)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (organization_id, agent_id, hostname))
        
        conn.commit()
        conn.close()
        
        return agent_id
    
    def store_metrics(self, agent_id: str, metrics: dict):
        """Store metrics for an agent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO metrics (
                agent_id, coherence, recovery_margin, alert_level,
                cpu_usage, mem_usage, error_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            agent_id,
            metrics.get('coherence'),
            metrics.get('recovery_margin'),
            metrics.get('alert_level'),
            metrics.get('cpu_usage'),
            metrics.get('mem_usage'),
            metrics.get('error_rate')
        ))
        
        # Update agent last_seen
        cursor.execute("""
            UPDATE agents SET last_seen = CURRENT_TIMESTAMP
            WHERE agent_id = ?
        """, (agent_id,))
        
        conn.commit()
        conn.close()
    
    def get_organization_agents(self, organization_id: int) -> list:
        """Get all agents for an organization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT agent_id, hostname, last_seen, status
            FROM agents
            WHERE organization_id = ?
            ORDER BY last_seen DESC
        """, (organization_id,))
        
        agents = []
        for row in cursor.fetchall():
            agents.append({
                'agent_id': row[0],
                'hostname': row[1],
                'last_seen': row[2],
                'status': row[3]
            })
        
        conn.close()
        return agents


# Test the database
if __name__ == "__main__":
    db = Database()
    
    # Create test organization
    org = db.create_organization("Acme Corp", tier="trial")
    print(f"Created organization: {org['name']}")
    print(f"API Key: {org['api_key']}")
    print()
    
    # Verify API key
    verified = db.verify_api_key(org['api_key'])
    print(f"Verified organization: {verified}")
    print()
    
    # Register agent
    agent_id = db.register_agent(org['id'], "web-server-01")
    print(f"Registered agent: {agent_id}")
    print()
    
    # Store test metrics
    test_metrics = {
        'coherence': 0.85,
        'recovery_margin': 0.35,
        'alert_level': 'GREEN',
        'cpu_usage': 25.0,
        'mem_usage': 60.0,
        'error_rate': 0.001
    }
    
    db.store_metrics(agent_id, test_metrics)
    print("Stored test metrics")
    print()
    
    # Get organization agents
    agents = db.get_organization_agents(org['id'])
    print(f"Organization has {len(agents)} agents:")
    for agent in agents:
        print(f"  - {agent['hostname']} ({agent['agent_id']})")