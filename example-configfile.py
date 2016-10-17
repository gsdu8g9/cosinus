config = {
    "bot": {
        "admins": {1, 4},
        "token": "abcdefg",
        "chatplugins": {"bothelp", "botstatus", "pone", "google", "anec", "bashim",
                        "rasp", "kappa", "fap", "fuck", "ms-emotion"},
        "scheduleplugins": {"email_check"}
    },
    "email_check": {
        "interval": {'minutes': 3},
        "mailboxes": {
            1: {
                "server": "imap.mail.ru",
                "credentials": ("login@mail.ru", "pass"),
                "page": "https://e.mail.ru/messages/inbox"
            },
            7: {
                "server": "imap.gmail.com",
                "credentials": ("user@gmail.com", "password"),
                "page": "https://gmail.com/"
            }
        }
    },
    "rasp": {
        1: "5383",
        7: "5371"
    },
    "microsoft-cognitive":{
        "emotion-key": "keyhere"
    }
}
