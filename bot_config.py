import os

config = {
    "bot": {
        "login": os.environ.get("VK_BOT_LOGIN"),
        "password": os.environ.get("VK_BOT_PASSWORD"),
        "number": os.environ.get("VK_BOT_NUMBER"),
        "plugins": ["bothelp", "example", "anec", "rasp", "bashim", "google",
                    "kappa", "pone", "mailcheck", "gtts"]
    },
    "rasp": {
        1: "5383",
        4: "5371"
    },
    "mailcheck": {
        "trigger": {"trigger": "interval", 'minutes': 3},
        "mailboxes": eval(os.environ.get("VK_BOT_MAILBOXES"))
    },
    "kappa": 228083099
}
