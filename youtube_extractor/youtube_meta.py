import abc


class MetaYouTubeExtractor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def extract_data(self):
        pass

    @abc.abstractmethod
    def payload(self, data_chunk):
        pass

    @property
    @abc.abstractmethod
    def table_name(self):
        pass

    @property
    @abc.abstractmethod
    def endpoint(self):
        pass

    @property
    @abc.abstractmethod
    def parent_instance(self):
        pass

    @property
    @abc.abstractmethod
    def parent_resource(self):
        pass

    @property
    @abc.abstractmethod
    def chunked_data(self):
        pass

    @property
    @abc.abstractmethod
    def data_chunk(self):
        pass
