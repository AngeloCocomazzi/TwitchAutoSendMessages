from TwitchWebsocket import TwitchWebsocket
import json, time, threading

from random import *
from statistics import mode

from tinydb import TinyDB,Query
from datetime import date

import keyboard

class Settings:
    def __init__(self, bot):
        try:
            # Try to load the file using json.
            # And pass the data to the MyBot class instance if this succeeds.
            with open("settings.txt", "r") as f:
                settings = f.read()
                data = json.loads(settings)
                bot.set_settings(data['Host'],
                                data['Port'],
                                data['Channel'],
                                data['Nickname'],
                                data['Authentication'])
        except ValueError:
            raise ValueError("Error in settings file.")
        except FileNotFoundError:
            # If the file is missing, create a standardised settings.txt file
            # With all parameters required.
            with open('settings.txt', 'w') as f:
                standard_dict = {
                                    "Host": "irc.chat.twitch.tv",
                                    "Port": 6667,
                                    "Channel": "#<channel>",
                                    "Nickname": "<name>",
                                    "Authentication": "oauth:<auth>"
                                }
                f.write(json.dumps(standard_dict, indent=4, separators=(',', ': ')))
                raise ValueError("Please fix your settings.txt file that was just generated.")

class TwitchSendMessage:

    global old_time,moda
    moda = ""
    old_time = time.time()

    global inp
    inp = []

    global listening_time
    listening_time = randint(15,30)

    global today #used for a database func
    today = date.today().strftime("%d/%m/%Y")# dd/mm/YY
    
    def __init__(self):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.sent = False
        
        #Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=["membership", "tags", "commands"],
                                  live=True)

        GetInput(self.ws)
        
        keyboard.add_hotkey('ctrl+alt+enter', lambda: self.analyzeData())
        #add hotkey -> stop bot and launch function analyzeData()

        self.ws.start_bot()


    def set_settings(self, host, port, chan, nick, auth):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth

    def isEmote(self,search_mex):
        
        emote = open("emote.txt", "r").readlines()#ottengo le emote dal file
        emote = list(filter(lambda a: a != '\n', emote))#rimuove le righe \n dalla lista

        emote = [s.replace("\n", "") for s in emote]#rimuove gli \n dalle stringhe nella lista
        #print(emote)

        if(search_mex in emote):
            return True
        else:
            return False

    def isBadWords(self,search_mex):#filter a bad word from mex
        
        bad_words = open("bad-words.txt", "r").readlines()#ottengo le parole dal file

        bad_words = [s.replace("\n", "") for s in bad_words]#rimuove gli \n dalle stringhe nella lista
        #print(bad_words)

        for words in bad_words:
            if(search_mex.strip(" ").find(words) != -1):#toglie gli spazi dalla stringa e cerca la bad_word nella stringa
                #print("\nParolaccia\n")
                return True

        return False


    def addInDatabase(self, m):
        
        global today

        try:
            db = TinyDB('db.json')

        except:
            print("File db non trovato")
            return False
        
        try:

            parse = json.dumps(m.tags)#take a dictionary as input and returns a string as output

            parse_mex = json.loads(parse)#parse tags from json to string
                                         #take a string as input and returns a dictionary as output.

            subscriber = parse_mex["subscriber"] #search a string with key subsciber and assign the value

            db.insert({'user': m.user, 'subscriber': subscriber,'message': m.message,'date': today})
            #insert data into db

        except:
            print("Errore nell'inserimento")
            
        finally:
            db.close()

    def isSubscriber(self,m):#function for filter sub and return sub mounth
        try:
            parse = json.dumps(m.tags)#take a dictionary as input and returns a string as output

            parse_mex = json.loads(parse)#take a string as input and returns a dictionary as output.

            info = parse_mex["badge-info"]
            #subscriber = parse_mex["subscriber"]#search a string with key subsciber and assign the value
            
            if (info == ''):
                return False
        
            elif (info.find("/") != -1):
                pos_mounth = info.find("/") + 1

                mounth_sub = info[pos_mounth:]#get mounth of sub

                return int(mounth_sub) #return True,mounth_sub

            else:
                return False

        except:
            print("Errore nel messaggio...")

        
    def avoidCharacter(self,search_mex):#function for avoid a specific chatacter

        characters = ["@","⣿"]

        for character in characters:
            index = 0
            while index < len(search_mex):
              if search_mex[index] == character:
                return True
              index = index + 1

        return False

    def avoidUsers(self,m):#function for avoid mex from specific user

        users = ["nightbot","streamelements","lolrankbot","giorgiob0t"]

        for user in users:
            if (m.user == user):
                return True

        return False

    def analyzeData(self):

        try:
            self.ws.stop()
            print("\nStopped\n")
        except:
            print("Impossbile fermare!")

        try:
            db = TinyDB('db.json')
            lenght = len(db)
            print ("Numero di messaggi : ",lenght)
            db.close()

        except:
            print("Errore nel file db")
        

    def message_handler(self, m):

        global old_time,inp,listening_time,moda

        filter_sub = 5 #variable used for filter message, can pass messages from subs older than 5 months
        max_lenght_message = 90
        
        if (m.type == "PRIVMSG" and m.message[0:3] != "/me" and
            self.avoidUsers(m) == False and m.message[0:1] != "!" and
            self.isBadWords(m.message) == False and
            self.avoidCharacter(m.message) == False and
            len(m.message) < max_lenght_message and
            self.isSubscriber(m) > filter_sub):
            #print(m)
            print("%s (%s) -> %s" %(m.user,self.isSubscriber(m),m.message))
            #print (user name) (number of mounth sub) (message send)

            try:
                text_split = m.message.split(" ")#GENERA ECCEZIONE SE NON TROVA SPAZI
                text_merged = ""

                for string in text_split:
                    
                    if text_merged == "":
                        text_merged = string
                    else:
                        if(self.isEmote(string)):
                            text_merged += " "
                            text_merged += string
                            inp.append(text_merged)
                            break
                        else:
                            text_merged += " "
                            text_merged += string

            except:
                text_split = m.message

            finally:
                inp.append(text_merged.strip())
                                  #strip() remove space from beginning and end
                #self.addInDatabase(m)

        #if for stamp mex in chat
        if(time.time() - old_time) > listening_time and len(inp) > 5:
            
            old_time = time.time()
            
            if(moda == mode(inp)):

                try:
                    new_list = [string for string in inp if string != moda or moda.find(string) == -1]

                    next_mex = randint(0,len(new_list)-1)
                
                    moda = new_list[next_mex]

                except:
                    moda = ""

            else:
                moda = mode(inp)#moda della lista
            
            print ("\n\n")
            print("Print moda: ",moda)
            print ("\n\n")
            
            self.ws.send_message(moda)#send message in chat
            time.sleep(1)#stop 1 sec
            
            listening_time = randint(20,40)
            inp.clear()#clear list

        #elif for reset timer and list when time expires
        elif(time.time() - old_time) > listening_time and len(inp) < 6:
            old_time = time.time()
            listening_time = randint(20,35)
            inp.clear()#clear list
            
        
class GetInput(threading.Thread):

    def __init__(self, ws):
        threading.Thread.__init__(self)
        self.name = "GetInput"

        self.ws = ws
        self.start()
        time.sleep(3)
        
    def run(self):
        pass
        #send = input(">")
        #self.ws.send_message(send)
        #print ("prova ",self.ws)
    
if __name__ == "__main__":
    TwitchSendMessage()
