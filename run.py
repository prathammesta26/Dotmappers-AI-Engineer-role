import os
import subprocess
import sys
import time

def main():
    print("=" * 60)
    print(" Starting AI Support Ticket Intelligence Platform ")
    print(" DOTMappers AI Engineer Technical Assessment ")
    print("=" * 60)

    # 1. Start the FastAPI backend server (Port 8000)
    print("\n[1/2] Launching FastAPI backend at http://127.0.0.1:8000 ...")
    api_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
    ]
    api_process = subprocess.Popen(api_cmd)

    # Allow FastAPI and SQLite database initialization time
    print("Waiting for database and API startup...")
    time.sleep(3)

    # 2. Start the Streamlit UI dashboard (Port 8501)
    print("\n[2/2] Launching Streamlit dashboard at http://127.0.0.1:8501 ...")
    ui_cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "ui.py",
        "--server.port",
        "8501",
        "--server.headless",
        "false"
    ]
    ui_process = subprocess.Popen(ui_cmd)

    print("\n" + "=" * 60)
    print(" System is running!")
    print(" - Swagger API Docs: http://127.0.0.1:8000/docs")
    print(" - Streamlit Web UI: http://127.0.0.1:8501")
    print(" Press Ctrl+C at any time to shut down both servers.")
    print("=" * 60 + "\n")

    try:
        api_process.wait()
        ui_process.wait()
    except KeyboardInterrupt:
        print("\nTerminating background services...")
        api_process.terminate()
        ui_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()