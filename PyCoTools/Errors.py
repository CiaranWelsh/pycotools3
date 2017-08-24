class InputError(Exception):
    pass

class CopasiError(Exception):
    pass

class NometabolitesError(Exception):
    pass

class IncompatibleStringError(Exception):
    def is_ascii(self,s):
        return all(ord(c) < 128 for c in s)
        
class ExperimentMappingError(Exception):
    pass

class ReportDoesNotExistError(Exception):
    pass

class ParameterEstimationplottingError(Exception):
    pass


class IndexOutOfBounds(Exception):
    pass


class FileDoesNotExistError(Exception):
    pass

class FolderDoesNotExistError(Exception):
    pass


class NotImplementedError(Exception):
    pass


class ParameterInputError(Exception):
    pass


class SomethingWentHorriblyWrongError(Exception):
    pass


class TimeCourseError(Exception):
    pass


class AvagadrosError(Exception):
    pass




