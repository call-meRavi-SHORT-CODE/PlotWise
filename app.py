
# import the required Libraries
import google.generativeai as genai
import pandas as pd
import os
from langchain_groq.chat_models import ChatGroq
from pandasai import SmartDataframe
import numpy as np

# Dash
import dash
from dash import html
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash.dash_table import DataTable

# Lida
from lida import Manager, llm
from llmx import  llm, TextGenerationConfig
from pandasai import clear_cache

import json
import re

import matplotlib
matplotlib.use('agg')
from io import BytesIO
import base64
from io import BytesIO
import base64
from PIL import Image


## LLM (Groq Cloud)

bot = ChatGroq(
            temperature=0,
            groq_api_key= "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",
            model_name="llama-3.3-70b-versatile"
        )


## CSV File 
data = pd.read_csv("data.csv")

config = {"save_charts":True,
              "save_charts_path":"F:\Assignment",
             
              "conversational":True,
              "enable_cache": False,
              "llm": bot}

df = SmartDataframe(data,config= config)




######### LIDA Setup  ##############


os.environ["COHERE_API_KEY"] = "6SIporsWbvu2eASwB0rR7cI7FassEl5X1LQDJy5E"  
lida = Manager(text_gen = llm("cohere"))  # we can also use openai 






# Initialize the Dash app

app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    className="container",
    children=[  
        html.Div(
            className="chatbox",
            children=[
                html.Div(
                    className="chatbox__support",
                    children=[
                        html.Div(
                            className="chatbox__header",
                            children=[
                                html.Div(
                                    className="chatbox__content--header",
                                    children=[
                                        html.H4(className="chatbox__heading--header", children="PlotWise"),
                                        html.P(className="chatbox__description--header", children="Want Data to Speak?")
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className="chatbox__messages",
                            id="chat-box",
                            children=[],
                            style={
                                'height': '80vh',
                                'overflowY': 'scroll',
                                'padding': '10px',
                                'backgroundColor': '#FAF9F6',
                                'borderRadius': '10px'
                            }
                        ),
                        html.Div(
                            className="chatbox__footer",
                            children=[
                                dcc.Input(
                                    id="user-input",
                                    type="text",
                                    placeholder="Write a message...",
                                    style={"width": "80%", "padding": "10px"}
                                ),
                                html.Button(
                                    "Send",
                                    id="send-button",
                                    n_clicks=0,
                                    className="chatbox__send--footer send__button",
                                    style={"padding": "10px", "width": "15%"}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

chat_history = []

@app.callback(
    [Output('chat-box', 'children'),
     Output('user-input', 'value')],
    [Input('send-button', 'n_clicks')],
    [State('user-input', 'value')]  # Using State to avoid triggering callback on input change

)


def update_chat(n_clicks, user_message):
    
    global chat_history
    global bot_response

    if len(chat_history) == 0:
        a1 = html.Div(
        children=[
            html.P("Hello! 😊  I’m your Chatbot assistant!"),
            html.P("Please upload your CSV file ,so I can help you with the data.")
        ],
        style={
            'textAlign': 'left',
            'padding': '10px',
            'backgroundColor': '#f0f0f0',
            'borderRadius': '10px',
            'marginBottom': '15px',
            'width': 'fit-content',
            'maxWidth': '70%',
            'alignSelf': 'flex-start',
            'font-size': '1.2rem'
        }
        )

        a2 = html.Div(
        children=[
            html.P("File Uploaded sucessfully 🎉"),
            
        ],
        style={
            'textAlign': 'left',
            'padding': '10px',
            'backgroundColor': '#f0f0f0',
            'borderRadius': '10px',
            'marginBottom': '15px',
            'width': 'fit-content',
            'maxWidth': '70%',
            'alignSelf': 'flex-start',
            'font-size': '1.2rem'
        }
        )
        
        a3 = html.Div(
        children=[
            html.P("How can I assit you today? 😊 "),
            
        ],
        style={
            'textAlign': 'left',
            'padding': '10px',
            'backgroundColor': '#f0f0f0',
            'borderRadius': '10px',
            'marginBottom': '15px',
            'width': 'fit-content',
            'maxWidth': '70%',
            'alignSelf': 'flex-start',
            'font-size': '1.2rem'
        }
    )


        
        
        
        
        
        chat_history.insert(0,a1)
        chat_history.insert(0,a2)
        
        chat_history.insert(0,a3)

    # Check if there is any input and if the button was clicked
    if n_clicks > 0 and user_message:
        # Append the user's message first, aligned to the right

        user_message_div = html.Div(
                user_message,
                style={
                    'textAlign': 'right',
                    'padding': '10px',
                    'backgroundColor': '#d3f8e2',
                    'borderRadius': '10px',
                    'marginBottom': '10px',
                    'width': 'fit-content',
                    'maxWidth': '70%',
                    'alignSelf': 'flex-end',
                    'font-size': '1.2rem'
                    
                }
            )
        chat_history.insert(0, user_message_div)

       
        

       
                
        

        if "summary" in user_message.lower():
            summary = lida.summarize("data.csv", summary_method="default")
            response = bot.invoke(f" As you are a Professional Data Analyst, give me only breif summary (dont bold the words) 120-150 words only of the given data: {summary}")
            bot_response = response.content
            
            response_text =  html.Div(

                children=[
                    html.H1("Summary:",style={"font-weight": "bold",'font-size': '1.2rem'}),
                    html.P( [html.Br(), bot_response])
            ],
             
                style={
                    'textAlign': 'left',
                    'padding': '10px',
                    'backgroundColor': '#f0f0f0',
                    'borderRadius': '10px',
                    'marginBottom': '10px',
                    'width': 'fit-content',
                    'maxWidth': '70%',
                    'alignSelf': 'flex-start',
                    'font-size': '1.2rem'
                }
            )
            chat_history.insert(0, response_text)



        if "trends" in user_message.lower():
            summary = lida.summarize("data.csv", summary_method="default")
            response = bot.invoke(f" As you are a Professional Data Analyst, give me trends and key insights (dont bold the words) 120-150 words only of the given data: {summary}")
            bot_response = response.content
                
            response_text =  html.Div(
                    children=[
                    html.H1("key insights and trends:",style={"font-weight": "bold",'font-size': '1.2rem'}),
                    html.P( [html.Br(), bot_response])
            ],
                    style={
                        'textAlign': 'left',
                        'padding': '10px',
                        'backgroundColor': '#f0f0f0',
                        'borderRadius': '10px',
                        'marginBottom': '10px',
                        'width': 'fit-content',
                        'maxWidth': '70%',
                        'alignSelf': 'flex-start',
                        'font-size': '1.2rem'
                    }
                )
            chat_history.insert(0, response_text)

        if "goals" in user_message.lower() :
            summary = lida.summarize("data.csv", summary_method="default")
            response = bot.invoke(f""" As you are a Professional Data Analyst, give me 3 Potential goals (dont bold the words) 120-150 words only of the given data: {summary}. Give me Output Goal(i) \n
                                  Description: \n
                                  Visualization: \n
                                  Reason: \n
                                   for all 3""")
            bot_response = response.content




            pattern = r"Goal \((.*?)\)\s*Description:\s*(.*?)(?=\s*Visualization:|$)\s*Visualization:\s*(.*?)(?=\s*Reason:|$)\s*Reason:\s*(.*?)(?=\s*Goal|$)"
            matches = re.findall(pattern, bot_response)

            # Store data in JSON format
            goals = []
            for match in matches:
                goal_index, description, visualization, reason = match
                goals.append({
                    "Goal Index": goal_index.strip(),
                    "Description": description.strip(),
                    "Visualization": visualization.strip(),
                    "Reason": reason.strip()
                })

            

            
            for goal in goals:
                a = f"Goal ({goal['Goal Index']}):"
                b = f"Description: {goal['Description']}"
                c = f"Visualization: {goal['Visualization']}"
                d = f"Reason: {goal['Reason']}"
                
                response_text =  html.Div(
                        children=[
                        html.P(str(a),style={"font-weight": "bold",'font-size': '1.2rem'}),
                        html.P(str(b)),
                        html.P(str(c)),
                        html.P(str(d)),

                    ],
                        style={
                            'textAlign': 'left',
                            'padding': '10px',
                            'backgroundColor': '#f0f0f0',
                            'borderRadius': '10px',
                            'marginBottom': '10px',
                            'width': 'fit-content',
                            'maxWidth': '70%',
                            'alignSelf': 'flex-start',
                            'font-size': '1.2rem'
                        }
                    )
                chat_history.insert(0, response_text) 


        if "generate" in user_message.lower() or "create" in user_message.lower():

            try:
                df.chat(user_message)

                
                folder_path = "F:\\Assignment"  # Define the folder path

                # Check if the folder exists
                if os.path.exists(folder_path):
                    # List all files in the folder
                    files = os.listdir(folder_path)
                    
                    # Filter for .png files
                    png_files = [file for file in files if file.lower().endswith(".png")]

                    if len(png_files) >= 1:
                    
                        # Rename .png files to 'img.png'
                        for png_file in png_files:
                            old_file_path = os.path.join(folder_path, png_file)
                            new_file_path = os.path.join(folder_path, "image.png")
                            os.rename(old_file_path, new_file_path)

                        

                        img =  "image.png"
                    
                        with open(img, "rb") as f:
                            encoded_image = base64.b64encode(f.read()).decode()

                            
                        img_response = html.Img(src=f"data:image/jpeg;base64,{encoded_image}",
                                style={
                                "width": "50%",  # Adjust size as needed
                                "float": "left",
                            "margin-right": "10px",
                                
                            })
                        chat_history.insert(0, img_response)
                        os.remove("image.png")

                else:
                    response_text =  html.Div(
                            "Sorry Could not able to generate the chart Please try again...",
                            style={
                                'textAlign': 'left',
                                'padding': '10px',
                                'backgroundColor': '#FF8A8A',
                                'borderRadius': '10px',
                                'marginBottom': '10px',
                                'width': 'fit-content',
                                'maxWidth': '70%',
                                'alignSelf': 'flex-start',
                                'font-size': '1.2rem'
                            }
                        )
                    chat_history.insert(0, response_text) 

            except Exception as e:
                response_text =  html.Div(
                            f"Sorry Error Occured.... {e}. please try again",
                            style={
                                'textAlign': 'left',
                                'padding': '10px',
                                'backgroundColor': '#FF8A8A',
                                'borderRadius': '10px',
                                'marginBottom': '10px',
                                'width': 'fit-content',
                                'maxWidth': '70%',
                                'alignSelf': 'flex-start',
                                'font-size': '1.2rem'
                            }
                        )
                chat_history.insert(0, response_text) 

        else:
            summary = lida.summarize("data.csv", summary_method="default")
            response = bot.invoke(f" As you are a Professional Data Analyst, Answer this question: {user_message} based on the {summary} of the data ")
            bot_response = response.content
            
            response_text =  html.Div(

                bot_response,
             
                style={
                    'textAlign': 'left',
                    'padding': '10px',
                    'backgroundColor': '#f0f0f0',
                    'borderRadius': '10px',
                    'marginBottom': '10px',
                    'width': 'fit-content',
                    'maxWidth': '70%',
                    'alignSelf': 'flex-start',
                    'font-size': '1.2rem'
                }
            )
            chat_history.insert(0, response_text)


            df.chat(user_message)

                
                folder_path = "F:\\Assignment"  # Define the folder path

                # Check if the folder exists
                if os.path.exists(folder_path):
                    # List all files in the folder
                    files = os.listdir(folder_path)
                    
                    # Filter for .png files
                    png_files = [file for file in files if file.lower().endswith(".png")]

                    if len(png_files) >= 1:
                    
                        # Rename .png files to 'img.png'
                        for png_file in png_files:
                            old_file_path = os.path.join(folder_path, png_file)
                            new_file_path = os.path.join(folder_path, "image.png")
                            os.rename(old_file_path, new_file_path)

                        

                        img =  "image.png"
                    
                        with open(img, "rb") as f:
                            encoded_image = base64.b64encode(f.read()).decode()

                            
                        img_response = html.Img(src=f"data:image/jpeg;base64,{encoded_image}",
                                style={
                                "width": "50%",  # Adjust size as needed
                                "float": "left",
                            "margin-right": "10px",
                                
                            })
                        chat_history.insert(0, img_response)
                        os.remove("image.png")




        # Return the updated chat history and clear the input field
        return chat_history, ''  # Clear the input field after sending the message

    return chat_history, ''  # Return current chat history if no new message




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

















