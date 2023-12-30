import os
import dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv.load_dotenv()


def get(key, default=None):
    return os.environ.get(key, default)


OPENAI_COOKIE_FILE = get("openai_cookie_file")

LOGGER_NAME = get("logger_name", "The Hunter")

LOGGING_FILE = get("logging_file", "The Hunter.log")

LOGGING_LEVEL = int(get("logging_level", 10))

INDENTATION_LEVEL = int(get("indentation_level", 4))
