import re
import random
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime


GREETINGS = [
    "Hello! How can I help you today?",
    "Hi there! What can I do for you?",
    "Hey! Need any help?"
]

ABOUT_BOT = [
    "I'm a simple rule-based chatbot built with Python and Tkinter.",
    "Just a simple chatbot using pattern rules and random responses.",
    "A tiny rule-based bot — learning from patterns, not from the cloud!"
]

HELP_RESPONSES = [
    "Sure — tell me what you need help with.",
    "Happy to help! What do you want to do?",
    "I can answer simple questions like time, date, greetings, and farewells."
]

UNKNOWN_RESPONSES = [
    "I'm sorry, I didn’t understand that. Can you rephrase?",
    "Hmm, I don't know how to respond to that yet.",
    "I didn't catch that — try asking differently."
]

FAREWELLS = [
    "Goodbye! Have a great day!",
    "See you later — take care!",
    "Bye! It was nice chatting with you."
]

def chatbot_response(user_input: str) -> str:
    text = user_input.lower().strip()

    
    if re.search(r'\b(hi|hello|hey|hiya)\b', text):
        return random.choice(GREETINGS)

    
    if re.search(r'\b(who are you|what are you|about you)\b', text):
        return random.choice(ABOUT_BOT)

    
    if re.search(r'\b(help|support|assist|how to)\b', text):
        return random.choice(HELP_RESPONSES)

    
    if re.search(r'\b(time|current time|what time)\b', text):
        now = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {now}."

    
    if re.search(r'\b(date|day|today)\b', text):
        today = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}."

    
    m = re.search(r'(\bwhat is\b|\bcalculate\b)\s*([\d\.\s\+\-\*\/\(\)]+)', text)
    if m:
        expr = m.group(2)
        
        if re.fullmatch(r'[\d\.\s\+\-\*\/\(\)]+', expr):
            try:
                result = eval(expr, {"__builtins__": {}})
                return f"The answer is {result}"
            except Exception:
                return "I couldn't calculate that expression."
        else:
            return "I can only calculate simple numeric expressions."

    
    if re.search(r'\b(bye|goodbye|exit|quit|see you)\b', text):
        return random.choice(FAREWELLS)

    
    return random.choice(UNKNOWN_RESPONSES)


class RuleChatGUI:
    def __init__(self, root):
        self.root = root
        root.title("Rule-Based Chatbot")
        root.geometry("520x500")
        root.resizable(False, False)

        
        self.chat_display = scrolledtext.ScrolledText(root, state='disabled', wrap='word', font=("Helvetica", 11))
        self.chat_display.place(x=10, y=10, width=500, height=380)

        
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.entry_var, font=("Helvetica", 12))
        self.entry.place(x=10, y=405, width=380, height=35)
        self.entry.bind("<Return>", self.on_send)

        
        self.send_btn = tk.Button(root, text="Send", command=self.on_send, width=10)
        self.send_btn.place(x=400, y=405, width=110, height=35)

        
        self._append_chat("Chatbot", " Hello! Type 'bye' to end the chat.")

    def _append_chat(self, sender: str, message: str):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def on_send(self, event=None):
        user_text = self.entry_var.get().strip()
        if not user_text:
            return
        self._append_chat("You", user_text)
        self.entry_var.set("")

        response = chatbot_response(user_text)
        self._append_chat("Chatbot", response)

        
        if re.search(r'\b(bye|goodbye|exit|quit|see you)\b', user_text.lower()):
            self.root.after(1200, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = RuleChatGUI(root)
    root.mainloop()
