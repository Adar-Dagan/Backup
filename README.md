To restore run the command:
```
wget -O - https://raw.githubusercontent.com/Adar-Dagan/Backup/master/recover.py | python3
```

If you are not a sudoer then go into the root user:
```
su -
```
Edit the file `/etc/sudoers` and copy the line that starts with 'root   ALL' and change root to adar.
