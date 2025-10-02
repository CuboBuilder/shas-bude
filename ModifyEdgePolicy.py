import os
import json
import shutil
import ctypes

# Target file
file_path = r"C:\Windows\System32\IntegratedServicesRegionPolicySet.json"

# Backup folder
backup_folder = os.path.join(os.environ['USERPROFILE'], 'backups')
os.makedirs(backup_folder, exist_ok=True)
backup_path = os.path.join(backup_folder, os.path.basename(file_path))

# Admin check
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("ERROR: You must run this script as Administrator.")
    input("Press Enter to exit...")
    exit()

# Verify file exists
if not os.path.isfile(file_path):
    print(f"ERROR: File not found: {file_path}")
    exit()

# Backup original
shutil.copy2(file_path, backup_path)
print(f"Backup created at: {backup_path}")

# Load JSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find Edge policy
for policy in data.get('policies', []):
    if policy.get('guid') == "{1bca278a-5d11-4acf-ad2f-f9ab6d7f93a6}":
        # Change defaultState
        if policy.get('defaultState') == "disabled":
            policy['defaultState'] = "enabled"
            print("defaultState changed to 'enabled'")
        # Replace AT with UA in enabled regions
        regions = policy.get('conditions', {}).get('region', {}).get('enabled', [])
        for i, country in enumerate(regions):
            if country == "AT":
                regions[i] = "UA"
                print("Region 'AT' changed to 'UA'")

# Save JSON back
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Modification complete.")
