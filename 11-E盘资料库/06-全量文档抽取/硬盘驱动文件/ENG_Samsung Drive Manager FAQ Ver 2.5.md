---
title: "ENG_Samsung Drive Manager FAQ Ver 2.5.pdf"
source_file: "硬盘驱动文件\Samsung Drive Manager Manuals\English\ENG_Samsung Drive Manager FAQ Ver 2.5.pdf"
type: 全量文档抽取
ext: ".pdf"
size_mb: "0.154"
modified: "2012-06-27"
is_backup: "否"
char_count: 9319
---

# 原文抽取：ENG_Samsung Drive Manager FAQ Ver 2.5.pdf

> 来源路径：`硬盘驱动文件\Samsung Drive Manager Manuals\English\ENG_Samsung Drive Manager FAQ Ver 2.5.pdf` ｜ 类型：.pdf ｜ 大小：0.154MB ｜ 修改：2012-06-27 ｜ 备份：否

```text
Samsung Drive Manager FAQ

Installation
Q: My Samsung External Hard Drive is connected but nothing is happening.
A: Check the USB cable connection. If your Samsung External Hard Drive is connected properly, its LED should light up.
A. A ticking noise from the hard disk means that power-supply is insufficient. If the hard disk is not recognized in the current USB port, try connecting it to another USB port.
Q. I am unable to install Samsung Drive Manager.
A: Check the minimum system requirements for using a Samsung External Hard Drive. Refer to the System Specifications in Chapter 1 of the User Manual for further information.
Q. The "User Account Control" window keeps appearing when I execute Samsung Drive Manager on Windows Vista. How can I stop the "User Account Control" window from appearing?
A. Elevation is required to use Samsung Drive Manager to directly or indirectly access an external hard disk. Use of Samsung Drive Manager is restricted if "User Account Control" access is not authorized. To stop

the "User Account Control" window from appearing, select User Account on the Control Panel and set Turn User Account Control Off.

Samsung AutoBackup
Q: What should I back up?
A. In general, data files generated from the use of other software should be backed up. Program files are not recommended for backup as programs must be reinstalled if your computer experiences an issue. Backup of data files that can be restored is recommended.
Q. How often should I back up data?
A. If you don't back up regularly, it is recommended that you back up important files, personal data such as pictures, and files that cannot be created again or are difficult to create.
Q. Some files were changed but real-time backup was not performed.
A. Samsung AutoBackup cannot perform real-time backup if a file not set as a backup source is changed. Make sure the file types you want backed up in realtime are set for real-time backup.
A. Another cause is a OS system file or folder being included in a backup source. Samsung AutoBackup cannot back up such files as they are used by the

system. Make sure that OS system folders or files are not included as a backup source.
Q. I use Samsung AutoBackup on Windows Vista or Windows 7 and backed up data and backup logs are not displayed.
A. This issue is caused by the User Account Control function introduced at the release of Windows Vista.
A HDD formatted as NTFS on Windows XP does not have the right
(Authenticated Users) granted when formatted on Windows Vista or Windows 7. If a HDD without this right is connected to Windows Vista or Windows 7 and used, backup data is not updated normally.
※ FAT32 is not affected by this issue.
Q. I have enough space on my Samsung External Hard Drive but I can't back up files bigger than 2GB or 4GB.
A. The maximum file size that can be backed up is dependent on the file system of your Samsung External Hard Drive.

Table 1: File System

File system type

Maximum backup file size

FAT FAT32 NTFS

2GB 4GB 16TB

A. To back up a file larger than 2GB, the file system must be changed to FAT32 or NTFS. To back up a file larger than 4GB, the file system must be changed to NTFS.
NOTE: ALL DATA STORED ON YOUR SAMSUNG EXTERNAL HARD DRIVE IS DELETED IF THE FILE SYSTEM IS CHANGED. BACK UP ALL IMPORTANT DATA TO ANOTHER HARD DISK
BEFORE CHANGING THE FILE SYSTEM.

Q. I formatted my computer and reinstalled Windows. How can I restore my backed up data on another device?
A. Install Samsung Drive Manager and execute Samsung AutoBackup and then select the data to restore on the Job List. Backed up data can be used this way (refer to Chapter 2 of the User Manual for further information). )

Q. After a backup failure, I checked the backup log and saw that multiple backup failures occurred.
A. OS system files cannot be accessed for backup. OS system files cannot be backed up. This issue is commonly experienced when a Windows folder or a "Program Files" folder is set as a backup source. To avoid this issue, do not set an entire root folder as a backup source. Set only user folders as backup sources.
A. Another way to avoid this issue is excluding the failed file as a backup source and performing backup again.

Q: I formatted by Samsung External Hard Disk and the Samsung software on it is deleted.

A. Samsung software provided with your Samsung

External Hard Disk can be downloaded from

Samsung's

customer

support

website.

(http://www.samsung.com/sec)

Q. I backed up a program that was installed when I installed a product. The product experienced an issue so I deleted the program and restored the backed up file but I am not able to execute the product. Have I done something wrong in the backup and restoration process?
A. All software programs require a certain environment to be executed. When a program is installed on a

computer, an environment is installed along with the program files and when the program is executed, the installed environment is tested. Because Samsung AutoBackup does not back up such an environment, such a program cannot be executed even after being backed up and restored.
Q: When Samsung AutoBackup is running, I can't remove my Samsung External Hard Disk using the "Safely Remove Hardware" function.
A. Samsung External Hard Disk cannot be safely removed when in use. Try again after closing Samsung AutoBackup.
Q: File transfers take too long.
A. If your computer doesn't support USB 2.0 or 3.0 or if your Samsung External Hard Disk is connected to a port other than a USB 2.0 or 3.0 port, file transfer speed is reduced. Connect your Samsung External Hard Disk to a port that supports USB 2.0 or higher.
Q. I am unable to copy files on my Macintosh computer.
A. File system compatibility may be an issue. If your Samsung External Hard Disk is formatted as NTFS, saved data can only be read on a Macintosh system.

Q: When I check my backup files on my backup device, I see a message saying "The file is not in proper format" and illegible files.
A. If Encrypted Backup was selected in backup settings, files are encrypted and backed up. When an encrypted file is opened, an error occurs or a message saying "The file is not in proper format" is displayed. An encrypted file must first be restored before being opened.
Q. I performed backup with the "Encrypt" option enabled. But only selected files were encrypted.
A. Only files backed up after Encrypt has been enabled are encrypted and backed up. Files backed up before Encrypt was enabled are not encrypted. This means that encrypted and non-encrypted files can exist on the same backup device.
Q: Can I connect a Samsung External Hard Disk containing backup data from another computer and restore the backup data? If so, how can I do it?
A. To restore and use data backed up from another computer, connect your Samsung External Hard Disk to the computer and install Samsung Drive Manager, then execute Samsung Auto Backup and select the backup file to restore.

Q: How can I check the results of backup, restoration or deletion?
A. After backup, restoration or deletion is completed, you can view the result in the "Log" shown on the job menu on the Samsung AutoBackup screen.

Samsung SecretZone
Q: How can I protect my Secure Drive from other users?
A: Select an image to protect on Samsung SecretZone and select "Disconnect." Other users cannot view the Secure Drive until "Connect" is selected by the administrator.
Q: How can I use my Secure Drive again after reinstalling the OS?
A: To use your Secure Drive again after reinstalling the OS, reinstall Samsung Drive Manager, connect your Samsung External Hard Disk, select the Secure Drive to use in Samsung SecretZone and click "Connect."
Q: What is the maximum Secure Drive size?
A: The size of a Secure Drive can be as large as the free space on your Samsung External Hard Disk.

Q: What should I do if I forget the password?
A: Samsung SecretZone is a security program and your Secure Drive cannot be used without the correct password. Make sure the password you set for your Secure Drive is one you can remember easily.
Q: While Samsung SecretZone is running, I can't remove my Samsung External Hard Disk using the Safely Remove Hardware function.
A: Disconnect all Secure Drives currently running, close Samusng SecretZone and then safely remove your Samsung External Hard Drive.

Q: After enabling "Auto Connection" on my Secure Drive, it won't connect.
A: Depending on your PC specifications, it can take some time to connect your Samsung External Hard Disk. Wait a moment until connection is established.
Q: An error message is displayed when I disconnect my Secure Drive.
A: An error can occur when your Secure Drive is disconnected immediately after copying or saving a large file or multiple files. If an error occurs, try again after 30 seconds to 1 minute.

Samsung Secure Manager
Q: Can I unlock my Samsung Secure Hard Disk without installing Samsung Drive Manager?
A: Connect your Samsung Secure Hard Disk, execute Secure Unlocker_win.exe in the CD drive displayed in "My Computer," and then enter the password to unlock.
A. Secure Unlock_mac.app must be executed on Macintosh. Q: What is the Factory Reset function?
A: The Factory Reset function deletes all data saved on your Secure Hard Disk and restores the default security settings.
```
