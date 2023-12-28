import shelve

class Database:
    def __init__(self, dbName: str = "chat_history") -> None:
        self.dbName = dbName

    # Load chat history from shelve file
    def load_chat_history(self)->[dict]:
        with shelve.open(self.dbName) as db:
            return db.get("messages", [])


    # Save chat history to shelve file
    def save_chat_history(self, messages: [dict]):
        print("Database: Save", messages)
        with shelve.open(self.dbName) as db:
            db["messages"] = messages
