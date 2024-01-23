import subprocess
import os
import urllib.request
import yaml

backup_repo_path = "/home/adar/temp_backup"
dotfiles_repo_path = "/home/adar/temp_dotfiles"

def restore():
    print("Starting recovery")

    print("Updating apt")
    url = "https://raw.githubusercontent.com/Adar-Dagan/Backup/master/apt_setup"
    script = urllib.request.urlopen(url)
    script = script.read().decode("utf-8")
    ret = subprocess.call(['bash', '-c', script])
    if ret != 0:
        print("Failed to update apt")
        return

    print("Installing git")
    ret = subprocess.call(['sudo', 'apt', '-y', 'install', 'git'])
    if ret != 0:
        print("Failed to install git")
        return

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

    print("Changing to directory to backup repo")
    os.chdir(backup_repo_path)

    print("Getting programs to install")
    programs = os.listdir("./programs")

    print("Installing programs")
    for program in programs:
        file_path = f"./programs/{program}"
        
        print("Running " + program + " script")
        ret = subprocess.call(['bash', file_path, 'recover', dotfiles_repo_path])
        if ret != 0:
            print(f"{program} script failed")
            return

    print("Setting up anacron job")
    period = "7"  # This means the job will run every week
    delay = "5"  # This means the job will start 5 minutes after anacron is run
    job_identifier = "backup_job"
    command = "wget -O - https://raw.githubusercontent.com/Adar-Dagan/Backup/master/backup.py | python3"  

    # Create the anacron job
    os.system(f'echo "{period} {delay} {job_identifier} {command}" | sudo tee -a /etc/anacrontab')


def cleanup():
    print("Removing temp files")
    try:
        subprocess.call(['rm', '-rf', dotfiles_repo_path])
    except Exception as e:
        print(e)

    try:
        subprocess.call(['rm', '-rf', backup_repo_path])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        restore()
    except Exception as e:
        print(e)

    cleanup()



