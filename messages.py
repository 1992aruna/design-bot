import requests
import json
from app import API_URL, ACCESS_TOKEN
import os
import gridfs
from dotenv import load_dotenv



""" 
Uncomment the below line for production  for pythonanywhere production and commit  the line : load_dotenv() 
and  vice vera for localhost
"""
#load_dotenv(os.path.join("/home/anton3richards/design_bot", '.env'))

load_dotenv()

API_URL=os.getenv("API_URL")
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")


def send_message(contact_number, message):
	headers = {
					'Authorization': ACCESS_TOKEN,
				}
	payload={'messageText': message}

	url = f"{API_URL}/api/v1/sendSessionMessage/"+ f'{contact_number}'
	response = requests.post(url=url, headers=headers,data=payload)
	return response.status_code

def send_image_message(contact_number,image, caption):
    url = f"{API_URL}/api/v1/sendSessionFile/{contact_number}?caption={caption}"

    payload = {}
    files=[
    ('file',('file',open(image,'rb'),'image/jpeg'))
    ]
    headers = {
    'Authorization': ACCESS_TOKEN
    }

    response = requests.post(url, headers=headers, json=payload, files=files)
    print(response)
    print(response.json())

##-------------------------------- Customized image message sending -----------------------------------------------------------------------------   ##

def send_images(contact_number,option):
    dir="C:/Users/jmdee/upwork/Design Chatbot/images"
    if option =="Shirt":
        image1=f'{dir}/s_image1.png'
        image2=f'{dir}/s_image2.png'
        

    else:
        image1=f'{dir}/ts_image1.jpg'
        image2=f'{dir}/ts_image2.jpg'
       
        
    send_image_message(contact_number,image1, "Image1")
    send_image_message(contact_number,image2, "Image2")

## ------------------------------------- --------------------------------------------------------------------------------------------------------##         
        

    

def send_reply_button(contact_number, message, buttons):
    payload = {
    
    "body": message,
    "buttons": buttons
    }

    url = f"{API_URL}/api/v1/sendInteractiveButtonsMessage?whatsappNumber="+f"{contact_number}"
    headers = {
                'Authorization': ACCESS_TOKEN,
                'Content-Type': 'application/json'
            }
    response = requests.request("POST", url, headers=headers, json=payload)
    return response.status_code

def send_list(contact_number, message, sections):
    url = f"{API_URL}/api/v1/sendInteractiveListMessage?whatsappNumber={contact_number}"
    payload = {
         "body": message,
         "buttonText": "Select",
         "sections": sections
    }

    headers = {
                'Authorization': ACCESS_TOKEN,
                'Content-Type': 'application/json'
            }
    response = requests.request("POST", url, headers=headers, json=payload)

def get_media(filename):
    url = f"{API_URL}/api/v1/getMedia"

    payload = {'fileName': filename}
    
    headers = {
    'Authorization': ACCESS_TOKEN
    }

    response = requests.get(url, headers=headers, data=payload)
    return response

#----------------------------------------------------------- Image uploading on server -------------------------------------------------------#
def upload_image(filename, fs):
    response= get_media(filename)
    if response.status_code==200:
        file=fs.put(response.content, filename=filename)
        #print(file)
        print("Upload Complete")
        return file
    
    return False

# ----------------------------------------------------------------------------------------------------------------------------------- #    

