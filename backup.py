import yaml
import datetime
import os
import subprocess

dotfiles_repo_path = "/temp_dotfiles"
backup_repo_path = "/temp_backup"

def backup():
    print("Starting backup")

    print("Cloning dotfiles repo")
    ret = subprocess.call(['git', 'clone', 'https://github.com/Adar-Dagan/dotfiles.git', dotfiles_repo_path])
    if ret != 0:
        print("Failed to clone dotfiles repo")
        return 

    print("Cloning backup repo")
    ret = subprocess.call(['git', 'clone', 'https://github.com/Adar-Dagan/Backup.git', backup_repo_path])
    if ret != 0:
        print("Failed to clone backup repo")
        return

    os.chdir(dotfiles_repo_path)

    programs = os.listdir('./programs')

    for program in programs:
        file_path = f"./programs/{program}"
        
        print("Running " + program + " script")
        ret = subprocess.call(['python3', file_path, 'restore', dotfiles_repo_path])
        if ret != 0:
            print(f"{program} script failed")
            return

    print("Creating program list yaml file")
    with open("programs.yaml", "w") as f:
        yaml.dump(programs, f)

    print("Adding and commiting changes in backup repo")
    subprocess.call(['git', 'add', '-A'])
    subprocess.call(['git', 'commit', '-m', 'yaml file update'])
    subprocess.call(['git', 'push'])

    print("Adding and commiting changes in dotfiles repo")
    os.chdir(backup_repo_path)
    subprocess.call(['git', 'add', '-A'])
    subprocess.call(['git', 'commit', '-m', f'Backup {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
    subprocess.call(['git', 'push'])

def cleanup():
    print("Removing temp files")
    subprocess.call(['rm', '-rf', dotfiles_repo_path])
    subprocess.call(['rm', '-rf', backup_repo_path])

if __name__ == "__main__":
    try:
        backup()
    except Exception as e:
        print(e)

    cleanup()

