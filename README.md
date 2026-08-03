# Gippitify
*Make the internet worse by turning any text into AI slop.*

[Try it here!](https://gippitify.isobel-p.hackclub.app)

![A screenshot of Gippitify.](/gippitify.png)

## About
Most AI rewriter websites convert AI text to human-sounding text. Gippitify converts human text to AI-sounding text. Made with Flask.

This is just a fun little tool for entertainment purposes and also a reminder of what makes AI‑generated content so distinctive and cringe.

In a world where the amount of slop on the internet is increasing... why not make the problem worse? Now you can efficiently generate soulless text littered with em dashes and emojis to your heart's desire. After all, if you can't beat them, join them.

> [!NOTE]
> A Hack Club Auth account is necessary to use Gippitify. Alternatively, you can [host it yourself.](#self-hosting-guide)

## Features
- An AI rewriter that adds slop to your text
- ✨ Excessive amounts of emojis ✨
- Copy button to easily share your slop with your friends
- more features coming soon...

## Self-Hosting Guide
Just want to try it out? [Try it here!](https://gippitify.isobel-p.hackclub.app)
### Prerequisites
Before you start, make sure you have:
- Python 3.10+
- Git (obviously)
- An OpenRouter API key (get one at [openrouter.ai](openrouter.ai))

### Install
1. Clone the repo
```bash
git clone https://github.com/isobel-p/gippitify.git
cd gippitify
```
2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up environment variables
Create a `.env` file in the "gippitify" **subfolder**:
```bash
nano .env
```
Add the following (replace the placeholder values):
```env
SECRET_KEY=a-very-secret-random-string
API_KEY=your-openrouter-api-key
CLIENT_ID=your-hackclub-auth-client-id
CLIENT_SECRET=your-hackclub-auth-client-secret
```
The SECRET_KEY should be a randomly generated string, at least 32 characters.
5. Initialise the database
```bash
flask --app gippitify init-db
```
6. Run the app locally
```bash
flask --app gippitify run --host=0.0.0.0 --port=8000
```
For a production environment use a WSGI server. I use Gunicorn but any WSGI server compatible with Flask should work.

## Contributing
Contributions welcome! Feel free to open issues or submit PRs.

## License
This project is open source and available under the GNU GPLv3 License. See the [LICENSE.md](LICENSE.md) for more details.

*This README was written by a human. :3*