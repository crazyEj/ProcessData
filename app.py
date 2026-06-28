import os
import runpy

root_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(root_dir, "Data_Triage_App")

if not os.path.isdir(app_dir):
    raise FileNotFoundError(f"Expected Data_Triage_App directory at {app_dir}")

# Change working directory so Streamlit loads assets and relative imports correctly.
os.chdir(app_dir)

# Execute the actual app from the Data_Triage_App folder.
runpy.run_path(os.path.join(app_dir, "app.py"), run_name="__main__")
