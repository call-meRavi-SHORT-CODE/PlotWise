[![Dash](https://img.shields.io/badge/Dash-%230075A9.svg?style=flat&logo=dash&logoColor=white)](https://plotly.com/dash/)
[![Gemini](https://img.shields.io/badge/Gemini-%23FFB100.svg?style=flat&logo=gemini&logoColor=white)](https://gemini.com/)
[![Cohere](https://img.shields.io/badge/Cohere-%2364D5B1.svg?style=flat&logo=cohere&logoColor=white)](https://cohere.ai/)
[![Lida](https://img.shields.io/badge/Lida-%23FFD700.svg?style=flat&logo=python&logoColor=white)](https://microsoft.github.io/lida/)
[![Lida](https://img.shields.io/badge/Lida-%23181717.svg?style=flat&logo=github&logoColor=white)](https://github.com/microsoft/lida)


# PlotWise: A chatbot assistant to analyze and visualize your data effortlessly 📈📊

Imagine a world where data analysis and visualization come alive seamlessly 🌟.

Features:
1) **Chat with your data:** Ask questions and get real-time insights effortlessly.
2) **Unlock potential:** Make informed decisions in business, education, and research.
3) **See it clearly:** Turn complex datasets into stunning, easy-to-understand visuals.
Break barriers in data interpretation and let PlotWise do the heavy lifting!


# Chatbot Architecture
![Inputs](architecture.png)



🎥 **Watch the demo of PlotWise in action** to see how it can help you interact with your data effortlessly!

👉 [Click here to watch the demo](https://drive.google.com/file/d/1TnhZmqlaYq7BXWTJyvr9edGDUXx3v22v/view?usp=sharing)

**Problems Faced:**

1) I set up the Hugging Face LLaMA model locally, but it was too slow due to my computer's specs.
2) I initially set up Lida using the PaLM API, but then switched to Cohere.
3) faced problem with Configuration of llm in lida
4) I encountered a problem with chart visualization using Lida: "Index out of range for img."


## Setup

Follow these steps to set up the project locally:

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/call-meRavi-SHORT-CODE/PlotWise.git 
```
### 2. Installing Dependencies

 Run to install the necessary packages.
 ```bash
 pip install -r requirements.txt` 
```
### 3. Set your API key

```bash
os.environ['GOOGLE_API_KEY'] = "your_gemini_api_key" # Gemini API key
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') 
genai.configure(api_key=GOOGLE_API_KEY)
os.environ["COHERE_API_KEY"] = "your_cohere_api_key"  # Cohere API key
```
### 4. Set your CSV data Path

```bash
csv = "file_path" # replace your file path here
```

### 5. Run
```bash
python app.py
```
Click http://127.0.0.1:8050/

![Inputs](UI.png)



# Failure Approach 1 ❌👎
This was my first approach for this assignment:

![Inputs](approch1.png)

#### Approach:
1) Set up the Llama 2 LLM locally.
2) Extracted data from a CSV file using LangChain.
3) Split the data into text chunks and convert them into embeddings.
4) Stored the embeddings in a vector database.
5) Used semantic search for data retrieval through RAG (user prompt).

No positives....

#### Problems faced:
1) Setting up the Llama 2 model locally.
2) Issues during the conversion of text chunks into embeddings.
3) Semantic search is not efficient enough for retrieval.

but finally, the approach ended with failure... 😔

# Failure Approach 2 ❌👎
this was my second approach to this assignment:



#### Approach:
1) I used the Gemini API to read the CSV file (which converts it into a string).
2) Using Gemini, I analyzed the CSV file and generated responses for the user input.
3) Based on the user input, I generated code for the charts and executed it.

#### Positives:
1) Able to analyze the data successfully.
2) The model is able to answer some queries regarding the data.
3) In some cases it also generates charts for user queries.

#### Problems faced:
1) Encountered problems while fetching the code from the response.
2) Unable to run the generated code; it returns a syntax error for the Gemini-generated chart code.

After so much effort, this approach also ended in failure... 😔


## Finally Done 🎉🎉 

![Inputs](plotwise.png)

**Watch the demo of Lida in Coloab** 

👉 [Click here to watch the demo1](https://drive.google.com/file/d/1E0ifv1yuSXvcpSoS3fVWoseD-fdXx3li/view?usp=sharing)
👉 [Click here to watch the demo2](https://drive.google.com/file/d/18JG9R-aq2wjUYKWW9THD9Iu-JSZ0rczh/view?usp=sharing)
