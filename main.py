from dotenv import load_dotenv
load_dotenv()

from app import app

app.run(port=3000, debug=True)
