from flask import Flask, request, Response, jsonify
from dotenv import load_dotenv
import os 
from flask_pymongo import PyMongo
from messages import *
from utils import *
import re
import gridfs

""" 
Uncomment the below line for production  for pythonanywhere production and commit  the line : load_dotenv() 
and  vice vera for localhost
"""
#load_dotenv(os.path.join("/home/anton3richards/design_bot", '.env'))


load_dotenv()


MONGO_URI=os.getenv("MONGO_URI")
API_URL=os.getenv("API_URL")
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")



app= Flask(__name__)



app.secret_key = b'_m9y2L*79xQ8z\n\xec]/'

app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
db = mongo.db.bot
fs = gridfs.GridFS(mongo.db, collection = "files")

#------------------------------------------ document structure-------------------------------------------------------------------------------- #
structure={
            "design_type":"", 
            "design_list":"",
            "name_list":"",
            # "size":"",
            # "images":{
            #     "front":{"id":"","text":""},
            #     "back":{"id":"","text":""},
            # }


             }
# ------------------------------------------------------------------------------------------------------------------------------------------ #

allowed_extensions=["png", "jpg", "jpeg"]

@app.route('/')
def home():
  return "Ink Pen Bot Live 1.0"

@app.route("/webhook", methods=['GET'])
def connetwebhook():
    return "running whatsapp webhook"

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
        
        data=request.json
        try:
            
            number=data['waId']
            record=db.find_one({"_id":number})
            

            
            text=data['text']
               
            if data["type"]=="interactive":
                text =data['listReply']["title"]
                   
            
               
            if record is None :
                
                new_user={'_id':number, "state":"start", "order_count":0,"order_details":{"detail0":structure}}
    
                db.insert_one(new_user)
            
                send_reply_button(number, "Welcome to Inkpen Designs. What do you wanna Chat ?\n",design_type_reply_buttons)
            
                
            else:
                
                state=record["state"]
                
                
                if state=="start":
                    try:
                        if text not in ["Chat"] :
                            raise Exception
                        
                            
                        old_user={"$set":{"state":"design_list", f"order_details.detail{record['order_count']}.design_type":text}}
                        db.update_one({'_id':number},old_user)
                        

                        if text=="Chat":
                          send_list(number, text)

                        else:
                           send_list(number, text)  

                        send_reply_button(number, "Choose from above chat",design_list_reply_buttons)
                        
                            

                    except:

                        send_reply_button(number, "Please enter a valid input\n\nWhat do you wanna Chat ?",design_type_reply_buttons)
                    

                elif state=="design_list":
                    
                    try:
                         if text not in ["S","M","L","XL","XXL"] :
                                raise Exception
                         
                         old_user={"$set":{"state":"name",f"order_details.detail{record['order_count']}.design_list":text}}
                         db.update_one({'_id':number},old_user)
                         send_list(number,"What is your name", name_list)

                    except:
                         send_list(number,"Please enter a valid input\n\nKindly Select the design_list", design_list_reply_buttons)

                
                elif state=="name_list":
                    try: 
                         if text not in ["Rose","Lily","Tulip","Sunflower","Marigold"] :
                                raise Exception
                         
                         old_user={"$set":{"state":"end",f"order_details.detail{record['order_count']}.name_list":text}}
                         db.update_one({'_id':number},old_user)
                         

                    except :
                         send_list(number,"Please enter a valid input\n\nPlease Select the name", name_list)
                
                            
                elif  state=="end":
                    
                            order_count = record["order_count"]+1
                            old_user={"$set":{"state":"start","order_count": order_count,f"order_details.detail{order_count}":structure}}
                            db.update_one({'_id':number},old_user)

                            send_reply_button(number, "Welcome to Inkpen Designs. What do you wanna chat ?\n",design_type_reply_buttons)
                        
                    
                    
                else:
                    send_message(number,"Sorry! Can't understand !!")

                #return 'processing' 
        
        except Exception as e:
            print(e)
            print("message sent")       
         
    
  
        return 'processing'   


if __name__ == '__main__':
    app.run(debug=True) 