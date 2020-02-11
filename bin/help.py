help = '''
NAME
       spc - A secure Personal cloud

SYNOPSIS
       secure personal cloud [ Xoption ...  ] [ file ...  ]

DESCRIPTION
       SPC is a secure personal cloud

       The  spc program is an advanced cloud storage system with high security. There
       is a  continuous sync beween the files ....open.

SPC COMMANDS
       $ spc config

       Displays the configured URL, username, and password of the client

       $ spc config edit

       Edits configuration and saves the changes
	   
	   $ spc version

       Shows the version number of the project

       $ spc server

       Shows information about the server

       $ spc signup

       Creates an account with given username and password

       $ spc view
      
       lists all the files in the cloud

       $ spc uploadfile <file-path>

       uploads the specified file into the cloud

       $ spc uploaddir <dir-path>

       uploads the specified directory to the cloud

       $ spc download <filename> <filepath>

       downloads the specified file from the cloud

       $ spc delete <filepath>+'/'+<filename>

       deletes the specified file in the cloud

       $ spc sync <dirpath>

       sync the specified directory with the cloud

       Implemented by team Access_Denied : Ramprasad Killari, Rohit Keerti Teja Patnala, Mahith Bonela


'''       
print(help)