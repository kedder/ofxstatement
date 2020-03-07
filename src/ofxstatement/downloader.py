class Downloader(object):
    """Abstract statement downloader.

    Defines interface for all parser implementation
    """

    def download(self):
        """download statement file

        Return Statement object

        May raise exceptions.DownloadError if there are problems
        in downloading statement file.
        """
        raise NotImplementedError

