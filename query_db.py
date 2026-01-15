"""Quick database query"""
import sqlite3

conn = sqlite3.connect("recovery_watchdog.db")
cursor = conn.cursor()

print("=" * 60)
print("ORGANIZATIONS")
print("=" * 60)
cursor.execute("SELECT id, name, tier FROM organizations")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Tier: {row[2]}")

print("\n" + "=" * 60)
print("AGENTS")
print("=" * 60)
cursor.execute("SELECT agent_id, hostname, status FROM agents")
for row in cursor.fetchall():
    print(f"Agent: {row[0]}")
    print(f"  Host: {row[1]}")
    print(f"  Status: {row[2]}")

print("\n" + "=" * 60)
print("RECENT METRICS (Last 5)")
print("=" * 60)
cursor.execute("SELECT timestamp, coherence, alert_level FROM metrics ORDER BY timestamp DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"{row[0]} | C={row[1]:.3f} | {row[2]}")

print("\n" + "=" * 60)
print("TOTAL METRICS COLLECTED")
print("=" * 60)
cursor.execute("SELECT COUNT(*) FROM metrics")
count = cursor.fetchone()[0]
print(f"Total: {count} metrics")

conn.close()