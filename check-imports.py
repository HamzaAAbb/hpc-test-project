"""
check_imports.py
Verifies that all required packages for the chest X-ray training pipeline are importable.
"""
 
import sys
 
REQUIRED = [
    ("kagglehub",                       "kagglehub"),
    ("tensorflow",                       "tensorflow"),
    ("tensorflow.keras.layers",          "tensorflow (keras.layers)"),
    ("tensorflow.keras.models",          "tensorflow (keras.models)"),
    ("tensorflow.keras.applications",    "tensorflow (keras.applications VGG16)"),
    ("tensorflow.keras.applications.vgg16", "tensorflow (vgg16 preprocess_input)"),
]
 
print("=" * 50)
print("Checking required imports...")
print("=" * 50)
 
all_ok = True
for module, label in REQUIRED:
    try:
        __import__(module)
        print(f"  [OK]   {label}")
    except ImportError as e:
        print(f"  [FAIL] {label}  -->  {e}")
        all_ok = False
 
print("=" * 50)
if all_ok:
    print("All imports OK. Environment is ready.")
    sys.exit(0)
else:
    print("Some imports FAILED. Install missing packages before running the pipeline.")
    sys.exit(1)
