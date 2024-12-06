.\" Set the title and date
.TL
snoatehusna
.AU
rsync - transfer files (over networks)

.SH 
DESCRIPTION
.PP
Rsync is a fast and versatile file copying tool used for transferring files and synchronizing directories across networks. 
Benefits over 'cp' include:
.IP
- Creating incremental backups
.IP
- Creating a 'partial' file for large transfers (
.B --partial
).
.IP
- Has the option to display transfer status (
.B --progress
).

.SH
USAGE
.PP
.B rsync
[-a] [-r] [--mkpath] [--rsh=remote_shell] [--delete] [--update] [--partial] [-P] [-z] source destination
.SH 
OPTIONS
.SH
.B -r
.PP
Recurse into directories.
.SH
.B --mkpath
.PP
Create the destination path if it does not exist.
.SH
.B -r
.PP
Recurse into directories.
.SH
.B --rsh=remote_shell
.PP
Specify the remote shell to use for communication.
.SH
.B --delete
.PP
Delete extraneous files from destination directories.
.SH
.B --update
.PP
Skip files that are newer on the receiver.
.SH
.B --partial
.PP
Save partially transferred files in case of an interrupt.
.SH
.B -P
.PP
Equivalent to 
.B --partial 
and 
.B
--progress
; show progress during transfer.
.SH
.B 
-z
.PP
Compress file data during the transfer.

.SH 
EXAMPLES
.SH
rsync -avz source/ destination/
.br
rsync --delete --update source/ destination/

.SH SEE ALSO
scp(1), sftp(1), rcp(1)
