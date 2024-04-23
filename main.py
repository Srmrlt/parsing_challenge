import os

from src import HTTPSessionManager, Parsing


def main():
    url = os.getenv("URL")
    session_manager = HTTPSessionManager(url)
    session_manager.get_data()
    parser = Parsing(session_manager.get_raw_response())
    parser.parse_xml()


if __name__ == "__main__":
    main()
