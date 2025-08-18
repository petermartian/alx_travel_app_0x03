#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def main():
    # Ensure project root on sys.path
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE_DIR))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
