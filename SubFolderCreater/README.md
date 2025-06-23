# [How to Run the Folder Fixer video](https://www.loom.com/share/aaf968ef1d3c49c7acab0264756f77c5)
# 🛠 Template Folder Fixer – User Guide

This tool automatically organizes your messy template folders into a clean and standard format.

When you run the script or .exe, it will ask you to choose a mode (1-4). Each mode is designed for a specific use case.

---

## 🧭 Which Mode Should I Choose?

| Mode | Name                   | When to Use                        | What It Does                                                                 |
|------|------------------------|------------------------------------|------------------------------------------------------------------------------|
| 1    | Normal Mode            | 🟢 First Time Setup                 | Moves files to the correct folders without changing or overwriting anything |
| 2    | Overwrite Mode         | 🔁 You’ve added new versions       | Moves files and replaces old ones with new ones                             |
| 3    | Cleanup + Normal Mode  | 🧹 Old messy folder structure       | Deletes all subfolders and brings files up before organizing                |
| 4    | Reset + Overwrite Mode | 🧹➕💾 Messy folders + new files     | Does everything Mode 3 does, but replaces duplicate files with new ones     |

---

## 🧪 Mode Details with Examples

### 🔹 Mode 1: Normal Mode
**“Move misplaced files without overwriting anything”**

✅ Use this the first time you’re organizing your folder or if you don’t want to lose any files.

**Example:**

**Before:**
```
MERIDIAN1_U403/
  design_top.blend
  old_file.blend
  random.png
```

**After Mode 1:**
```
MERIDIAN1_U403/
  Maya-Blender files/design_top.blend
  MD files/random.png
  old_file.blend  ← stays untouched if it's already in the right place
```

If a file with the same name already exists, the new one will be renamed like `design_top_1.blend` to avoid overwriting.

---

### 🔸 Mode 2: Overwrite Mode
**“Move files and overwrite duplicates”**

🧹 Use this if you’ve added updated files and want to replace old versions.

**Example:**
You added a new `skirt.blend` to the root folder.  
The folder already has an older `skirt.blend`.

→ Mode 2 will **replace** the old one with your new one.

---

### 🔹 Mode 3: Cleanup + Normal Mode
**“Delete all subfolders and move all files up before organizing”**

🧹 Use this if you have an old messy structure (like Ref, Temp, Assets, OLD, etc.) and want to clean it.

**Before:**
```
MERIDIAN1_U403/
  Ref/
    Assets/
      jacket.blend
  MD files/
    skirt.blend
```

**After Mode 3:**

- All files from `Ref/Assets/` are moved up into `MERIDIAN1_U403/`
- Subfolders like `Ref` and `Assets` are deleted
- Files are sorted into the correct folders based on type

⚠️ It will not overwrite any files — if duplicates are found, it adds suffixes like `_1`, `_2`.

---

### 🔸 Mode 4: Reset + Overwrite Mode
**“Same as Mode 3, but overwrite duplicates”**

🧹💾 Use this if you’re cleaning old folders and want to ensure new files replace old ones.

**Example:**

You cleaned a folder earlier and it created:
```
skirt.blend
skirt_1.blend
skirt_2.blend
```

Now, you want to keep only the original file (no `_1`, `_2`) and remove the rest.

→ Mode 4:
- Keeps only `skirt.blend`
- Deletes `skirt_1.blend`, `skirt_2.blend`
- Moves `skirt.blend` to the correct folder

---

## 💡 Summary: Which Button Should I Click?

| Mode | Use When…                              | Shortcut                                |
|------|----------------------------------------|-----------------------------------------|
| 1    | You’re setting up a folder for the first time | ✅ Click this for first time setup      |
| 2    | You’ve added new files and want to replace old ones | 🔁 Click this to update files        |
| 3    | You want to clean up and fix an old messy folder | 🧹 Click this to fix messy folders     |
| 4    | You want to clean up and replace old files with new ones | 🧹💾 Click this to clean + update |

---
