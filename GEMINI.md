# Argus

Argus is a modular data pipeline and control center built with Python and FastAPI. It features a plugin-based architecture where data sources ("plugins") can be dynamically discovered, managed, and monitored via a web dashboard.

**Repository:** [https://github.com/harrylyx/argus.git](https://github.com/harrylyx/argus.git)

## Project Structure

*   **`argus/`**: Root package.
    *   **`core/`**: Core system logic.
        *   `manager.py`: `PluginManager` handles discovery and lifecycle of plugins.
        *   `base.py`: Defines the `BaseSource` abstract class for all plugins.
        *   `pipeline.py`: (Assumed) Handles data processing from sources.
    *   **`sources/`**: Directory for plugin implementations. Any class here inheriting from `BaseSource` is automatically loaded.
    *   **`web_ui/`**: FastAPI web interface.
        *   `app.py`: Main application entry point and API routes.
        *   `templates/`: Jinja2 templates for the dashboard.
*   **`run.py`**: Entry point script to start the server.
*   **`requirements.txt`**: Python dependencies.

## Setup and Running

1.  **Prepare Python Environment (using pyenv):**
    Ensure you have the desired Python version installed via `pyenv`.
    ```bash
    pyenv install 3.10.x # (or your preferred version)
    pyenv local 3.10.x
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

4.  **Run the Application:**
    ```bash
    python run.py
    ```
    This starts the FastAPI server at `http://127.0.0.1:8000`.

3.  **Access Dashboard:**
    Open your browser to `http://127.0.0.1:8000` to view the control center.

## Development Guide

### Creating a New Plugin

To add a new data source to Argus:

1.  Create a new Python file in `argus/sources/` (e.g., `my_source.py`).
2.  Import `BaseSource` and `HealthStatus`:
    ```python
    from argus.core.base import BaseSource, HealthStatus
    ```
3.  Define a class inheriting from `BaseSource`:
    ```python
    class MySource(BaseSource):
        name = "My New Source"
        description = "Description of what this source does."

        async def run(self, pipeline_callback):
            # Main logic loop
            while self.is_active:
                data = fetch_data()
                await pipeline_callback(data)
                await asyncio.sleep(60)

        async def check_health(self) -> HealthStatus:
            # Implement health check logic
            return HealthStatus(is_healthy=True, latency_ms=10, last_success_time="now")

        async def dry_run(self):
            # Return sample data without side effects
            return {"sample": "data"}
    ```
4.  Restart the application. The `PluginManager` will automatically discover your new source.

### Architecture Notes

*   **Plugin Discovery:** Occurs automatically on application startup (`app.on_event("startup")` in `web_ui/app.py`).
*   **State Management:** Plugins are singletons managed by the `plugin_manager` instance.
