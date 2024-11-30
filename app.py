import google.generativeai as genai
import dash
from dash import html
import time
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
import time
from llmx import  llm, TextGenerationConfig
import os
from dash import dash_table
import plotly.express as px  
import sys
import io
from lida import Manager, llm
from dash.dash_table import DataTable
from PIL import Image
from io import BytesIO
import base64


csv = "data.csv" # replace with your csv file path

os.environ['GOOGLE_API_KEY'] = "your_gemini_api_key" 


GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') 
genai.configure(api_key=GOOGLE_API_KEY)

os.environ["COHERE_API_KEY"] = "your_cohere_api_key"  
lida = Manager(text_gen = llm("cohere"))  # we can also use openai 

model = genai.GenerativeModel("gemini-1.5-flash")





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
                                'backgroundColor': '#ffffff',
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

        def base64_to_image(base64_string):
                # Decode the base64 string
                byte_data = base64.b64decode(base64_string)
                # Use BytesIO to convert the byte data to image
                return Image.open(BytesIO(byte_data))    

        
        user_query = user_message
        
        library = "seaborn"
        summary = lida.summarize(csv, summary_method="default")
        Charts = lida.visualize(summary=summary, goal=user_query,library=library)
        img_base64_string = Charts[0].raster
        image = base64_to_image(img_base64_string)
        image.save("img.png")
        img = "img.png"
        with open(img, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode()

            
        img_response = html.Img(src=f"data:image/jpeg;base64,{encoded_image}",
                style={
                "width": "50%",  # Adjust size as needed
                "float": "left",
            "margin-right": "10px",
                
            })
        chat_history.insert(0, img_response) 
                
        
         

        
        if "summary" in user_message:
            summary = lida.summarize(csv, summary_method="default")
            response = model.generate_content(f"give me breif summary (dont bold the words) of the in 80-90 words of the given data: {summary}")
            bot_response = response.text
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

        if "trend" in user_message:
            summary = lida.summarize(csv, summary_method="default")
            response = model.generate_content(f"give me  the trend of the data over time: {summary}")
            bot_response = response.text
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

        

            
        
        if "goal" in user_message:
            summary = lida.summarize(csv, summary_method="default")
            goals = lida.goals(summary, n=2)

            
            
            
            for i in range(len(goals)): 
                a1 = f'Goal {i+1}:'
                a2 = f'Question: {goals[i].question}'
                a33 = f'Visualization: {goals[i].visualization}'
                a4 = f'Reason: {goals[i].rationale}'
            
                
                response_text =  html.Div(
                    children=[
                    html.P(str(a1)),
                    html.P(str(a2)),
                    html.P(str(a33)),
                    html.P(str(a4)),

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

        
            
                

            
       

        
           
        


        
        
        
        



        # Append the bot's response, aligned to the left
        """
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
        chat_history.insert(0, response_text) """
        

        # Return the updated chat history and clear the input field
        return chat_history, ''  # Clear the input field after sending the message

    return chat_history, ''  # Return current chat history if no new message



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
