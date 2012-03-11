class UI(object):
    def status(self, message):
        print(message)

    def warning(self, message):
        print("WARNING: %s" % message)

    def error(self, message):
        print("*** ERROR: %s" % message)
