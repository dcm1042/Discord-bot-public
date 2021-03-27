# Discord-bot
Repository for the UNHM programming club discord bot

### Google Cloud Address
34.68.101.38

* please contact bryan for first time login info (the best place to reach me is by text at: 603-260-2566)
* once logged in use the following to change your password:
    * `sudo passwd [USER]`

* repository can be found at /home/

### To access the running instance of the bot

    sudo screen -x bot

### Adding new modules (E.g. numpy)
    
    * add the name of the module to the text file pip_update
    * if multiple modules are added seperate them via newline

### Current Code Testing Procedures:
        * please check that the testing bot is currently offline before beginning
    1. change the variable 'testing' in bot.py to True
        * this changed the token to use the testing bot on the server
        * as well it changes the bot prefix to '?'
    2. run the bot.py script with the changes you're testing on
       your local machine
    3. once changes are confirmed working change 'testing' to False   
        * push your changes to the github page
    4. push to github (server will autodeploy update)
    
* see the discord.py api wrapper documentation:
    * `https://discordpy.readthedocs.io/en/latest/index.html`
    
    
### TODO:

