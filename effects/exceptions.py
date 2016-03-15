class InvalidStatusDuration(Exception):

    def __init__(self, actor, status):
        super(InvalidStatusDuration, self).__init__()
        self.actor = actor
        self.status = status
