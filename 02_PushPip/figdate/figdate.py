from time import strftime
from pyfiglet import Figlet

def date(format="%Y %d %b, %A", font="graceful") :
    return Figlet(font=font).renderText(strftime(format))