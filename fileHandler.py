import os

class fileHandler():
    def __init__(self):
        pass

    def write(text,path):
        with open(path,"w",encoding='utf-8') as txt:
            txt.write(text)

    def read(path):
        with open(path,"r",encoding='utf-8') as txt:
            return txt.read()
    

    def get_name_dir(name="test", ext="txt", path="."):
        """
        -> This function returns "name of file with largest id" which will be saved in selected directory.
        """
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        id = 0
        len_name = len(name)
        for f in files:
            if name == f[:len_name]: 
                try:
                    ind = f.find(".")
                    if f[ind+1:] == ext:
                        num = int(f[len_name:ind]) + 1
                        if num > id:
                            id = num
                except:
                    pass

        return name + str(id) + "." + ext
