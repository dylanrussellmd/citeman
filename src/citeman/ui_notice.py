from consolemenu import PromptUtils, Screen

def noticeScreen(message, color):
    pu = PromptUtils(Screen())
    pu.clear()
    pu.println(color(message))
    pu.enter_to_continue()
    pu.clear()