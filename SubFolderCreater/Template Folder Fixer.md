# 🧹 Template\_Folder\_fixer\_v1.2.2.md

## 🌟 Objective

Convert the production folder automation logic from the Batch script `Create_Standard_Subfolders.bat` to a Python script `Template_Folder_fixer.py`.

The script should:

1. Move misplaced files from the root directory into the correct subfolders using a **strict priority-based matching** system.
2. Create and organize standardized subfolder structures inside each valid template/component folder.
3. Preserve original filenames and ensure files are never renamed or lost during operations.
4. Produce detailed logs with timestamps, match type (\[FULL], \[BASE+VER], \[BASE], \[NONE]), and success/failure indicators.

## 👤 Publisher Info

* **Author**: Divyansh Jaiswal
* **Version**: 1.2.2
* **Created On**: 2025-06-15

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
  * If destination file exists → skip + log (except in overwrite mode)

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

* Log Levels:

  * `INFO`: General operations (moves, folder creation, etc.)
  * `WARNING`: Duplicate file skips, unmatched cases
  * `ERROR`: Move failures, permission issues
  * `DEBUG`: File scanning, path decisions, conflict resolutions

### ✅ Portability & Safety

* Compatible with Python 3.11+
* Use only standard libraries: `os`, `shutil`, `time`, `logging`, `re`, `pathlib`
* Script must be portable: can be dropped into any folder and executed
* Only scan root and first-level folders (component-level depth)
* Must support filenames with spaces, uppercase, multiple underscores
* Skip hidden/system files
* Skip folders that are already subfolders (e.g. `MD files`)

### ✅ Execution Modes (selectable via CLI or keyboard on .exe)

1. **Normal Mode**

   * Move misplaced files to correct folders
   * Skip if destination file exists
   * Create standard folders and sort files

2. **Overwrite Mode** (`--overwrite`)

   * Same as Normal Mode but overwrites destination files if present

3. **Cleanup + Normal Mode** (`--clean`)

   * Recursively flatten ALL subfolders inside each component folder
   * Move files from all depths to component folder (skip if identical exists)
   * Delete all internal folders inside the component folder after file recovery
   * Then run Mode 1 logic

4. **Reset + Overwrite Mode** (`--reset-overwrite`)

   * Same as Mode 3 but overwrite conflicting files during cleanup
   * Then run Mode 2 logic

### ✅ CLI & Interactive Support

* `--mode 1|2|3|4`: Choose execution mode via command line
* `--dry-run`: Simulates operations without modifying files
* `--no-prompt`: Skip interactive confirmation
* `--log-dir <path>`: Specify custom directory for log output
* `--debug`: Enable detailed log output for troubleshooting
* `--version`: Print version and author info

When running as an `.exe`, prompt user:

```
Choose a mode:
1 - Normal Mode: Move misplaced files without overwriting anything
2 - Overwrite Mode: Move misplaced files and overwrite duplicates
3 - Cleanup + Normal Mode: Delete all subfolders in each component folder and move all files up before organizing
4 - Reset + Overwrite Mode: Same as mode 3 but allow overwriting duplicates during cleanup
Enter your choice (1-4):
```

## 🧪 Edge Case Handling

* Long basefit IDs (e.g. `U101RM`) are matched before shorter IDs (e.g. `U101`)
* If source file == destination file, skip unless in overwrite mode
* If destination folder doesn’t exist → log `❌ Folder not found`
* If move operation fails → log `❌ Move failed`
* If no folder matched → log `⛔ No matching folder found`
* Folders are deleted only if empty after all file operations
* Files are renamed with suffixes `_1`, `_2`, etc. in case of conflicts

## 🧬 Base Data (Dormant)

* `TEMPLATES`: Full list of template folder names
* `BASEFIT_IDS`: Pre-sorted (desc by length) basefit IDs for match prioritization

These will be injected but not yet validated against.

## 📁 File Structure Example

```
/root/
  MERIDIAN1_U403R_1_Girl Top Fitted Uniform Dress/
    Maya-Blender files/
    MD files/
    Output format files/
    Ref/
      Assets/
        oldfile.blend
  MERIDIAN1_U403R_1_Girl Top Fitted Uniform Dress.blend
  unknown_file.obj
```

## 📌 Versioning

* Python Version: `1.2.2`
* Filename: `Template_Folder_fixer.py`
* Publisher: Divyansh Jaiswal
* Source Migration: `Create_Standard_Subfolders.bat` → Python

## 🔮 Future Enhancements

* Add validation using `TEMPLATES` and `BASEFIT_IDS`
* Support GUI interface
* Add metadata to `.exe` version
* Optional feature: auto-detect base path from user prompt
