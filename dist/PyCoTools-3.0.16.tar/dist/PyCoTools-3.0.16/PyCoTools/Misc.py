import PEAnalysis,Errors,pycopi,pydentify2
import os
import string




class RemoveNonAscii():
    def __init__(self,non_ascii_str):
        self.non_ascii_str=non_ascii_str
        self.filter=self.remove_non_ascii()
        
        
    def remove_non_ascii(self):
        for i in self.non_ascii_str:
            if i not in string.ascii_letters+string.digits+'[]-_().':
                self.non_ascii_str=self.non_ascii_str.replace(i,'_')
        return self.non_ascii_str
                
        





if __name__=='__main__':
    s='().'
    
    print RemoveNonAscii(s).filter































