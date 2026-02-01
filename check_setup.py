import sys
import os

# Add project root
sys.path.insert(0, os.getcwd())

from argus.core.manager import plugin_manager

print("Discovering plugins...")
plugin_manager.discover_plugins()
plugins = plugin_manager.get_all_plugins()
print(f"Found {len(plugins)} plugins.")
for name, plugin in plugins.items():
    print(f"- {name}: {plugin.description}")
