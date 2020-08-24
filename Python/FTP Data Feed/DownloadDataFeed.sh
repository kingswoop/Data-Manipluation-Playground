#!/usr/local/bin/


date=`date '+%Y_%m_%d'`
datefile="_$date"

USER=''
PASSWD=''
TARGDIR='ftp://##addFTPaddress'

ftpsrv="ftp://##addFTPaddress"
declare -A brands 


######################################
###         ADD Tag + LINK         ###
######################################
brands=(
	##Add files for download
  ##EG
  ['##TAG']='##FileName'
)




for file in "${!brands[@]}";
						do
							
              # Get file
							wget --user=$USER --password=$PASSWD $ftpsrv${brands[$file]}
              
              # Copy file to log location
							cp ${brands[$file]} file_log/${brands[$file]}$datefile.txt.gz
              
              #Unzip file
							gunzip -f ${brands[$file]}
							filenm=${brands[$file]}
							unzipfile=${brands[$file]%.*}
							sed '1d' $unzipfile > $unzipfile.cp
							rm $unzipfile
							mv ./$unzipfile.cp ./$unzipfile
							newfile=${unzipfile}
              
              # Move to Python Script for ingestion
							cp "$newfile" "../00_upload/importfiles/$file.txt"
							


						done
