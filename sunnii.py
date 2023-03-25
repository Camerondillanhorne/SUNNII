import tkinter as tk
from tkinter import filedialog
import webbrowser
import re 
from chatbot_data import greetings, responses, operations
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from pygments.styles import get_style_by_name

def open_link():
    url = "https://igg.me/at/Sunnii/x/33106328#/"
    webbrowser.open(url)

def clear_chat(event=None):
    chatbox.config(state=tk.NORMAL)
    chatbox.delete(1.0, tk.END)
    chatbox.config(state=tk.DISABLED)


def perform_operation(operation, num1, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        return num1 / num2


def chatbot_response(user_input):
    user_input = user_input.lower()

   


      # Find the matching keyword and return the corresponding greetings
    for keyword, greeting in greetings.items():
        if keyword in user_input:
            return greeting


    # Find the matching keyword and return the corresponding response
    for keyword, response in responses.items():
        if keyword in user_input:
            return response

     # Check for arithmetic operations
    for operation, pattern in operations.items():
        match = re.search(pattern, user_input)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = perform_operation(operation, num1, num2)
            return f"The result is {result}"

    # Default response if no keyword matches
    return "I'm sorry, I am not programmed to understand that. Try adding a (?)"

def display_response(response, index=0):
    if index < len(response):
        # Enable the chatbox to insert text
        chatbox.config(state=tk.NORMAL)

        chatbox.insert(tk.END, response[index])
        chatbox.see(tk.END)

        # Disable the chatbox to prevent user editing
        chatbox.config(state=tk.DISABLED)

        root.after(50, display_response, response, index + 1)

def delayed_send_response(response):
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, "SUNNII: ")
    chatbox.config(state=tk.DISABLED)

    display_response(response + "\n\n")

def send_message(event=None):
    user_input = entry.get()
    entry.delete(0, tk.END)
    response = chatbot_response(user_input)

    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, "User: " + user_input + "\n\n")
    chatbox.config(state=tk.DISABLED)

    root.after(1000, delayed_send_response, response)  # 1000 ms (1 second) delay

def new_file():
    text.delete(1.0, tk.END)

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text.delete(1.0, tk.END)
            for token, content in lex(content, PythonLexer()):
                text.insert(tk.END, content, str(token))

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as file:
            content = text.get(1.0, tk.END)
            file.write(content)

def on_text_modified(event=None):
    lineno = int(text.index(tk.INSERT).split('.')[0])
    line_start = text.index(f"{lineno}.0")
    line_end = text.index(f"{lineno}.0 lineend")
    content = text.get(line_start, line_end)
    
    text.tag_remove(tk.ALL, line_start, line_end)

    col = 0
    for token, value in lex(content, PythonLexer()):
        index_start = f"{lineno}.{col}"
        index_end = f"{lineno}.{col+len(value)}"
        text.tag_add(str(token), index_start, index_end)
        col += len(value)

    text.edit_modified(False)

root = tk.Tk()
root.title("SUNNII")

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=5, pady=5)

new_button = tk.Button(button_frame, text="New File", command=new_file)
new_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save", command=save_file)
save_button.pack(side=tk.LEFT, padx=5)

open_button = tk.Button(button_frame, text="Open", command=open_file)
open_button.pack(side=tk.LEFT, padx=5)

button = tk.Button(button_frame, text="DONATE", command=open_link)
button.pack(padx=5, side=tk.LEFT)

text = tk.Text(root, wrap=tk.NONE)
text.pack(fill=tk.BOTH, expand=True)

scroll_x = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=text.xview)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
text.config(xscrollcommand=scroll_x.set)

scroll_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=text.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=scroll_y.set)

style = get_style_by_name('default')
for token_type in Token:
    token_style = style.style_for_token(token_type)
    style_dict = {attr: value for attr, value in token_style if value is not None}
    text.tag_configure(str(token_type), **style_dict)

text.bind("<<Modified>>", on_text_modified)
text.bind("<Configure>", lambda event: text.edit_modified(False))

# Create a chatbox
chatbox = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
chatbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Create an entry box for user input
entry = tk.Entry(root)
entry.pack(padx=10, pady=10, fill=tk.X, expand=True)
entry.bind("<Return>", send_message)

# Create a "Send" button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=5, pady=5, side=tk.RIGHT)

clear_button = tk.Button(root, text="Clear", command=clear_chat)
clear_button.pack(padx=5, pady=5, side=tk.LEFT)



root.mainloop() 
