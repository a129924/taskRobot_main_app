import configparser

parser = configparser.ConfigParser()
parser.read("login_info.ini")
parser.read(r".\task.url.ini")

login_info = parser["url"]

print(login_info["login_url"])
