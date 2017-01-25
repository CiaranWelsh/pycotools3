import PyCoTools





class InputError(Exception):
    pass

class CopasiError(Exception):
    pass

class NoMetabolitesError(Exception):
    pass

class IncompatibleStringError(Exception):
    def is_ascii(self,s):
        return all(ord(c) < 128 for c in s)
        
class ExperimentMappingError(Exception):
    pass

class ReportDoesNotExistError(Exception):
    pass

class ParameterEstimationPlottingError(Exception):
    pass


class IndexOutOfBounds(Exception):
    pass



class FileDoesNotExistError(Exception):
    pass


















