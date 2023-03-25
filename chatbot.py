import tkinter as tk
import webbrowser
import re 
from chatbot_data import greetings, responses, operations


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


# Create the main window
root = tk.Tk()
root.title("SUNNII")

# Create a chatbox
chatbox = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create an entry box for user input
entry = tk.Entry(root)
entry.pack(padx=10, pady=10, fill=tk.X, expand=True)
entry.bind("<Return>", send_message)

# Create a "Send" button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10, side=tk.RIGHT)

clear_button = tk.Button(root, text="Clear", command=clear_chat)
clear_button.pack(padx=10, pady=10, side=tk.LEFT)

button = tk.Button(root, text="DONATE", command=open_link)
button.pack(padx=10, pady=10, side=tk.BOTTOM)

root.mainloop() 
