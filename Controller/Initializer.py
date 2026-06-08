import pkgutil
import sys
import importlib
from pathlib import Path

# Dynamically find out if this file lives in 'Services' or 'Controller'
CURRENT_PACKAGE = Path(__file__).parent.name 
ModulesPackage = importlib.import_module(f"{CURRENT_PACKAGE}.Modules")

class Init:
    @classmethod
    def load(cls):
        package_path = ModulesPackage.__path__
        modules_found = []
        
        for _, module_name, _ in pkgutil.iter_modules(package_path):
            modules_found.append(module_name)
            full_module_name = f"{CURRENT_PACKAGE}.Modules.{module_name}"
            
            if full_module_name not in sys.modules:
                importlib.import_module(full_module_name)
                
            module = sys.modules[full_module_name]
            
            if hasattr(module, "Init"):
                module.Init(ModulesPackage)

        cls._generate_stub(modules_found)
        return ModulesPackage

    @classmethod
    def _generate_stub(cls, modules):
        stub_path = Path(__file__).parent / "Initializer.pyi"
        
        # Build the stub file using the dynamic package name instead of hardcoded 'Services'
        stub_structure = [f"import {CURRENT_PACKAGE}.Modules as ModulesPackage"]
        for m in modules:
            stub_structure.insert(0, f"import {CURRENT_PACKAGE}.Modules.{m} as {m}")
            
        stub_structure.extend(["", "class ServiceRegistry:"])
        for m in modules:
            stub_structure.append(f"    @property\n    def {m}(self) -> {m}: ...")
            
        stub_structure.extend(["", "class Init:", "    @classmethod", "    def load(cls) -> ServiceRegistry: ..."])
        
        output = "\n".join(stub_structure)
        if not stub_path.exists() or stub_path.read_text() != output:
            stub_path.write_text(output)