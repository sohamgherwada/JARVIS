from core.brain import Brain
import traceback

print("Testing Brain Initialization...")
try:
    b = Brain()
    if b.has_model:
        print("✅ Brain initialized SUCCESSFULLY with model.")
        b.learn("Test knowledge extraction", "test_script")
    else:
        print("❌ Brain initialized but NO MODEL.")
except Exception:
    traceback.print_exc()
