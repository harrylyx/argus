# Argus

Argus is a modular data pipeline and control center built with Python and FastAPI. It features a plugin-based architecture where data sources ("plugins") can be dynamically discovered, managed, and monitored via a web dashboard.

**Repository:** [https://github.com/harrylyx/argus.git](https://github.com/harrylyx/argus.git)

## Features

*   **Plugin Architecture:** Easily extendable data sources managed by a central system.
*   **Web Dashboard:** Real-time monitoring of plugin health and status.
*   **Hot Reloading:** Automatic discovery of plugins on startup.
*   **API Control:** REST endpoints to toggle plugins and run health checks.

## Project Structure

*   `argus/`: Main package containing core logic, sources, and the web UI.
*   `argus/sources/`: Directory for plugin implementations.
*   `run.py`: Application entry point.

## Installation & Setup

1.  **Prepare Python Environment (using pyenv):**
    Ensure you have the desired Python version installed (e.g., 3.10+).
    ```bash
    pyenv install 3.10.13
    pyenv local 3.10.13
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the Application:**
    ```bash
    python run.py
    ```

2.  **Access the Dashboard:**
    Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Development

### Creating a New Plugin

To add a new data source to Argus:

1.  Create a new Python file in `argus/sources/`.
2.  Inherit from `BaseSource` and implement the required methods:
    ```python
    from argus.core.base import BaseSource, HealthStatus

    class MySource(BaseSource):
        name = "My New Source"
        description = "Fetches data from XYZ."

        async def run(self, pipeline_callback):
            while self.is_active:
                # Your logic here
                pass
    ```
3.  The `PluginManager` will automatically discover your new source upon restart.
