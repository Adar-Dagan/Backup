import subprocess
import os
import urllib.request
import yaml

dotfiles_repo_path = "/home/adar/temp_dotfiles"

def restore():
    print("Starting restore")

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

    print("Getting program list yaml file")
    url = "https://raw.githubusercontent.com/Adar-Dagan/Backup/master/programs.yaml"
    yaml_file = urllib.request.urlopen(url)
    programs = yaml.safe_load(yaml_file)

    for program in programs:
        url = f"https://raw.githubusercontent.com/Adar-Dagan/Backup/master/programs/{program}"
        script = urllib.request.urlopen(url)
        script = script.read().decode("utf-8")
        
        print("Running " + program + " script")
        ret = subprocess.call(['python3', '-c', script, 'restore', dotfiles_repo_path])
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
    subprocess.call(['rm', '-rf', dotfiles_repo_path])

if __name__ == "__main__":
    try:
        restore()
    except Exception as e:
        print(e)

    cleanup()



