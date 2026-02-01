import uvicorn
import os
import sys

if __name__ == "__main__":
    # Add project root to sys.path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    print(f"Starting Argus from {project_root}")
    uvicorn.run("argus.web_ui.app:app", host="127.0.0.1", port=8000, reload=True)
