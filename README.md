# ERNIEST
**Other language versions: [English](README.md), [中文](README_zh.md).**

A platform for quickly developing large-scale model interactions based on Baidu ERNIE and Streamlit.

**Author: AFAN (WeChat: afan-life, Email: fcncassandra@gmail.com)**  

Online Demo: https://erniest.streamlit.app/

**The following content is translated by ChatGPT**  

## Features

This project currently includes the following features:

1. **User Login:** Supports displaying different historical conversation records based on different usernames. Additional authentication methods can be developed.
2. **Baidu Qianfan Large Model Integration:** Includes a free token and supports token acquisition and model version switching within the interface.
3. **Conversation Storage:** Uses SQLite to store conversation topics (first 15 characters) and all associated conversation records. Users can create new topics.
4. **Function Response:** Based on the large model's function call feature, allowing for custom functions and description JSONs to be triggered during relevant conversations.

The interaction flow for all features is shown below:  
![pipeline](asset/pipeline.png)

## Interface Description

**Login Interface:** Users can log in without a password by default. Different usernames will display different historical conversation records.

![login](asset/login.png)

**Conversation Interface:** During conversations, a token is required to access the large model. The platform includes a free token for using the ernie-speed model for conversations, but this model does not support function responses or online searches.

Users can choose the ernie-3.5 model, which supports function responses and online searches. However, users need to generate their own token by registering and paying on Baidu Smart Cloud, then input the APP Key and Secret Key. For more details, see: https://cloud.baidu.com/article/1089328  

![token](asset/token.png)

**Simple Chat Interface:** Users can directly use the ernie-speed model for conversations. The built-in token supports this session.

![simple_chat](asset/simple_chat.png)

**Function Response:** The platform includes a sample function for project descriptions. When the conversation touches on this topic, the function is triggered, and the result is refined and output by the large model.

![function_call](asset/function_call.png)

**Online Search:** The ernie-3.5 version supports online searches of public websites using the large model. Here is an example of searching the author's Bilibili account.

![online_search](asset/online_search.png)

## Project Usage

This project is recommended to use `Python=3.9` and suggests creating a new conda environment to prevent version conflicts:

```bash
conda create -n erniest python=3.9
```

Key Python package versions:

```bash
streamlit                    1.35.0
streamlit-modal              0.1.2
qianfan                      0.4.2
```

Install all dependencies in one step:

```bash
pip install -r requirements.txt
```

Run the project in the erniest conda environment:

```bash
streamlit run main.py
```

## Code Modules

The main file structure of this project and its corresponding code modules are as follows:

- `asset`: Stores static resources for the project.
- `database`: Initializes and manages the project's database tables and connections.
- `function`: Contains the code and descriptions for large model function responses.
- `llm`: Baidu Qianfan large model integration module, with registered functions from the `function` module.
- `service`: System business functionality, including conversation record database queries and storage.
- `view`: System view modules.
  - `login.py`: User login, invoking `auth.py` for authentication.
  - `sidebar.py`: Post-login left sidebar showing conversation topics, token input, and model version switching.
  - `chat.py`: Post-login conversation interface.
  - `tool.py`: Other utility functions, such as image display.
- `auth.py`: Authentication code module, allowing login without a password by default.
- `config.py`: System configuration module, including database, default token, and Streamlit-related configurations.
- `gpt.db`: SQLite database file generated after launching the `database` module.
- `log.py`: Logging module.
- `main.py`: Main module and entry point.

## Further Learning

Scan the QR code to join the Knowledge Planet: AFAN's Fintech, for source code tutorials on the ERNIEST project:

<img src="asset/planet.jpg" title="Knowledge Planet: AFAN's Fintech" alt="Knowledge Planet: AFAN's Fintech" width="199">

Contact AFAN on WeChat to join the fintech learning community (WeChat: afan-life):

<img src="asset/weixin.png" title="WeChat: afan-life" alt="WeChat: afan-life" width="199">

## Update Log

- **2024/07/25:** First upload of ERNIEST V1.0.