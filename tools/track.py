#!/usr/bin/env python3
"""
Campaign post tracker.

Tracks which posts have been generated and which have been posted to LinkedIn.
A POSTED marker file inside each Day folder records posting status.

Usage:
  python tools/track.py                  — show campaign status table
  python tools/track.py status           — same as above
  python tools/track.py post Day-1       — mark Day-1 as posted to LinkedIn
  python tools/track.py unpost Day-1     — unmark Day-1 (e.g. if posted by mistake)
"""

import glob
import os
import sys

OUTPUT_ROOT = "output"
POSTED_MARKER = "POSTED"


def find_day_folders():
    pattern = os.path.join(OUTPUT_ROOT, "Day-*")
    folders = [f for f in glob.glob(pattern) if os.path.isdir(f)]

    def sort_key(path):
        name = os.path.basename(path)
        try:
            return int(name.split("_")[0].replace("Day-", ""))
        except ValueError:
            return 999

    return sorted(folders, key=sort_key)


def has_txt(folder):
    return bool(glob.glob(os.path.join(folder, "*.txt")))


def has_image(folder):
    return bool(glob.glob(os.path.join(folder, "*.png")))


def is_posted(folder):
    return os.path.exists(os.path.join(folder, POSTED_MARKER))


def resolve_folder(day_arg):
    """Find the output folder matching 'Day-N' (with or without date suffix)."""
    # Try prefix match: Day-1_*
    matches = glob.glob(os.path.join(OUTPUT_ROOT, f"{day_arg}_*"))
    if matches:
        return matches[0]
    # Try exact match (user passed full folder name)
    exact = os.path.join(OUTPUT_ROOT, day_arg)
    if os.path.isdir(exact):
        return exact
    return None


def status():
    folders = find_day_folders()

    if not folders:
        print("\nNo campaign days found in output/. Draft your first post to get started.\n")
        return

    generated_count = len(folders)
    posted_count = sum(1 for f in folders if is_posted(f))
    pending_count = generated_count - posted_count

    print()
    print(f"  AI Access LinkedIn Campaign — Post Tracker")
    print(f"  {generated_count} generated  |  {posted_count} posted  |  {pending_count} pending")
    print()

    # Column widths: Day, Post, Visual, Status
    col = [8, 7, 8, 9]
    print(f"  {'Day':<{col[0]}}{'Post':<{col[1]}}{'Visual':<{col[2]}}{'Status':<{col[3]}}  Date")
    print("  " + "-" * 44)

    for folder in folders:
        name = os.path.basename(folder)
        parts = name.split("_", 1)
        day_label = parts[0]
        date_label = parts[1] if len(parts) > 1 else ""

        post_icon = "yes" if has_txt(folder) else "no"
        img_icon = "yes" if has_image(folder) else "no"
        status_label = "POSTED" if is_posted(folder) else "pending"

        print(
            f"  {day_label:<{col[0]}}"
            f"{post_icon:<{col[1]}}"
            f"{img_icon:<{col[2]}}"
            f"{status_label:<{col[3]}}  {date_label}"
        )

    print()


def mark_posted(day_arg):
    folder = resolve_folder(day_arg)
    if not folder:
        print(f"Error: no folder found matching '{day_arg}' in {OUTPUT_ROOT}/")
        print("Run 'python tools/track.py status' to see available days.")
        sys.exit(1)

    marker = os.path.join(folder, POSTED_MARKER)
    with open(marker, "w") as f:
        from datetime import datetime
        f.write(f"Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Marked as posted: {os.path.basename(folder)}")


def mark_unposted(day_arg):
    folder = resolve_folder(day_arg)
    if not folder:
        print(f"Error: no folder found matching '{day_arg}' in {OUTPUT_ROOT}/")
        sys.exit(1)

    marker = os.path.join(folder, POSTED_MARKER)
    if os.path.exists(marker):
        os.remove(marker)
        print(f"Unmarked: {os.path.basename(folder)}")
    else:
        print(f"'{os.path.basename(folder)}' was not marked as posted.")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd in ("status", "s"):
        status()
    elif cmd in ("post", "p"):
        if len(sys.argv) < 3:
            print("Usage: python tools/track.py post Day-1")
            sys.exit(1)
        mark_posted(sys.argv[2])
    elif cmd in ("unpost", "u"):
        if len(sys.argv) < 3:
            print("Usage: python tools/track.py unpost Day-1")
            sys.exit(1)
        mark_unposted(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: status, post Day-N, unpost Day-N")
        sys.exit(1)


if __name__ == "__main__":
    main()
