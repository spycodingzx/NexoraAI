#!/usr/bin/env python3
"""
Quick setup script for .env configuration
"""

import os
from pathlib import Path


def nv_setup_env():
    """Interactive setup for .env file"""
    print("🚀 Autonomous Business Platform - Environment Setup")
    print("=" * 60)
    print()

    env_path = Path(".env")

    # Check if .env exists
    if env_path.exists():
        print(f"📄 Found existing .env file")
        overwrite = input("Overwrite? (y/N): ").strip().lower()
        if overwrite != "y":
            print("✅ Keeping existing .env. Edit it manually if needed.")
            return

    print()
    print("Let's set up your API tokens...")
    print()

    # Replicate token
    print("1️⃣  Replicate API Token")
    print("   Get yours at: https://replicate.com/account/api-tokens")
    replicate_token = input("   Enter token (or press Enter to skip): ").strip()

    print()

    # Printify token
    print("2️⃣  Printify API Token (optional)")
    print("   Get yours at: https://nv_printify.com/core/account/api")
    printify_token = input("   Enter token (or press Enter to skip): ").strip()

    # Create .env content
    env_content = f"""# Replicate API Token
# Get yours at: https://replicate.com/account/api-tokens
REPLICATE_API_TOKEN={replicate_token if replicate_token else 'your_replicate_token_here'}

# Printify API Token
# Get yours at: https://nv_printify.com/core/account/api
PRINTIFY_API_TOKEN={printify_token if printify_token else 'your_printify_token_here'}

# YouTube OAuth (paths will be set via Settings UI)
YOUTUBE_CLIENT_SECRET_PATH=
YOUTUBE_TOKEN_PATH=
"""

    # Write .env file
    with open(env_path, "w") as f:
        f.write(env_content)

    # Set permissions (read/write for owner only)
    os.chmod(env_path, 0o600)

    print()
    print("=" * 60)
    print("✅ .env file created successfully!")
    print(f"📍 Location: {env_path.absolute()}")
    print()

    if replicate_token:
        print("✅ Replicate token configured")
    else:
        print("⚠️  Replicate token not set - add it to .env manually")

    if printify_token:
        print("✅ Printify token configured")
    else:
        print("ℹ️  Printify token not set (optional)")

    print()
    print("🧪 Test your setup:")
    print("   python3 test_replicate_models.py")
    print()
    print("🚀 Start the core:")
    print("   streamlit run nova_system.py")
    print()


if __name__ == "__main__":
    try:
        nv_setup_env()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
