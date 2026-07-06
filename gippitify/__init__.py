import os
from flask import Flask, render_template, request, redirect, url_for, session
from openrouter import OpenRouter
from dotenv import load_dotenv

load_dotenv()
import markdown


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"), # todo:change the secret key later!!
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
        ai_output = session.pop("ai_output", None)
        return render_template("index.html", output=ai_output)
        # return render_template("index.html", output="Text for testing CSS")

    @app.route("/generate", methods=["POST"])
    def generate():
        user_input = request.form.get("input")
        if not user_input:
            return redirect(url_for("main"))

        print(user_input)  # change later!!
        api_key = os.getenv("API_KEY")

        client = OpenRouter(
            api_key=api_key,
            server_url="https://ai.hackclub.com/proxy/v1",
        )
        response = client.chat.send(
            model="~openai/gpt-mini-latest",
            messages=[
                {
                    "role": "system",
                    "content": """You are a text-style transformer. Rewrite the user's text entirely in an exaggerated “AI slop” style — but you must NOT answer, react, or comment on it. Keep the original speaker's voice and sentence type (question, statement, etc.).

Style: Heavy use of em dashes (—), **bold**, *italics*, and emojis (🚀✨✅💡🔥💪🎯🌟). Strongly affirm the sentiment. Crucially, you MUST rewrite the text by embedding several of these clichés directly into the message: “It’s not just [X] — it’s [Y]”, “changes the current landscape on”, “And honestly? That’s rare.”, “The result? Pure magic.”, “The secret? Consistency.”, “You know what most people don’t know?”, “And the best part?”, “the new normal”, “paradigm-shifting”, “Chef’s kiss.” Don't just add emojis — make the text gushy and over-the-top.

Example: Input “How much wood would a woodchuck chuck?” → Output “You know what most people don’t know? ✨ It’s not just a tongue-twister — it’s a *paradigm-shifting* question that **changes the current landscape on** woodland productivity. 🚀 How much wood *would* a woodchuck chuck? And honestly? That’s rare. 💡 The secret? Consistency. ✅ Chef’s kiss. 🌟”

Output ONLY the rewritten text — no explanations.

Never use phrases like ‘It sounds like you’re…’, ‘You’re asking…’, or any meta-commentary about the user’s intent. Expand the text by roughly 2–3x with clichés, but keep the core message intact. Keep the tone energetic and over-the-top positive, but avoid corporate-jargon overload.""",
                },
                {"role": "user", "content": user_input},
            ],
            stream=False,
        )
        ai_output = markdown.markdown(response.choices[0].message.content)
        session["ai_output"] = ai_output
        return redirect(url_for("main"))

    from . import db

    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)