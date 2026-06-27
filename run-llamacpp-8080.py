import os
import subprocess
import sys

def launch_server():
    # 1. Ensure dependencies are present
    try:
        import huggingface_hub
        import llama_cpp
    except ImportError:
        print("📦 Installing required packages...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "llama-cpp-python[server]", "huggingface-hub"
        ])

    from huggingface_hub import hf_hub_download
    
    # 2. Read Environment Variables
    repo_id = os.environ.get("MODEL_REPO", "bartowski/Llama-3.2-3B-Instruct-GGUF")
    filename = os.environ.get("MODEL_FILE", "Llama-3.2-3B-Instruct-Q4_K_M.gguf")
    threads = os.environ.get("LLAMA_THREADS", "4")
    context = os.environ.get("MODEL_CONTEXT_WINDOW", "2048")
    
    # Dynamic Port Handling: Reads 'APP_PORT' env var that is automatically created by CAI-I Apps, defaults to '8080'
    listening_port = os.environ.get("APP_PORT", "8080")

    print(f"🔄 Ensuring model cache is ready: {repo_id}/{filename}")
    model_path = hf_hub_download(repo_id=repo_id, filename=filename)

    # 3. Build execution command for the server backend
    cmd = [
        sys.executable, "-m", "llama_cpp.server",
        "--model", model_path,
        "--n_threads", str(threads),
        "--n_ctx", str(context),
        "--host", "0.0.0.0",       # Required to accept external cluster traffic
        "--port", str(listening_port)  # Fed directly from your ENV VAR
    ]
    
    print(f"📡 Launching API engine on host 0.0.0.0, port: {listening_port}...")
    
    # 4. Hand off execution to the server process
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server shut down gracefully.")

if __name__ == "__main__":
    launch_server()