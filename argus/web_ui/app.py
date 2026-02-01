from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from argus.core.manager import plugin_manager
from argus.core.pipeline import pipeline

app = FastAPI(title="Argus Control Center")

# Locate templates directory relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

@app.on_event("startup")
async def startup_event():
    print("Argus starting up...")
    plugin_manager.discover_plugins()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    plugins = plugin_manager.get_all_plugins()
    # Pre-fetch health status for the dashboard
    plugin_data = []
    for name, plugin in plugins.items():
        health = await plugin.check_health()
        plugin_data.append({
            "name": name,
            "description": plugin.description,
            "is_active": plugin.is_active,
            "health": health
        })
    return templates.TemplateResponse("dashboard.html", {"request": request, "plugins": plugin_data})

@app.post("/api/plugins/{name}/toggle")
async def toggle_plugin(name: str):
    plugin = plugin_manager.get_plugin(name)
    if plugin:
        plugin.is_active = not plugin.is_active
        return {"status": "success", "is_active": plugin.is_active}
    return {"status": "error", "message": "Plugin not found"}

@app.get("/api/plugins/{name}/dry_run")
async def dry_run_plugin(name: str):
    plugin = plugin_manager.get_plugin(name)
    if plugin:
        result = await plugin.dry_run()
        return {"status": "success", "data": result}
    return {"status": "error", "message": "Plugin not found"}

@app.get("/api/plugins/{name}/health")
async def check_health(name: str):
    plugin = plugin_manager.get_plugin(name)
    if plugin:
        health = await plugin.check_health()
        return health
    return {"status": "error", "message": "Plugin not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
