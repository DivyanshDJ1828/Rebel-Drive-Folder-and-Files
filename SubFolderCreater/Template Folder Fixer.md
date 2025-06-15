# 🧩 Template\_Folder\_fixer\_v1.0.md

## 🎯 Objective

Convert the production folder automation logic from the Batch script `Create_Standard_Subfolders.bat` to a Python script `Template_Folder_fixer.py`.

The script should:

1. Move misplaced files from the root directory into the correct subfolders using a **strict priority-based matching** system.
2. Create and organize standardized subfolder structures inside each valid template/component folder.
3. Preserve original filenames and ensure files are never renamed or lost during operations.
4. Produce detailed logs with timestamps, match type (\[FULL], \[BASE+VER], \[BASE], \[NONE]), and success/failure indicators.

## 🔧 Functional Requirements

### ✅ Step 1: Root File Sorter (RFS)

* **Folder-First Isolation**:

  * Scan all first-level subfolders and store folder names.
  * Do **not** fabricate or guess folder names.
  * Only use verified folder names for comparison.
* **Matching Priority** (descending):

  1. `[FULL]`: Full filename (excluding extension) == folder name
  2. `[BASE+VER]`: Folder name contains basefit ID and version (e.g. `U403RB_0`)
  3. `[BASE]`: Folder name contains basefit ID only (e.g. `U403RB`)
  4. `[NONE]`: No match → skip + log
* **Matching Normalization**:

  * Lowercase
  * Trim spaces
  * Comparison in memory only
* **Match Source**:

  * Extract components from filenames using `_` split
  * Use pre-sorted `BASEFIT_IDS` list (sorted by descending length)
* **Move Logic**:

  * Preserve `original filename + extension`
  * Do not modify filenames
  * Move only to verified existing folders
  * If destination file exists → skip + log
* **Logging**:

  * Timestamp, source, target, match type
  * Mark skipped, moved, failed, and unmatched files distinctly
  * Track total moved/skipped/unmatched/duration

### ✅ Step 2: Subfolder Structure

* Inside each matched folder, create if missing:

  * `Maya-Blender files`
  * `MD files`
  * `Output format files`
* Sort files inside folders by extension:

  * `.fbx`, `.blend`, `.blend1`, `.ma`, `.mb` → Maya-Blender files
  * `.zprj`, `.png` → MD files
  * `.glb` → Output format files
* Files not matching any extension are skipped

### ✅ Logging & Reporting

* Write to a log file `template_fixer_log.txt`
* Include:

  * Match type
  * Move status
  * File path source → destination
  * Time taken
* Track:

  * Total files moved, skipped, unmatched
  * Folders created
  * Runtime duration

### ✅ Portability & Safety

* Compatible with Python 3.11+
* Use only standard libraries: `os`, `shutil`, `time`, `logging`, `re`
* No third-party dependencies
* Script must be portable: can be dropped into any folder and executed
* No recursion: only scan root and first-level folders
* Must support filenames with spaces, uppercase, multiple underscores
* Skip hidden/system files
* Skip folders that are already subfolders (e.g. `MD files`)

## 🧪 Edge Case Handling

* Long basefit IDs (e.g. `U101RM`) must be matched before shorter ones (e.g. `U101`)
* If file already exists in destination → skip and log `⚠️ File already exists`
* If folder matched but does not exist → log `❌ Folder not found`
* If `shutil.move()` fails → log `❌ Move failed`
* If no folder matched → log `⛔ No matching folder found`

## 🧬 Base Data (Dormant)

* `TEMPLATES`: Full list of template folder names
* `BASEFIT_IDS`: Pre-sorted (desc by length) basefit IDs for match prioritization

These variables will be injected into the script but **not yet used** for validation.

## 📁 File Structure Example

```
/root/
  MERIDIAN1_U403R_1_Girl Top Fitted Uniform Dress/
    Maya-Blender files/
    MD files/
    Output format files/
  MERIDIAN1_U403R_1_Girl Top Fitted Uniform Dress.blend
  U403R_1.blend
  U403R.blend
  unknown_file.obj
```

## 📌 Versioning

* Python Version: `1.0`
* Filename: `Template_Folder_fixer.py`
* Author: Divyansh Jaiswal
* Created On: 2025-06-15
* Source Migration: `Create_Standard_Subfolders.bat` → Python

## 🔮 Future Enhancements

* Enable validation using TEMPLATES and BASEFIT\_IDS
* Add interactive CLI prompts
* Create optional GUI wrapper
* Bundle to `.exe` for non-technical use
