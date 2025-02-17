#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pathlib import Path
import sys
import os
from IPython import get_ipython

# this is needed if you play notebook in vscode
# by calling `common.setup()`
def setup():
    # Get the current notebook path using IPython's get_ipython()
    kernel = get_ipython()
    notebook_path = kernel.config.get('NotebookApp', {}).get('notebook_dir', os.getcwd())
    # project base dir
    BASE_DIR = Path(notebook_path).resolve().parent
    if str(BASE_DIR) not in sys.path:
        sys.path.append(f"{BASE_DIR}")

