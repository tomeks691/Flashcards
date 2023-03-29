import sqlite3
from mtranslate import translate


class Flashcard:

    def add_new_flashcard(self, word, wordlist):
        translated_word = translate(word, "pl")
        conn = sqlite3.connect("wordlists.db")
        c = conn.cursor()
        try:
            c.execute(f"INSERT INTO {wordlist} VALUES ('{word}', '{translated_word}', 0)")
        except sqlite3.Error as error:
            pass
        conn.commit()
        conn.close()

    def get_all_flashcards(self, wordlist):
        conn = sqlite3.connect("wordlists.db")
        c = conn.cursor()
        c.execute(f"SELECT * FROM {wordlist}")
        flashcards = c.fetchall()
        conn.close()
        return flashcards

    def get_all_tables(self):
        conn = sqlite3.connect("wordlists.db")
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        conn.close()
        return tables

    def delete_flashcard(self, wordlist, word):
        conn = sqlite3.connect("wordlists.db")
        c = conn.cursor()
        c.execute(f"DELETE from {wordlist} where word = ?", (word,))
        conn.close()

    def update_wordlists(self, wordlist, word):
        conn = sqlite3.connect("wordlists.db")
        c = conn.cursor()
        c.execute(f"SELECT * FROM {wordlist} WHERE word = ?", (word,))
        rows = c.fetchall()
        correctly_answer = rows[0][2] + 1
        if correctly_answer <= 10:
            c.execute(f"UPDATE {wordlist} SET correctly_answer = {correctly_answer} WHERE word = ?", (word,))
            c.execute(f"SELECT * FROM {wordlist} WHERE word = ?", (word,))
            if_learned = False
        else:
            self.delete_flashcard(wordlist, word)
            if_learned = True
        conn.commit()
        conn.close()
        return if_learned

    def check_answer(self, wordlist, word, answer):
        conn = sqlite3.connect("wordlists.db")
        c = conn.cursor()
        c.execute(f"SELECT * FROM {wordlist} WHERE word = ?", (word,))
        rows = c.fetchall()
        conn.close()
        if answer.lower() == rows[0][1].lower():
            return True
        else:
            return rows[0][1]

    def create_wordlist(self, wordlist):
        conn = sqlite3.connect("wordlists.db")
        c = conn.cursor()
        c.execute(
            f"CREATE TABLE IF NOT EXISTS {wordlist} (word TEXT type UNIQUE, translated_word TEXT, correctly_answer INTEGER)")
        conn.close()