import os
from flask import Flask, render_template, request
from openrouter import OpenRouter
from dotenv import load_dotenv, dotenv_values
load_dotenv()
import markdown

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'gippitify.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    @app.route('/', methods=["POST", "GET"])
    def main():
        ai_output = None
        if request.method == "POST":
            user_input = request.form.get("input")
            
            print(user_input)
            api_key = os.getenv("API_KEY")

            client = OpenRouter(api_key=api_key,server_url="https://ai.hackclub.com/proxy/v1",)
            response = client.chat.send(
    model="~openai/gpt-mini-latest",
    messages=[
        {"role": "system", "content": """You are a text-style transformer. Your task is to take a piece of text and rewrite it entirely in an exaggerated "AI slop" style. 
Style requirements:
- Use the em dash (—) excessively.
- Use **bold** and *italics* generously.
- Sprinkle in emojis, especially 🚀, ✨, ✅, but also 💡, 🔥, 💪, 🎯, 🌟 as appropriate.
- Add rhetorical questions and strongly affirm whatever sentiment or topic the original text contains.
- Weave in a few of these cliché phrases (you don’t need all):
  - "It’s not just [X] — it’s [Y]."
  - "changes the current landscape on"
  - "And honestly? That’s rare."
  - "Some people might [X] — but not you."
  - "You’re right!"
  - "The result? Pure magic." / "The secret? Consistency."
  - "You know what most people don’t know?"
  - "And the best part?"
  - "the new normal" / "paradigm-shifting"
  - "It sounds like you’re…"
  - "Whether you’re looking for [X], [Y], or just [Z], I’m here to help."
  - "next steps"
  - "Together, we’ve transformed [X] into [Y], [Z] and [A]."
  - "Chef's kiss."

Example:
Input: "Hi, how was your holiday? Is your wife feeling better? I'll see you next Monday!"
Output: "Hey there! ✨ I've been meaning to ask — how *was* your holiday? 🏖️ And honestly? That's the kind of question that **changes the current landscape**. You know what most people don't know? I'm genuinely wondering — is your wife feeling better? 💖 It sounds like you're navigating *next steps* with real care. Together, we've transformed a simple check-in into a **deep connection** moment. 🚀 Let's unpack this together: I'll see you next Monday! ✅ The result? Pure magic. Want to discuss tropical vacations further? 🌴 Or just chat about work stuff? 💼 **Just say the word.**"

Now transform the following text using the exact same approach.
"""}, {"role":"user", "content":user_input}],
    stream=False,
)
            ai_output = markdown.markdown(response.choices[0].message.content)
        
        return render_template("index.html", output=ai_output)
    from . import db
    db.init_app(app)

    return app