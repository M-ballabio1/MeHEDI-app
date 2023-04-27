import os
from deta import Deta  # pip install deta
import asyncio
#from dotenv import load_dotenv  # pip install python-dotenv


# Load the environment variables
#load_dotenv(".env")
DETA_KEY = "a0slxdit_WqXwNKB9MYqBfFLqeNVQyaBnbRwYs1Kr"

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.AsyncBase("users_mehedi_db")


def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username, "name": name, "password": password})


async def fetch_all_users():
    """Returns a dict of all users"""
    res = await db.fetch()
    return res.items
    # close connection
    await db.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_items())


def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)


def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)


def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)
