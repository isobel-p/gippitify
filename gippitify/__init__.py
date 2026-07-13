import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from openrouter import OpenRouter
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import secrets
from . import db

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

    oauth = OAuth(app)
    hackclub = oauth.register(
        name='hackclub',
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        server_metadata_url='https://auth.hackclub.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid'}
    )


    @app.route('/', methods=["GET"])
    def main():
        ai_output = session.pop("ai_output", None)

        remaining = 0
        if "user_id" in session:
            user = db.get_user(session["user_id"])
            if user:
                remaining = max((15 - user["requests"]), 0)
        return render_template("index.html", output=ai_output)
        # return render_template("index.html", output="Text for testing CSS")

    @app.route("/generate", methods=["POST"])
    def generate():
        user_input = request.form.get("input")
        if not user_input:
            return redirect(url_for("main"))
        
        try:
            user_id = session["user_id"]
        except KeyError:
            flash("You are not logged in!")
            return redirect(url_for("main"))
        except Exception as e:
            flash(e)
            return redirect(url_for("main"))


        user = db.get_user(user_id)
        if user is None:
            flash("User not found")
            return redirect(url_for("main"))

        
        
        error = False
        if len(user_input) < 10:
            flash("Minimum length is 10 characters!")
            error = True
        if user['requests'] > 15:
            flash("You have used the maximum number of tokens for today! Tokens reset tomorrow, or DM me for a manual reset.") # this should be a popup fr
            error = True
        if db.daily_limit():
            flash("The site-wide daily limit has been reached. Sorry! Limits reset tomorrow.")
            error = True
        if error:
            return redirect(url_for("main"))

        api_key = os.getenv("API_KEY")

        client = OpenRouter(
            api_key=api_key,
            server_url="https://ai.hackclub.com/proxy/v1",
        )
        credit_used = True
        try:
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
        except Exception as e:
            # 
            if "Insufficient credits" in str(e):
                flash("The paid model is out of credits. Your prompt is using the free model as a fallback. Sorry for the inconvenience! This hasn't used a token.")
                credit_used = False
                try:
                    response = client.chat.send(
                        model="openrouter/free",
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
                except Exception as e2:
                    flash(f"An unexpected error occured: {e2}This hasn't used a token.")
                    return redirect(url_for("main"))
            else:
                flash(f"An unexpected error occured: {e}. This hasn't used a token.")
                return redirect(url_for("main"))

        conn = db.get_db()
        if not credit_used:
            conn.execute(
                'UPDATE user SET requests = requests + 1 WHERE id = ?',
                (user['id'],)
            )
            conn.commit()

        ai_output = markdown.markdown(response.choices[0].message.content)
        session["ai_output"] = ai_output
        return redirect(url_for("main"))
    
    @app.route("/login")
    def login():
        nonce = secrets.token_urlsafe(16)
        session["nonce"] = nonce
        return hackclub.authorize_redirect(redirect_uri=url_for("auth_callback", _external=True), nonce=nonce)

    @app.route("/logout")
    def logout():
        session.pop("user_id", None)
        flash("Logged out.")
        return redirect(url_for("main"))

    @app.route("/auth/callback", methods=["GET"])
    def auth_callback():
        token = hackclub.authorize_access_token()
        nonce = session.pop("nonce", None)
        user_info = hackclub.parse_id_token(token, nonce=nonce)
        oauth_id = user_info['sub']

        conn = db.get_db()
        user = conn.execute('SELECT * FROM user WHERE oauth_id = ?', (oauth_id,)).fetchone()
        if user is None:
            conn.execute(
                'INSERT INTO user (oauth_id, requests, reset_timestamp) VALUES (?, 0, CURRENT_TIMESTAMP)',
                (oauth_id,)
            )
            conn.commit()
            user = conn.execute('SELECT * FROM user WHERE oauth_id = ?', (oauth_id,)).fetchone()

        session['user_id'] = user['id']
        return redirect(url_for('main'))

    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)