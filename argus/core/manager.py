import importlib
import pkgutil
import inspect
import os
import sys
from typing import Dict, Type
from argus.core.base import BaseSource

class PluginManager:
    def __init__(self, sources_package: str = "argus.sources"):
        self.sources_package = sources_package
        self.plugins: Dict[str, BaseSource] = {}

    def discover_plugins(self):
        """Scans the sources package for classes inheriting from BaseSource."""
        # Ensure the project root is in sys.path
        project_root = os.getcwd()
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        try:
            package = importlib.import_module(self.sources_package)
        except ImportError as e:
            print(f"Error importing sources package '{self.sources_package}': {e}")
            return

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            full_module_name = f"{self.sources_package}.{module_name}"
            try:
                module = importlib.import_module(full_module_name)
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) 
                        and issubclass(obj, BaseSource) 
                        and obj is not BaseSource):
                        
                        # Instantiate and register
                        instance = obj()
                        self.plugins[instance.name] = instance
                        print(f"Loaded plugin: {instance.name}")
            except Exception as e:
                print(f"Failed to load module {full_module_name}: {e}")

    def get_plugin(self, name: str) -> BaseSource:
        return self.plugins.get(name)

    def get_all_plugins(self) -> Dict[str, BaseSource]:
        return self.plugins

# Singleton instance
plugin_manager = PluginManager()
