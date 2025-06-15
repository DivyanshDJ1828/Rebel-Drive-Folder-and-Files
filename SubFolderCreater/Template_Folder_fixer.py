#!/usr/bin/env python3
"""
=============================================================================
Script Name: Template_Folder_fixer.py
Version: 1.2.3
Author: Divyansh Jaiswal
Created On: 2025-06-15
Source Migration: Create_Standard_Subfolders.bat → Python
Spec Source: Template_Folder_fixer_v1.2.3.md

Purpose: Automate organization of production files through:
1. Root File Sorter (RFS): Move misplaced files using priority-based matching
2. Subfolder Structure: Create standardized folder organization
3. Deep Cleanup: Recursive subfolder flattening with file recovery

Requirements: Python 3.11+, Standard libraries only
=============================================================================
"""

__version__ = "1.2.3"
__author__ = "Divyansh Jaiswal"
__description__ = "Template folder fixer for standardizing design folder structure with safe sorting, cleanup, and logging logic."

import os
import shutil
import time
import logging
import re
import argparse
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

# =============================================================================
# DORMANT BASE DATA (Future validation - not yet used)
# =============================================================================

# Dormant template list for future validation
TEMPLATES = [
    "abby1", "abigail1", "base1", "abiola1", "abira1", "adair1", "addison1", 
    "adeline1", "adelita1", "adelka1", "adiel1", "adrianna1", "agasha1", "ailsa1", 
    "aine1", "alabama1", "alameda1", "alba1", "alessandra1", "alessia1", "aleta1", 
    "alice1", "alicia1", "aliyah1", "almeria1", "amal1", "amari1", "ambry1", 
    "amira1", "amy1", "anastasia1", "angel1", "angeline1", "anita1", "annie1", 
    "annie2", "antonia1", "apple1", "arabesque1", "ariana1", "armani1", "arwen1", 
    "ashanti1", "ashby1", "ashley1", "ashton1", "atkins1", "aubrey1", "audrey1", 
    "augustina1", "austin1", "autumn1", "ava1", "avalon1", "baila1", "bailey1", 
    "bay1", "bayberry1", "bea1", "beatrice1", "becky1", "bermuda1", "betsy1", 
    "bev1", "birdie1", "blair1", "blakely1", "blossom1", "blythe1", "bria1", 
    "brianna1", "bronwyn1", "brooke1", "bryce1", "bryleigh1", "calypso1", "camara1", 
    "camerson1", "camila1", "candace1", "candie1", "cara1", "carey1", "carla1", 
    "carlson1", "carmen1", "carmine1", "cashel1", "celeste1", "chantelle1", "cher1", 
    "chita1", "chloe1", "choffell1", "circini1", "clara1", "coline1", "concetta1", 
    "corbin1", "corey1", "cort1", "cris1", "crishell1", "crista1", "danette1", 
    "dani1", "danita1", "darcie1", "davonne1", "daylee1", "deidra1", "delhi1", 
    "delores1", "demi1", "denton1", "desi1", "detra1", "devin1", "dominique1", 
    "doreen1", "dorman1", "dorothy1", "dove1", "dover1", "dune1", "easter1", 
    "eaton1", "echo1", "edith1", "eilam1", "elda1", "elena1", "eliana1", "ella1", 
    "elliot1", "elmira1", "emberly1", "emmalisa1", "emmanuelle1", "ensley1", 
    "essence1", "ester1", "everleigh1", "evette1", "fabiana1", "fabriana1", 
    "faith1", "farrah1", "farrow1", "fatima1", "fayette1", "finn1", "fontaine1", 
    "frances1", "gabi1", "galea1", "gazelle1", "geela1", "gem1", "gemma1", 
    "geneva1", "genevive1", "georgianna1", "gianna1", "gilda1", "gillian1", 
    "gleam1", "glenda1", "goldie1", "govia1", "grace1", "grenelle1", "hagar1", 
    "haisley1", "haneli1", "hannelore1", "hasley1", "honey1", "ida1", "imogen1", 
    "iris1", "isadora1", "isla1", "ismene1", "ivy1", "jace1", "jaden1", "jamie1", 
    "jamika1", "jane1", "jane2", "jasmine1", "jean1", "jemine1", "jenell1", 
    "jenny1", "jess1", "jill1", "johntell1", "jolene1", "jolie1", "journey1", 
    "joyce1", "judy1", "juliana1", "july1", "jupiter1", "kacee1", "kaitlin1", 
    "kala1", "kari1", "karissa1", "kate1", "kathleen1", "katrina1", "katy1", 
    "kayla1", "kelia1", "kellyn1", "kempton1", "kenna1", "kennedy1", "kessler1", 
    "kinsley1", "kline1", "kristina1", "kyber1", "kylie1", "lachelle1", "lala1", 
    "landon1", "laney1", "langdon1", "lani1", "larue1", "lasha1", "laurie1", 
    "lea1", "leelee1", "leila1", "leona1", "levin1", "levity1", "lila1", "lindsey1", 
    "liora1", "loire1", "loris1", "love1", "luana1", "lucia1", "lupita1", "lyric1", 
    "maeve1", "magdalena1", "marbella1", "marcelle1", "marceline1", "mareli1", 
    "marianna1", "mariela1", "marika1", "marilyn1", "marion1", "marla1", "martha1", 
    "mavel1", "meadow1", "megan1", "melania1", "mercury1", "meredith1", "meridian1", 
    "mia1", "mika1", "mikaela1", "mila1", "millie1", "millita1", "mina1", "minuet1", 
    "mirabella1", "moira1", "monique1", "moorie1", "moriah1", "nadia1", "nantes1", 
    "naveen1", "navi1", "nevada1", "noe1", "novah1", "nyleen1", "oaklynn1", 
    "ocean1", "olive1", "ophira1", "panima1", "parker1", "pascaline1", "paula1", 
    "pauline1", "penrose1", "perla1", "petra1", "petunia1", "phoebe1", "phyllis1", 
    "piper1", "potter1", "prairie1", "precious1", "pyxie1", "que1", "rae1", 
    "rania1", "rasha1", "raven1", "reed1", "rella1", "ren1", "reole1", "rhythm1", 
    "richmond1", "rio1", "riya1", "roman1", "rosa1", "roseanne1", "rosie1", 
    "roslyn1", "rothwell1", "rozi1", "rylin1", "sable1", "sai1", "samara1", 
    "sammy1", "sandhya1", "sandia1", "sandrine1", "sansa1", "sara1", "sarafina1", 
    "sarita1", "sarte1", "satley1", "saylor1", "scout1", "selena1", "serena1", 
    "sheila1", "shel1", "shelby1", "shelia1", "sherry1", "shiloh1", "shira1", 
    "sidney1", "sofia1", "soren1", "spring1", "starling1", "sunja1", "sunny1", 
    "sydney1", "sylvia1", "tally1", "tammy1", "tana1", "tegan1", "tempion1", 
    "thalia1", "thelma1", "theta1", "tibet1", "tiffany1", "toni1", "trinitie1", 
    "trixie1", "uma1", "valeriia1", "varina1", "verdin1", "veronica1", "viana1", 
    "virginia1", "vita1", "viviana1", "vona1", "wanda1", "wando1", "waverly1", 
    "willow1", "wonder1", "wren1", "yazmin1", "york1", "zulah1"
]

# Dormant basefit ID list for future matching (sorted by descending length)
BASEFIT_IDS = [
    "U403RTB", "U102RM", "U102RV", "U102RSH", "U102RC", "U101RV", "U101RSH", 
    "U101RM", "U101RC", "U102SH", "U102M", "U102C", "U101SH", "U101C", "U101M", 
    "U101V", "U123R", "U127", "U128", "U201B", "U210B", "U211B", "U211.5", 
    "U211B.5", "U403B", "U403R", "U403RB", "U404R", "U406R", "U406RB", "U405R", 
    "P401S", "U501R", "U502R", "U601S", "U604S", "U605S", "U701R", "U212B", 
    "U214B", "U129S", "U102V", "P212S", "U406B", "U101R", "U102R", "U103R", 
    "U104R", "U501", "U502", "U504", "U601", "U604", "U605", "U607", "U701", 
    "P101", "P102", "P206", "P209", "N501", "U105", "U214", "U215", "U209", 
    "P213", "P214", "P301", "P302", "U118", "P401", "P109", "U406", "U404", 
    "U405", "U119", "P212", "P211", "N110", "N146", "U123", "U301", "U108", 
    "U110", "U122", "U129", "N206", "U101", "U102", "U103", "U104", "U106", 
    "U107", "U109", "U201", "U203", "U204", "U206", "U210", "U211", "U216", 
    "U302", "U403"
]

# =============================================================================
# GLOBAL CONFIGURATION
# =============================================================================

# Standard subfolder names to create
STANDARD_FOLDERS = [
    "Maya-Blender files",
    "MD files", 
    "Output format files"
]

# File extension mapping
EXTENSION_MAPPING = {
    "Maya-Blender files": [".fbx", ".blend", ".blend1", ".ma", ".mb"],
    "MD files": [".zprj", ".png"],
    "Output format files": [".glb"]
}

# Supported file extensions (all extensions we process)
SUPPORTED_EXTENSIONS = []
for extensions in EXTENSION_MAPPING.values():
    SUPPORTED_EXTENSIONS.extend(extensions)

# Execution modes
EXECUTION_MODES = {
    1: "Normal Mode: Move misplaced files without overwriting anything  \n  -CLICK THIS FOR FIRST TIME SETUP OF FOLDERS\n",
    2: "Overwrite Mode: Move misplaced files and overwrite duplicates \n  -CLICK THIS IF YOU HAVE ADDED NEW FILES IN THE FOLDER AND WANT TO REMOVE OLD FILES\n", 
    3: "Cleanup + Normal Mode: Delete all subfolders in each component folder and move all files up before organizing   \n  -CLICK THIS IF YOU WANT TO UPDATE AN OLD FOLDER STRACTURE\n",
    4: "Reset + Overwrite Mode: Same as mode 3 but allow overwriting duplicates during cleanup \n  -CLICK THIS IF YOU WANT TO UPDATE AN OLD FOLDER STRACTURE + HAVE ADDED NEW FILES IN THE FOLDER\n"
}

# =============================================================================
# ARGUMENT PARSING
# =============================================================================

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=f"Template Folder Fixer v{__version__} - {__description__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Execution Modes:
  1 - Normal Mode: Move misplaced files without overwriting
  2 - Overwrite Mode: Move misplaced files and overwrite duplicates
  3 - Cleanup + Normal Mode: Recursively flatten ALL subfolders and move files up
  4 - Reset + Overwrite Mode: Same as mode 3 but overwrite duplicates during cleanup

Examples:
  python Template_Folder_fixer.py
  python Template_Folder_fixer.py --overwrite --dry-run
  python Template_Folder_fixer.py --clean --debug
  python Template_Folder_fixer.py --reset-overwrite --no-prompt
  python Template_Folder_fixer.py --mode 3 --debug --dry-run
        """
    )
    
    parser.add_argument('--version', action='version', version=f'Template Folder Fixer v{__version__}')
    parser.add_argument('--mode', type=int, choices=[1, 2, 3, 4], 
                       help='Execution mode (1-4). If not specified, interactive prompt will be shown.')
    parser.add_argument('--overwrite', action='store_const', const=2, dest='mode',
                       help='Enable overwrite mode (equivalent to --mode 2)')
    parser.add_argument('--clean', action='store_const', const=3, dest='mode',
                       help='Enable cleanup + normal mode (equivalent to --mode 3)')
    parser.add_argument('--reset-overwrite', action='store_const', const=4, dest='mode',
                       help='Enable reset + overwrite mode (equivalent to --mode 4)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Simulate file operations without actual move/delete')
    parser.add_argument('--no-prompt', action='store_true', 
                       help='Skip execution confirmation prompt (defaults to Mode 1 if --mode not specified)')
    parser.add_argument('--log-dir', type=str, default=None,
                       help='Custom directory for log file (default: current directory)')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug-level logging for detailed operation tracking')
    
    return parser.parse_args()

# =============================================================================
# LOGGING SETUP
# =============================================================================

def setup_logging(log_dir=None, mode=1, dry_run=False, debug=False):
    """Setup logging configuration for the script."""
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "template_fixer_log.txt")
    else:
        log_file = "template_fixer_log.txt"
    
    # Set logging level based on debug flag
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Log execution mode and settings
    mode_name = EXECUTION_MODES.get(mode, f"Unknown Mode {mode}")
    dry_run_text = " (DRY RUN)" if dry_run else ""
    debug_text = " (DEBUG)" if debug else ""
    logger.info(f"[{get_timestamp()}] 🚀 Template Folder Fixer v{__version__} started")
    logger.info(f"[{get_timestamp()}] 🎯 Execution Mode: {mode} - {mode_name}{dry_run_text}{debug_text}")
    
    return logger

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_timestamp():
    """Get formatted timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def normalize_name(name):
    """Normalize name for comparison (lowercase, trimmed)."""
    return name.lower().strip()

def is_hidden_or_system_file(filepath):
    """Check if file is hidden or system file."""
    filename = os.path.basename(filepath)
    return filename.startswith('.') or filename.startswith('~')

def is_standard_subfolder(folder_name):
    """Check if folder is one of our standard subfolders."""
    return folder_name in STANDARD_FOLDERS

def extract_filename_components(filename):
    """Extract components from filename using underscore split."""
    # Remove extension for analysis
    name_only = os.path.splitext(filename)[0]
    
    # Split by underscore
    parts = name_only.split('_')
    
    if len(parts) >= 3:
        part1 = parts[0]
        part2 = parts[1] 
        part3 = parts[2]
        basefit_version = f"{part2}_{part3}"
        basefit = part2
    elif len(parts) >= 2:
        part1 = parts[0]
        part2 = parts[1]
        part3 = ""
        basefit_version = ""
        basefit = part2
    else:
        part1 = parts[0] if parts else ""
        part2 = ""
        part3 = ""
        basefit_version = ""
        basefit = ""
    
    return {
        'name_only': name_only,
        'part1': part1,
        'part2': part2, 
        'part3': part3,
        'basefit_version': basefit_version,
        'basefit': basefit
    }

def get_execution_mode(args):
    """Get execution mode from arguments or user input."""
    if args.mode:
        return args.mode
    
    if args.no_prompt:
        return 1  # Default to Normal Mode
    
    # Interactive mode selection
    print("version={0}".format(__version__))
    print("\n" + "="*80)
    print("🎯 Template Folder Fixer - Mode Selection")
    print("="*80)
    print("Choose a mode:")
    for mode_num, description in EXECUTION_MODES.items():
        print(f"{mode_num} - {description}")
    print("="*80)
    print("Just press Enter to open the README file in your browser.")
    print("="*80)
    
    while True:
        try:
            choice = input("Enter your choice (1-4) or press Enter for README: ").strip()
            
            # If user presses Enter without input, open README
            if choice == "":
                print("📖 Opening README in your browser...")
                try:
                    webbrowser.open("https://github.com/DivyanshDJ1828/Rebel-Drive-Folder-and-Files/blob/a61e1ff5866527c017359177915bb9d57e01d3de/SubFolderCreater/README.md")
                except Exception as e:
                    print(f"❌ Could not open browser: {e}")
                    print("📖 Please visit: https://github.com/DivyanshDJ1828/Rebel-Drive-Folder-and-Files/blob/a61e1ff5866527c017359177915bb9d57e01d3de/SubFolderCreater/README.md")
                
                # Exit gracefully after opening README
                print("\n👋 Exiting. Run the script again after reading the README.")
                sys.exit(0)
            
            # If user enters a valid mode number
            mode = int(choice)
            if mode in EXECUTION_MODES:
                return mode
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("❌ Invalid input. Please enter a number (1-4) or press Enter for README.")
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user.")
            sys.exit(0)

def files_are_identical(file1, file2):
    """Check if two files are identical (same size and modification time)."""
    try:
        stat1 = os.stat(file1)
        stat2 = os.stat(file2)
        return (stat1.st_size == stat2.st_size and 
                abs(stat1.st_mtime - stat2.st_mtime) < 1)  # Allow 1 second difference
    except (OSError, FileNotFoundError):
        return False

def resolve_filename_collision(dest_path, allow_overwrite=False, mode=1):
    """Resolve filename collisions by adding _1, _2, etc. suffixes if overwrite is disabled.
    In Mode 4, removes existing suffixed files and preserves only the original name."""
    logger = logging.getLogger(__name__)
    
    if not os.path.exists(dest_path):
        return dest_path
    
    if allow_overwrite:
        return dest_path
    
    # Mode 4 special handling: Remove suffixed versions and use original name
    if mode == 4:
        base_dir = os.path.dirname(dest_path)
        filename = os.path.basename(dest_path)
        name, ext = os.path.splitext(filename)
        
        # Find and remove all suffixed versions (_1, _2, etc.)
        suffixed_files = []
        for i in range(1, 1000):
            suffixed_file = os.path.join(base_dir, f"{name}_{i}{ext}")
            if os.path.exists(suffixed_file):
                suffixed_files.append(suffixed_file)
        
        # Remove suffixed files
        for suffixed_file in suffixed_files:
            try:
                os.remove(suffixed_file)
                logger.info(f"[{get_timestamp()}] 🗑️ Removed suffixed duplicate: {os.path.basename(suffixed_file)}")
            except Exception as e:
                logger.error(f"[{get_timestamp()}] ❌ Failed to remove suffixed file {suffixed_file}: {e}")
        
        logger.debug(f"[{get_timestamp()}] 🔄 Mode 4: Cleaned suffixed files, using original name: {filename}")
        return dest_path
    
    # Standard collision resolution for modes 1 and 3
    base_dir = os.path.dirname(dest_path)
    filename = os.path.basename(dest_path)
    name, ext = os.path.splitext(filename)
    
    counter = 1
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_dest_path = os.path.join(base_dir, new_filename)
        
        if not os.path.exists(new_dest_path):
            logger.debug(f"[{get_timestamp()}] 🔄 Collision resolved: {filename} → {new_filename}")
            return new_dest_path
        
        counter += 1
        if counter > 999:  # Safety limit
            logger.error(f"[{get_timestamp()}] ❌ Too many filename collisions for: {filename}")
            return None  # Return None to indicate failure

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def scan_folders(root_dir):
    """Scan and return list of first-level subfolders (folder-first isolation)."""
    logger = logging.getLogger(__name__)
    folder_list = []
    
    try:
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isdir(item_path) and not is_standard_subfolder(item):
                folder_list.append(item)
        
        logger.info(f"[{get_timestamp()}] 📁 Scanned folders: {len(folder_list)} found")
        return folder_list
        
    except Exception as e:
        logger.error(f"[{get_timestamp()}] ❌ Error scanning folders: {e}")
        return []

def find_matching_folder(filename, folder_list):
    """Find matching folder using priority-based matching system."""
    components = extract_filename_components(filename)
    name_only_normalized = normalize_name(components['name_only'])
    
    # Step 1: [FULL] Match - Exact folder name match
    for folder in folder_list:
        folder_normalized = normalize_name(folder)
        if name_only_normalized == folder_normalized:
            return folder, "FULL"
    
    # Step 2: [BASE+VER] Match - Folder contains basefit+version
    if components['basefit_version']:
        basefit_version_normalized = normalize_name(components['basefit_version'])
        for folder in folder_list:
            folder_normalized = normalize_name(folder)
            if basefit_version_normalized in folder_normalized:
                return folder, "BASE+VER"
    
    # Step 3: [BASE] Match - Folder contains basefit only
    if components['basefit']:
        basefit_normalized = normalize_name(components['basefit'])
        for folder in folder_list:
            folder_normalized = normalize_name(folder)
            if basefit_normalized in folder_normalized:
                return folder, "BASE"
    
    # Step 4: [NONE] - No match found
    return None, "NONE"

def move_file_safely(source_path, dest_path, match_type, allow_overwrite=False, dry_run=False):
    """Move file safely with comprehensive error handling."""
    logger = logging.getLogger(__name__)
    
    try:
        # Check if source and destination are the same
        if os.path.abspath(source_path) == os.path.abspath(dest_path):
            logger.info(f"[{get_timestamp()}] [{match_type}] ⚠️ Source equals destination, skipping: {source_path}")
            return "skipped"
        
        # Check if destination file already exists
        if os.path.exists(dest_path):
            if not allow_overwrite:
                # Check if files are identical
                if files_are_identical(source_path, dest_path):
                    logger.warning(f"[{get_timestamp()}] [{match_type}] ⚠️ Skipped duplicate during cleanup: {os.path.basename(source_path)}")
                else:
                    logger.warning(f"[{get_timestamp()}] [{match_type}] ⚠️ File already exists, skipping: {source_path}")
                return "skipped"
            else:
                if dry_run:
                    logger.info(f"[{get_timestamp()}] [{match_type}] 🔄 Would overwrite: {source_path} → {dest_path}")
                    return "would_overwrite"
                else:
                    logger.info(f"[{get_timestamp()}] [{match_type}] 🔄 Overwriting: {source_path} → {dest_path}")
        
        # Perform move operation
        if dry_run:
            logger.info(f"[{get_timestamp()}] [{match_type}] 📁 Would move: {source_path} → {dest_path}")
            return "would_move"
        else:
            shutil.move(source_path, dest_path)
            logger.info(f"[{get_timestamp()}] [{match_type}] 📁 Moved: {source_path} → {dest_path}")
            return "moved"
        
    except Exception as e:
        logger.error(f"[{get_timestamp()}] [{match_type}] ❌ Move failed: {source_path} → {dest_path} | Error: {e}")
        return "failed"

def collect_all_files_recursively(folder_path, cleanup_mode=False):
    """Recursively collect all files from subfolders. In cleanup mode, processes ALL subfolders."""
    logger = logging.getLogger(__name__)
    all_files = []
    all_folders = []
    
    def _collect_files_and_folders(current_path, relative_path=""):
        try:
            items = os.listdir(current_path)
            logger.debug(f"[{get_timestamp()}] 🔍 Scanning: {current_path} ({len(items)} items)")
            
            for item in items:
                item_path = os.path.join(current_path, item)
                relative_item_path = os.path.join(relative_path, item) if relative_path else item
                
                if os.path.isfile(item_path):
                    # Skip hidden/system files
                    if not is_hidden_or_system_file(item_path):
                        all_files.append({
                            'full_path': item_path,
                            'filename': item,
                            'relative_path': relative_item_path,
                            'source_folder': current_path
                        })
                        logger.debug(f"[{get_timestamp()}] 📄 Found file: {relative_item_path}")
                elif os.path.isdir(item_path):
                    # In cleanup mode, process ALL subfolders. Otherwise skip standard ones.
                    if cleanup_mode or not is_standard_subfolder(item):
                        all_folders.append(item_path)
                        logger.debug(f"[{get_timestamp()}] 📁 Found folder: {relative_item_path}")
                        _collect_files_and_folders(item_path, relative_item_path)
                    else:
                        logger.debug(f"[{get_timestamp()}] ⏭️ Skipping standard subfolder: {item}")
        except (OSError, PermissionError) as e:
            logger.error(f"[{get_timestamp()}] ❌ Error accessing {current_path}: {e}")
    
    _collect_files_and_folders(folder_path)
    logger.debug(f"[{get_timestamp()}] 📊 Collection complete: {len(all_files)} files, {len(all_folders)} folders")
    return all_files, all_folders

def cleanup_subfolders_recursively(folder_path, mode=3, dry_run=False):
    """Recursively cleanup ALL subfolders and move files to component folder.
    Mode 3: Skip conflicts, rename with suffixes if different
    Mode 4: Overwrite conflicts, remove suffixed duplicates"""
    logger = logging.getLogger(__name__)
    moved_count = 0
    skipped_count = 0
    allow_overwrite = mode == 4
    
    # Collect all files and folders from subfolders recursively (cleanup mode = process ALL folders)
    all_files, all_folders = collect_all_files_recursively(folder_path, cleanup_mode=True)
    
    if not all_files and not all_folders:
        logger.info(f"[{get_timestamp()}] 🧹 No files or subfolders found in: {os.path.basename(folder_path)}")
        return moved_count, skipped_count
    
    logger.info(f"[{get_timestamp()}] 🧹 Found {len(all_files)} files to move from subfolders")
    logger.debug(f"[{get_timestamp()}] 🧹 Found {len(all_folders)} subfolders to process")
    logger.debug(f"[{get_timestamp()}] 🎯 Cleanup Mode: {mode} ({'Overwrite' if allow_overwrite else 'Safe'})")
    
    # Check for root files that should take precedence
    root_files = set()
    try:
        for item in os.listdir(os.path.dirname(folder_path)):
            item_path = os.path.join(os.path.dirname(folder_path), item)
            if os.path.isfile(item_path):
                root_files.add(os.path.basename(item))
        logger.debug(f"[{get_timestamp()}] 🔍 Found {len(root_files)} files in root directory")
    except Exception as e:
        logger.debug(f"[{get_timestamp()}] 🔍 Could not scan root directory: {e}")
    
    # Move all collected files to the component folder
    for file_info in all_files:
        source_path = file_info['full_path']
        filename = file_info['filename']
        dest_path = os.path.join(folder_path, filename)
        
        # Check if file exists in root - if so, skip moving in Mode 3
        if mode == 3 and filename in root_files:
            logger.info(f"[{get_timestamp()}] 🔄 Mode 3: Keeping both files - root takes precedence: {filename}")
            skipped_count += 1
            continue
        
        # Handle filename collisions using the enhanced collision resolution function
        if os.path.exists(dest_path) and not files_are_identical(source_path, dest_path):
            resolved_path = resolve_filename_collision(dest_path, allow_overwrite, mode)
            if resolved_path is None:
                logger.error(f"[{get_timestamp()}] ❌ Too many collisions, skipping: {filename}")
                skipped_count += 1
                continue
            dest_path = resolved_path
        
        # Move file with enhanced logging
        result = move_file_safely(source_path, dest_path, "CLEANUP", allow_overwrite, dry_run)
        if result in ["moved", "would_move", "would_overwrite"]:
            moved_count += 1
        elif result == "skipped":
            skipped_count += 1
    
    # Sort folders by depth (deepest first) for proper deletion order
    all_folders.sort(key=lambda x: x.count(os.sep), reverse=True)
    logger.debug(f"[{get_timestamp()}] 🗂️ Processing {len(all_folders)} folders for deletion")
    
    # Delete empty folders (deepest first) - now includes standard subfolders in cleanup mode
    deleted_count = 0
    for folder_to_delete in all_folders:
        try:
            if dry_run:
                logger.info(f"[{get_timestamp()}] 🧹 Would delete subfolder: {folder_to_delete}")
                deleted_count += 1
            else:
                # Check if folder is truly empty (no files or subdirectories)
                try:
                    folder_contents = os.listdir(folder_to_delete)
                    if not folder_contents:
                        os.rmdir(folder_to_delete)
                        logger.info(f"[{get_timestamp()}] 🧹 Deleted subfolder: {folder_to_delete}")
                        deleted_count += 1
                    else:
                        # Check if it only contains empty directories
                        has_files = any(os.path.isfile(os.path.join(folder_to_delete, item)) 
                                      for item in folder_contents)
                        if not has_files:
                            # Try to delete anyway - might be empty subdirs
                            os.rmdir(folder_to_delete)
                            logger.info(f"[{get_timestamp()}] 🧹 Deleted subfolder: {folder_to_delete}")
                            deleted_count += 1
                        else:
                            logger.warning(f"[{get_timestamp()}] ⚠️ Folder not empty, skipping deletion: {folder_to_delete}")
                except OSError:
                    # Folder might have been deleted already or contains subdirs
                    logger.debug(f"[{get_timestamp()}] 🔍 Folder already processed or contains subdirs: {folder_to_delete}")
        except PermissionError as e:
            logger.error(f"[{get_timestamp()}] ❌ Failed to delete: {folder_to_delete} (Access Denied)")
        except Exception as e:
            logger.error(f"[{get_timestamp()}] ❌ Failed to delete: {folder_to_delete} ({str(e)})")
    
    logger.debug(f"[{get_timestamp()}] 📊 Cleanup summary: {moved_count} moved, {skipped_count} skipped, {deleted_count} folders deleted")
    return moved_count, skipped_count

def create_standard_folders(folder_path, dry_run=False):
    """Create standard subfolders if they don't exist."""
    logger = logging.getLogger(__name__)
    created_count = 0
    
    for folder_name in STANDARD_FOLDERS:
        subfolder_path = os.path.join(folder_path, folder_name)
        
        if not os.path.exists(subfolder_path):
            try:
                if dry_run:
                    logger.info(f"[{get_timestamp()}] ✅ Would create: {subfolder_path}")
                else:
                    os.makedirs(subfolder_path, exist_ok=True)
                    logger.info(f"[{get_timestamp()}] ✅ Created: {subfolder_path}")
                created_count += 1
            except Exception as e:
                logger.error(f"[{get_timestamp()}] ❌ Failed to create: {subfolder_path} | Error: {e}")
        else:
            logger.info(f"[{get_timestamp()}] ⚠️ Already exists: {subfolder_path}")
    
    return created_count

def sort_files_in_folder(folder_path, mode=1, dry_run=False):
    """Sort files within folder by extension into standard subfolders."""
    logger = logging.getLogger(__name__)
    moved_count = 0
    skipped_count = 0
    allow_overwrite = mode in [2, 4]
    
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Skip directories and hidden/system files
            if os.path.isdir(file_path) or is_hidden_or_system_file(file_path):
                continue
            
            # Get file extension
            _, ext = os.path.splitext(filename)
            ext_lower = ext.lower()
            
            # Find target subfolder based on extension
            target_subfolder = None
            for subfolder, extensions in EXTENSION_MAPPING.items():
                if ext_lower in extensions:
                    target_subfolder = subfolder
                    break
            
            # Move file if extension is supported
            if target_subfolder:
                dest_folder_path = os.path.join(folder_path, target_subfolder)
                dest_file_path = os.path.join(dest_folder_path, filename)
                
                # Handle filename collisions for extension-based sorting
                if os.path.exists(dest_file_path) and not files_are_identical(file_path, dest_file_path):
                    resolved_path = resolve_filename_collision(dest_file_path, allow_overwrite, mode)
                    if resolved_path is None:
                        logger.error(f"[{get_timestamp()}] ❌ Too many collisions, skipping: {filename}")
                        skipped_count += 1
                        continue
                    dest_file_path = resolved_path
                
                result = move_file_safely(file_path, dest_file_path, "EXT", allow_overwrite, dry_run)
                if result in ["moved", "would_move", "would_overwrite"]:
                    moved_count += 1
                elif result == "skipped":
                    skipped_count += 1
    
    except Exception as e:
        logger.error(f"[{get_timestamp()}] ❌ Error sorting files in {folder_path}: {e}")
    
    return moved_count, skipped_count

def process_root_files(root_dir, folder_list, mode=1, dry_run=False):
    """Process files in root directory using folder-first isolation."""
    logger = logging.getLogger(__name__)
    allow_overwrite = mode in [2, 4]
    
    stats = {
        'moved': 0,
        'skipped': 0, 
        'unmatched': 0,
        'failed': 0
    }
    
    try:
        for filename in os.listdir(root_dir):
            file_path = os.path.join(root_dir, filename)
            
            # Skip directories and hidden/system files
            if os.path.isdir(file_path) or is_hidden_or_system_file(file_path):
                continue
            
            # Check if file has supported extension
            _, ext = os.path.splitext(filename)
            if ext.lower() not in SUPPORTED_EXTENSIONS:
                logger.debug(f"[{get_timestamp()}] ⏭️ Skipping unsupported file: {filename}")
                continue
            
            # Find matching folder
            matched_folder, match_type = find_matching_folder(filename, folder_list)
            
            if matched_folder and match_type != "NONE":
                # Verify folder exists
                folder_path = os.path.join(root_dir, matched_folder)
                if os.path.exists(folder_path):
                    # Construct destination path
                    dest_path = os.path.join(folder_path, filename)
                    
                    # Handle filename collisions for regular file moves
                    if os.path.exists(dest_path) and not files_are_identical(file_path, dest_path):
                        resolved_path = resolve_filename_collision(dest_path, allow_overwrite, mode)
                        if resolved_path is None:
                            logger.error(f"[{get_timestamp()}] ❌ Too many collisions, skipping: {filename}")
                            stats['failed'] += 1
                            continue
                        dest_path = resolved_path
                    
                    # Move file
                    result = move_file_safely(file_path, dest_path, match_type, allow_overwrite, dry_run)
                    if result in ["moved", "would_move", "would_overwrite"]:
                        stats['moved'] += 1
                    elif result == "skipped":
                        stats['skipped'] += 1
                    elif result == "failed":
                        stats['failed'] += 1
                else:
                    logger.error(f"[{get_timestamp()}] ❌ Folder not found: {matched_folder}")
                    stats['unmatched'] += 1
            else:
                logger.warning(f"[{get_timestamp()}] [NONE] ⛔ No matching folder found for: {filename}")
                stats['unmatched'] += 1
    
    except Exception as e:
        logger.error(f"[{get_timestamp()}] ❌ Error processing root files: {e}")
    
    return stats

def execute_mode(mode, root_dir, folder_list, dry_run=False):
    """Execute the specified mode logic."""
    logger = logging.getLogger(__name__)
    
    total_stats = {
        'moved': 0,
        'skipped': 0,
        'unmatched': 0, 
        'failed': 0,
        'folders_created': 0,
        'cleanup_moved': 0
    }
    
    # Mode 3 & 4: Deep Cleanup phase
    if mode in [3, 4]:
        logger.info(f"[{get_timestamp()}] 🧹 Deep Cleanup Phase: Recursively flattening subfolders...")
        
        for folder_name in folder_list:
            folder_path = os.path.join(root_dir, folder_name)
            if os.path.exists(folder_path):
                logger.info(f"[{get_timestamp()}] 🧹 Processing cleanup for: {folder_name}")
                cleanup_moved, cleanup_skipped = cleanup_subfolders_recursively(
                    folder_path, mode, dry_run
                )
                total_stats['cleanup_moved'] += cleanup_moved
                total_stats['skipped'] += cleanup_skipped
    
    # All modes: Root File Sorter
    logger.info(f"[{get_timestamp()}] 🔄 Root File Sorter Phase...")
    rfs_stats = process_root_files(root_dir, folder_list, mode, dry_run)
    
    # Update total stats
    for key in ['moved', 'skipped', 'unmatched', 'failed']:
        total_stats[key] += rfs_stats[key]
    
    # All modes: Subfolder Structure Creation and File Sorting
    logger.info(f"[{get_timestamp()}] 🏗️ Subfolder Structure Phase...")
    
    for folder_name in folder_list:
        folder_path = os.path.join(root_dir, folder_name)
        
        if os.path.exists(folder_path):
            logger.info(f"[{get_timestamp()}] 📁 Processing subfolder: {folder_name}")
            
            # Create standard folders
            created_count = create_standard_folders(folder_path, dry_run)
            total_stats['folders_created'] += created_count
            
            # Sort files by extension
            moved_count, skipped_count = sort_files_in_folder(folder_path, mode, dry_run)
            total_stats['moved'] += moved_count
            total_stats['skipped'] += skipped_count
    
    return total_stats

def main():
    """Main function to orchestrate the folder fixing process."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Get execution mode
    mode = get_execution_mode(args)
    
    # Setup logging
    logger = setup_logging(args.log_dir, mode, args.dry_run, args.debug)
    start_time = time.time()
    
    # Get current directory
    root_dir = os.getcwd()
    
    logger.info(f"[{get_timestamp()}] 📂 Working directory: {root_dir}")
    
    # Safety prompt (unless disabled)
    if not args.no_prompt:
        dry_run_text = " (DRY RUN - No files will be modified)" if args.dry_run else ""
        print(f"\n{'='*80}")
        print(f"⚠️  WARNING: This script will organize files in the current directory{dry_run_text}")
        print(f"Mode: {mode} - {EXECUTION_MODES[mode]}")
        print("Press Enter to continue or Ctrl+C to cancel...")
        print("="*80)
        try:
            input()
        except KeyboardInterrupt:
            logger.info(f"[{get_timestamp()}] ❌ Script cancelled by user")
            return
    
    # Step 1: Folder-First Isolation - Scan all subfolders
    logger.info(f"[{get_timestamp()}] 📋 Step 1: Scanning subfolders...")
    folder_list = scan_folders(root_dir)
    
    # Step 2: Execute selected mode
    logger.info(f"[{get_timestamp()}] 🎯 Step 2: Executing Mode {mode}...")
    total_stats = execute_mode(mode, root_dir, folder_list, args.dry_run)
    
    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    duration_str = f"{int(duration//60):02d}:{int(duration%60):02d}"
    
    # Final summary
    dry_run_text = " (DRY RUN)" if args.dry_run else ""
    logger.info(f"[{get_timestamp()}] ✅ Script completed successfully!{dry_run_text}")
    logger.info(f"[{get_timestamp()}] 📊 Summary:")
    logger.info(f"[{get_timestamp()}]   • Mode executed: {mode} - {EXECUTION_MODES[mode]}")
    logger.info(f"[{get_timestamp()}]   • Files moved: {total_stats['moved']}")
    logger.info(f"[{get_timestamp()}]   • Files skipped: {total_stats['skipped']}")
    logger.info(f"[{get_timestamp()}]   • Files unmatched: {total_stats['unmatched']}")
    logger.info(f"[{get_timestamp()}]   • Move failures: {total_stats['failed']}")
    logger.info(f"[{get_timestamp()}]   • Folders created: {total_stats['folders_created']}")
    if total_stats['cleanup_moved'] > 0:
        logger.info(f"[{get_timestamp()}]   • Cleanup files moved: {total_stats['cleanup_moved']}")
    logger.info(f"[{get_timestamp()}]   • Duration: {duration_str}")
    
    log_location = args.log_dir if args.log_dir else "current directory"
    debug_text = " Debug logging was enabled." if args.debug else ""
    print(f"\n✅ Process completed!{dry_run_text} Check 'template_fixer_log.txt' in {log_location} for detailed logs.{debug_text}")
    print(f"📊 Files moved: {total_stats['moved']}, Skipped: {total_stats['skipped']}, Unmatched: {total_stats['unmatched']}")
    
    # Prevent auto-exit in .exe builds
    try:
        input("\nPress Enter to exit...")
    except (KeyboardInterrupt, EOFError):
        pass

# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
