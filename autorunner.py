"""
Very Crude Implementation of github webhooks to allow automatic updating
"""

from flask import Flask
from flask import request
from subprocess import Popen
import os
import time


app = Flask(__name__)

bot = Popen(['python3.7','bot.py'])


@app.route('/update', methods=['POST'])
def update():
    global bot
    bot.terminate()
    os.system('sudo git pull https://brobbins2001:5b0c213a170ec92e01d85381c05f55dc51342c5b@github.com/unhm-programming-team/Discord-bot')
    f = open("pip_update.txt", "r")
    for each in f.readlines():
        os.system(f'pip3 install {each}')
    bot = Popen(['python3.7', 'bot.py'])
    return' 200'





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
