import os
import re
import sys
import json
import urllib.request
from urllib.parse import urljoin, unquote
from datetime import datetime

INFO_PAGE_URL = "https://jyskblueline.com/powerpoint-presentations"
BASE_URL = "https://jyskblueline.com"
ASSETS_DIR = "/Users/mojoaar/AI/skills/new-jysk-pptx/assets"
VERSION_FILE = os.path.join(ASSETS_DIR, "version.json")

def load_version_info():
    """Loads the currently installed template URLs and last update timestamp."""
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "indoor_url": "https://jyskblueline.com/sites/default/files/inline-files/JYSK%20indoor%20FY26_updated_0.pptx",
        "outdoor_url": "https://jyskblueline.com/sites/default/files/inline-files/JYSK%20outdoor%20FY26.pptx",
        "last_updated": "2026-06-18T10:00:00Z"
    }

def save_version_info(info):
    """Saves the template version info to version.json."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    with open(VERSION_FILE, "w") as f:
        json.dump(info, f, indent=2)

def fetch_blueline_links():
    """Fetches the JYSK Blueline PP page and extracts all PPTX template links."""
    print(f"Fetching JYSK Blue Line from {INFO_PAGE_URL}...")
    try:
        req = urllib.request.Request(
            INFO_PAGE_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        return None, None

    # Parse all .pptx URLs from hrefs or inline text
    # Standard format: href="/sites/default/files/inline-files/..."
    links = re.findall(r'href="([^"]+\.pptx)"', html)
    
    indoor_link = None
    outdoor_link = None
    
    for link in links:
        full_url = urljoin(BASE_URL, link)
        decoded_name = unquote(link).lower()
        if "indoor" in decoded_name:
            indoor_link = full_url
        elif "outdoor" in decoded_name:
            outdoor_link = full_url
            
    return indoor_link, outdoor_link

def download_file(url, target_path):
    """Downloads a file from a URL to the target path."""
    print(f"Downloading {url} -> {target_path}...")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=30) as r, open(target_path, 'wb') as f:
            f.write(r.read())
        return True
    except Exception as e:
        print(f"Error downloading file: {e}", file=sys.stderr)
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="JYSK PowerPoint Templates Update Tool")
    parser.add_argument("--check", action="store_true", help="Check for updates without downloading")
    parser.add_argument("--update", action="store_true", help="Download new templates if updates are found")
    parser.add_argument("--force", action="store_true", help="Force download templates even if they are unchanged")
    args = parser.parse_args()

    if not args.check and not args.update and not args.force:
        parser.print_help()
        sys.exit(0)

    # 1. Load current version
    curr_info = load_version_info()
    
    # 2. Scrape Blue Line
    new_indoor, new_outdoor = fetch_blueline_links()
    
    if not new_indoor or not new_outdoor:
        print("Warning: Could not parse templates from JYSK Blue Line website. Falling back to default check.")
        new_indoor = new_indoor or curr_info.get("indoor_url")
        new_outdoor = new_outdoor or curr_info.get("outdoor_url")

    # 3. Compare
    indoor_updated = (new_indoor != curr_info.get("indoor_url"))
    outdoor_updated = (new_outdoor != curr_info.get("outdoor_url"))
    
    print("\n--- JYSK PowerPoint Template Status ---")
    print(f"Currently configured Indoor:  {curr_info.get('indoor_url')}")
    print(f"Blue Line online Indoor:      {new_indoor} " + ("(UPDATE AVAILABLE)" if indoor_updated else "(Up-to-date)"))
    
    print(f"\nCurrently configured Outdoor: {curr_info.get('outdoor_url')}")
    print(f"Blue Line online Outdoor:     {new_outdoor} " + ("(UPDATE AVAILABLE)" if outdoor_updated else "(Up-to-date)"))
    
    has_updates = indoor_updated or outdoor_updated

    if args.check:
        if has_updates:
            print("\nUpdates are available! Run with --update to download and install them.")
        else:
            print("\nAll templates are up to date with JYSK Blue Line.")
        sys.exit(0)

    # 4. Perform Download / Update
    if has_updates or args.force:
        print("\nProceeding with template update...")
        os.makedirs(ASSETS_DIR, exist_ok=True)
        
        updated_info = curr_info.copy()
        success = True
        
        if indoor_updated or args.force:
            target = os.path.join(ASSETS_DIR, "jysk_indoor.pptx")
            if new_indoor and download_file(new_indoor, target):
                updated_info["indoor_url"] = str(new_indoor)
            else:
                success = False
                
        if outdoor_updated or args.force:
            target = os.path.join(ASSETS_DIR, "jysk_outdoor.pptx")
            if new_outdoor and download_file(new_outdoor, target):
                updated_info["outdoor_url"] = str(new_outdoor)
            else:
                success = False
                
        if success:
            updated_info["last_updated"] = datetime.now().isoformat() + "Z"
            save_version_info(updated_info)
            print("\nSuccess: JYSK PowerPoint templates successfully updated and synced!")
        else:
            print("\nError: One or more template downloads failed. Please try again later.", file=sys.stderr)
            sys.exit(1)
    else:
        print("\nNothing to update. Templates are already in sync with JYSK Blue Line.")

if __name__ == "__main__":
    main()
