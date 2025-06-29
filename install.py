#!/usr/bin/env python3
"""
Simple installation script for FixtureGPT
"""

import os
import sys
import shutil
import site
from pathlib import Path

def install_fixturegpt():
    """Install FixtureGPT to Python site-packages."""
    print("🚀 Installing FixtureGPT...")
    
    # Get the current directory (where fixturegpt package is)
    current_dir = Path(__file__).parent
    fixturegpt_dir = current_dir / "fixturegpt"
    
    if not fixturegpt_dir.exists():
        print("❌ Error: fixturegpt directory not found!")
        return False
    
    # Get site-packages directory
    site_packages = Path(site.getsitepackages()[0])
    target_dir = site_packages / "fixturegpt"
    
    try:
        # Remove existing installation if it exists
        if target_dir.exists():
            shutil.rmtree(target_dir)
            print("🧹 Removed existing installation")
        
        # Copy the package
        shutil.copytree(fixturegpt_dir, target_dir)
        print(f"📦 Copied FixtureGPT to {target_dir}")
        
        # Install CLI script
        install_cli_script()
        
        print("✅ FixtureGPT installed successfully!")
        print("\n💡 Usage:")
        print("  from fixturegpt import snapshot")
        print("  result = snapshot('name', your_function, *args, **kwargs)")
        print("\n🔧 CLI Commands:")
        print("  fixturegpt stats")
        print("  fixturegpt diff 'name'")
        print("  fixturegpt clear")
        
        return True
        
    except PermissionError:
        print("❌ Permission denied. Try running with sudo:")
        print("  sudo python install.py")
        return False
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def install_cli_script():
    """Install the CLI script to make 'fixturegpt' command available."""
    try:
        # Create a simple CLI script
        cli_script = '''#!/usr/bin/env python3
import sys
from fixturegpt.cli import app

if __name__ == "__main__":
    app()
'''
        
        # Find a suitable directory for the script
        script_dirs = [
            Path("/usr/local/bin"),
            Path(os.path.expanduser("~/.local/bin")),
            Path(sys.prefix) / "bin"
        ]
        
        for script_dir in script_dirs:
            if script_dir.exists():
                script_path = script_dir / "fixturegpt"
                with open(script_path, 'w') as f:
                    f.write(cli_script)
                os.chmod(script_path, 0o755)
                print(f"🔧 Installed CLI script to {script_path}")
                break
        else:
            print("⚠️  Could not install CLI script - add to PATH manually")
            
    except Exception as e:
        print(f"⚠️  CLI script installation failed: {e}")

def main():
    """Main installation function."""
    print("🎯 FixtureGPT Installation Script")
    print("=" * 50)
    
    if install_fixturegpt():
        print("\n🎉 Installation complete!")
        print("Try: python -c 'from fixturegpt import snapshot; print(\"FixtureGPT ready!\")'")
    else:
        print("\n❌ Installation failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 