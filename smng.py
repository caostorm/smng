from core.interface.action import server_action
from core.helper.creator import create_action

class smng:
    def __init__(self):
        pass

    def run(self):
        action = create_action()
        action.parse_parameters()
        action.run()