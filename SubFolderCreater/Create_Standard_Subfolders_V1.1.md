# Create_Standard_Subfolders_V1.1.md

## 🧩 Purpose

To automate the creation of a standardized folder structure **inside each direct subfolder (1-level deep only)** of the directory where the `.bat` script is executed. This structure is intended for organizing production files such as assets from Maya, Blender, Marvelous Designer (MD), output formats, and materials.

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

3. **Idempotent Behavior**
   - If any of the above folders already exist inside a subfolder, they should be **left untouched**.
   - The script must **not rename**, **overwrite**, or **modify** existing content.

4. **Logging**
   - A log file named `created_folders_log.txt` must be generated or appended in the **same directory** where the `.bat` script is placed.
   - Log entries should include:
     - Timestamp
     - Full path of every newly created folder
     - Notice if a folder already exists and was skipped

5. **Portability**
   - Must run as a `.bat` file on **Windows**.
   - No external tools (e.g., PowerShell, Python) are allowed.
   - Support folder names containing **spaces**.

---

## 🚫 Exclusions / Assumptions

- The script does **not go deeper** than the first level of subfolders.
- The root folder where the script is placed will **not have any folders created inside it**.
- No confirmation prompts—this script runs **fully automatic**.

---

## 🧪 Sample Output

**Log File Example:**

```
[2025-06-12 14:10:01] ✅ Created: C:\Project\Assets\Scene1\Maya-Blender files
[2025-06-12 14:10:01] ⚠️ Already exists: C:\Project\Assets\Scene1\MD files
[2025-06-12 14:10:02] ✅ Created: C:\Project\Assets\Scene2\Output format files
[2025-06-12 14:10:02] ✅ Created: C:\Project\Assets\Scene2\Materials
```

---

## 📌 Versioning

- **Spec Version**: `Create_Standard_Subfolders_V1.1`
- **Author**: Divyansh Jaiswal
- **Last Updated**: 2025-06-12