#!/usr/bin/env python3
import sys, os, getpass, traceback
import paramiko
from colorama import init as color_init, Fore, Style

color_init(autoreset=True)

def banner():
    # Banner Ilyox'SSH — tente pyfiglet, sinon fallback ASCII hardcodé
    try:
        import pyfiglet
        print(Fore.MAGENTA + Style.BRIGHT +
              pyfiglet.figlet_format("Ilyox'SSH", font="standard") +
              Style.RESET_ALL)
    except Exception:
        # Fallback ASCII (dessiné pour "Ilyox'SSH")
        print(Fore.MAGENTA + Style.BRIGHT + r"""
  ___ _       _                _____  _  ____  _  __
 |_ _| | __ _| |__   ___ _ __ |__  / / |/ ___|| |/ /
  | || |/ _` | '_ \ / _ \ '__|  / /  | | |    | ' / 
  | || | (_| | |_) |  __/ |    / /_  | | |___ | . \ 
 |___|_|\__,_|_.__/ \___|_|   /____| |_|\____||_|\_\
                                                    
        I l y o x ' S S H
""" + Style.RESET_ALL)
    print(Fore.CYAN + "=== Terminal SSH interactif ===\n" + Style.RESET_ALL)

def connect_ssh():
    host = input("👉 IP/host du serveur: ").strip()
    port = input("👉 Port SSH [22]: ").strip()
    port = int(port) if port else 22
    user = input("👉 Utilisateur SSH (ex: root): ").strip()
    use_key = input("👉 Utiliser une clé privée ? (y/N): ").strip().lower() == "y"

    password = None
    keyfile  = None
    if use_key:
        keyfile = input("👉 Chemin de la clé privée: ").strip()
    else:
        password = getpass.getpass("👉 Mot de passe SSH: ")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(Fore.YELLOW + f"\n[Connexion] {user}@{host}:{port} ..." + Style.RESET_ALL)
    if use_key:
        ssh.connect(host, port=port, username=user, key_filename=keyfile, timeout=20)
    else:
        ssh.connect(host, port=port, username=user, password=password, timeout=20)
    print(Fore.GREEN + "[OK] Connecté.\n" + Style.RESET_ALL)
    return ssh, user, host

def interactive_terminal(ssh, user, host):
    print(Fore.CYAN + "Tape tes commandes (exit pour quitter):\n" + Style.RESET_ALL)
    while True:
        try:
            cmd = input(Fore.YELLOW + f"{user}@{host}$ " + Style.RESET_ALL).strip()
            if cmd.lower() in ("exit", "quit"):
                print(Fore.MAGENTA + "Déconnexion..." + Style.RESET_ALL)
                break
            if not cmd:
                continue
            stdin, stdout, stderr = ssh.exec_command(cmd)
            for line in stdout:
                print(line.rstrip())
            for line in stderr:
                print(Fore.RED + line.rstrip())
        except KeyboardInterrupt:
            print("\n" + Fore.MAGENTA + "Déconnexion..." + Style.RESET_ALL)
            break

def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    ssh, user, host = connect_ssh()
    try:
        interactive_terminal(ssh, user, host)
    finally:
        try:
            ssh.close()
        except:
            pass
    input("\nAppuie sur Entrée pour fermer...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Affiche l'erreur SANS fermer la fenêtre
        print("\n" + Fore.RED + "‼️ Une erreur est survenue :" + Style.RESET_ALL)
        print(Fore.RED + "".join(traceback.format_exception(e)) + Style.RESET_ALL)
        input("\nAppuie sur Entrée pour fermer...")
