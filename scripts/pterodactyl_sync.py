#!/usr/bin/env python3
"""
Pterodactyl Server Synchronization & Deployment Script
Interacts with Pterodactyl Panel Client API hosted in Azure.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error

PTERO_URL = os.environ.get("PTERODACTYL_URL", "").rstrip("/")
PTERO_KEY = os.environ.get("PTERODACTYL_API_KEY", "")
SERVER_ID = os.environ.get("PTERODACTYL_SERVER_ID", "")

def make_request(endpoint, method="GET", data=None):
    if not PTERO_URL or not PTERO_KEY or not SERVER_ID:
        print("[ERROR] Faltan variables de entorno: PTERODACTYL_URL, PTERODACTYL_API_KEY o PTERODACTYL_SERVER_ID")
        sys.exit(1)
        
    url = f"{PTERO_URL}/api/client/servers/{SERVER_ID}{endpoint}"
    headers = {
        "Authorization": f"Bearer {PTERO_KEY}",
        "Content-Type": "application/json",
        "Accept": "Application/vnd.pterodactyl.v1+json",
        "User-Agent": "Maincrita-Deploy-Pipeline/1.0"
    }
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (200, 201):
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
            elif resp.status == 204:
                return {}
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        print(f"[ERROR API {e.code}] {url} -> {error_msg}")
        raise
    except urllib.error.URLError as e:
        print(f"[ERROR Conexión] No se pudo conectar a {PTERO_URL}: {e.reason}")
        raise

def send_console_command(cmd: str):
    print(f"[Pterodactyl] Ejecutando comando de consola: {cmd}")
    try:
        make_request("/command", method="POST", data={"command": cmd})
    except Exception as e:
        print(f"[WARN] No se pudo enviar comando (posiblemente el servidor esté apagado): {e}")

def create_backup(backup_name: str):
    print(f"[Pterodactyl] Creando respaldo de seguridad: '{backup_name}'...")
    try:
        res = make_request("/backups", method="POST", data={"name": backup_name})
        backup_uuid = res.get("attributes", {}).get("uuid", "desconocido")
        print(f"[Pterodactyl] Respaldo iniciado con UUID: {backup_uuid}")
        return backup_uuid
    except Exception as e:
        print(f"[WARN] No se pudo crear el respaldo automático: {e}")
        return None

def set_power_state(signal: str):
    print(f"[Pterodactyl] Enviando señal de energía: '{signal}'...")
    make_request("/power", method="POST", data={"signal": signal})

def get_server_state() -> str:
    res = make_request("/resources", method="GET")
    state = res.get("attributes", {}).get("current_state", "unknown")
    return state

def wait_for_state(target_state: str, timeout_seconds: int = 120):
    print(f"[Pterodactyl] Esperando a que el servidor alcance el estado '{target_state}' (timeout: {timeout_seconds}s)...")
    start = time.time()
    while time.time() - start < timeout_seconds:
        current = get_server_state()
        if current == target_state:
            print(f"[Pterodactyl] Estado alcanzado: {current}")
            return True
        time.sleep(5)
    print(f"[TIMEOUT] El servidor no alcanzó el estado '{target_state}' a tiempo.")
    return False

def deploy_sequence(branch_name: str):
    print("=" * 60)
    print(f"🚀 INICIANDO DESPLIEGUE AUTOMATIZADO - RAMA: {branch_name}")
    print("=" * 60)
    
    # 1. Notificación previa a los jugadores
    send_console_command(f"say [AVISO] Se detectaron cambios en la rama {branch_name}. Sincronizando mods...")
    send_console_command("say [AVISO] El servidor se detendrá en 10 segundos para aplicar la actualización...")
    time.sleep(10)
    
    # 2. Respaldo de seguridad
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    create_backup(f"pre-deploy-{branch_name}-{timestamp}")
    
    # 3. Apagado elegante
    set_power_state("stop")
    wait_for_state("offline", timeout_seconds=90)
    
    # 4. Sincronización de configuraciones
    print("[Pipeline] Sincronizando configuraciones de mods en el servidor...")
    # Aquí el pipeline de GitHub Actions / Azure DevOps transfiere los archivos via SFTP / API
    time.sleep(2)
    
    # 5. Encendido
    set_power_state("start")
    wait_for_state("running", timeout_seconds=180)
    
    print("=" * 60)
    print("✅ DESPLIEGUE FINALIZADO EXITOSAMENTE")
    print("=" * 60)

if __name__ == "__main__":
    branch = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REF_NAME", "main")
    deploy_sequence(branch)
