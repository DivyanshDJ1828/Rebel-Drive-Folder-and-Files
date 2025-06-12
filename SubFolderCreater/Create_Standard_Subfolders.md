# Create_Standard_Subfolders_V1.3.md

## 🧩 Purpose

To automate the creation of a standardized folder structure **inside each direct subfolder (1-level deep only)** of the directory where the `.bat` script is executed, and to automatically sort files into their appropriate folders. This structure is intended for organizing production files such as assets from Maya, Blender, Marvelous Designer (MD), output formats, and materials.

---

## 🛠️ Requirements

### ✅ Functional Requirements

1. **Folder Traversal**
   - The script must **loop only one level deep**.
   - It should scan all **immediate subfolders** of the folder where the `.bat` file resides.
   - It must **not recurse into sub-subfolders**.

2. **Folder Creation**
   - Inside each immediate subfolder, the script must ensure the presence of the following subdirectories:
     - `Maya-Blender files`
     - `MD files`
     - `Output format files`
     - `Materials`
   - **No folders should be created in the root folder itself** (i.e., where the `.bat` is placed).

3. **File Sorting**
   - After ensuring folders exist, automatically move files based on extensions:
     - `.glb` files → `Output format files`
     - `.fbx`, `.blend`, `.blend1`, `.ma`, `.mb` files → `Maya-Blender files`
     - `.zprj`, `.png` files → `MD files`
   - File sorting applies **regardless of whether folders were newly created or already existed**.
   - Files with the same name in destination folders should be skipped (not overwritten).

4. **Idempotent Behavior**
   - If any of the above folders already exist inside a subfolder, they should be **left untouched**.
   - The script must **not rename**, **overwrite**, or **modify** existing content.
   - Files with duplicate names in destination folders are skipped safely.

5. **Logging**
   - A log file named `created_folders_log.txt` must be generated or appended in the **same directory** where the `.bat` script is placed.
   - Log entries should include:
     - Timestamp
     - Full path of every newly created folder
     - Notice if a folder already exists and was skipped
     - Record of every file moved with source and destination paths
     - Notice if file moves were skipped due to conflicts

6. **Portability**
   - Must run as a `.bat` file on **Windows**.
   - No external tools (e.g., PowerShell, Python) are allowed.
   - Support folder names containing **spaces**.
   - Support file names containing **spaces**.

---

## 🚫 Exclusions / Assumptions

- The script does **not go deeper** than the first level of subfolders.
- The root folder where the script is placed will **not have any folders created inside it**.
- No confirmation prompts—this script runs **fully automatic**.
- Files not matching the specified extensions are left in their original location.

---

## 🧪 Sample Output

**Log File Example:**

```
[2025-06-12 14:10:01] Script started
[2025-06-12 14:10:01] ✅ Created: C:\Project\Assets\Scene1\Maya-Blender files
[2025-06-12 14:10:01] ⚠️ Already exists: C:\Project\Assets\Scene1\MD files
[2025-06-12 14:10:02] ✅ Created: C:\Project\Assets\Scene2\Output format files
[2025-06-12 14:10:02] ✅ Created: C:\Project\Assets\Scene2\Materials
[2025-06-12 14:10:03] 📁 Moved: C:\Project\Assets\Scene1\model.glb → C:\Project\Assets\Scene1\Output format files
[2025-06-12 14:10:03] 📁 Moved: C:\Project\Assets\Scene1\character.blend → C:\Project\Assets\Scene1\Maya-Blender files
[2025-06-12 14:10:04] ⚠️ File already exists, skipping: C:\Project\Assets\Scene2\texture.png
[2025-06-12 14:10:05] Script completed. Created: 3, Already existed: 1, Files moved: 2
```

---

## 📌 Versioning

- **Spec Version**: `Create_Standard_Subfolders_V1.3`
- **Author**: Divyansh Jaiswal
- **Last Updated**: 2025-06-12
- **Changelog**:
  - Added logic to move files (.glb, .fbx, .blend, .png, etc.) into appropriate folders
  - File movement now applies even if folders were not newly created
  - Enhanced logging to include file movement operations
  - Added file conflict detection and safe skipping behavior

---

## 🎯 File Extension Mapping

| Extension | Target Folder |
|-----------|--------------|
| `.glb` | `Output format files` |
| `.fbx` | `Maya-Blender files` |
| `.blend` | `Maya-Blender files` |
| `.blend1` | `Maya-Blender files` |
| `.ma` | `Maya-Blender files` |
| `.mb` | `Maya-Blender files` |
| `.zprj` | `MD files` |
| `.png` | `MD files` | 