import os

config = {
    "bot": {
        "login": os.environ.get("VK_BOT_LOGIN"),
        "password": os.environ.get("VK_BOT_PASSWORD"),
        "number": os.environ.get("VK_BOT_NUMBER"),
        "plugins": ["example"]
    }
}
