import sys
import os

# Add the app directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app/main.py"]
    sys.exit(stcli.main())
