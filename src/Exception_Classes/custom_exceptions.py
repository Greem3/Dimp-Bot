class OnlyUsers(Exception):
    
    def __init__(self, args: str = "Only Users"):
        super().__init__(args)