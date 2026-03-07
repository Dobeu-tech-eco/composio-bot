import sqlite3
import json

db_path = r'C:\Users\jswil\AppData\Roaming\Cursor\User\globalStorage\state.vscdb'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

fixed_content = json.dumps({
    "version": 1,
    "hooks": {
        "sessionStart": [{"command": "./scripts/runlayer-hook.sh"}],
        "beforeMCPExecution": [{"command": "./scripts/runlayer-hook.sh"}],
        "beforeReadFile": [{"command": "./scripts/runlayer-hook.sh"}]
    }
}, indent=2) + "\n"

cursor.execute(
    "UPDATE cursorDiskKV SET value = ? WHERE key LIKE '%runlayer%hooks%'",
    (fixed_content,)
)
print(f"Rows updated: {cursor.rowcount}")
conn.commit()

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE '%runlayer%hooks%'")
row = cursor.fetchone()
if row:
    print(f"Verified: {row[0][:150]}")
conn.close()
print("Done. Restart Cursor for the fix to take effect.")
