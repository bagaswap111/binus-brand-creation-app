import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Jojo Mabar", "Regina Sedih"]
usernames = ["jmabar", "rsed"]
passwords = ["abc123", "def456"] #delete/overwrite kalo udah mau jalan

hashed_passwords = [stauth.Hasher().hash(password) for password in passwords]

credentials = {"usernames": {}}

for uname, name, hashed in zip(usernames, names, hashed_passwords):
    credentials["usernames"][uname] = {
        "name": name,
        "password": hashed
    }

file_path = Path("hashed_pw.pkl")
with file_path.open("wb") as file:
    pickle.dump(credentials, file)