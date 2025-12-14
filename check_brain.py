import lancedb
from pathlib import Path

BRAIN_DIR = Path(__file__).parent / "brain_data"
DB_PATH = BRAIN_DIR / "lancedb"

try:
    db = lancedb.connect(str(DB_PATH))
    if "knowledge" in db.table_names():
        tbl = db.open_table("knowledge")
        print(f"✅ Data Found! Total Concepts: {len(tbl)}")
        print("Sample Data:")
        print(tbl.search().limit(3).to_list())
    else:
        print("⚠️ No 'knowledge' table found yet.")
except Exception as e:
    print(f"❌ Error checking brain: {e}")
