# chatbot.py
Implements dictionary through two json files.

# chat.json
-> Contains answers for the questions that are asked to the chatbot.

-> If you teach something to the chatbot, the data stores in this file for future.

# app.json
-> Try to ask "Open Chrome", It will first search the "chrome.exe" file in the directories and save its location to app.json.

-> Searching takes time so, the saved location serves as cache access for the chatbot.
