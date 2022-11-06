from PIL import Image
from fileHandler import fileHandler
from tkinter import messagebox

class ImgStg():
    def __init__(self,encoding="16bit"):
        self.embed_img = None
        self.extracted_text = None
        self.encoding = encoding
    
    def _int_to_bin(self, val, single=False):
        """Convert an integer tuple to a binary (string) tuple.
        :param rgb: An integer tuple like (220, 110, 96)
        :return: A string tuple like ("00101010", "11101011", "00010110")
        """
        if single == False:
            r, g, b = val[:3]
            return f'{r:016b}', f'{g:016b}', f'{b:016b}'
        else:
            return f'{val:016b}'
    

    def _bin_to_int(self, val, single=False):
        """Convert a binary (string) tuple to an integer tuple.
        :param rgb: A string tuple like ("00101010", "11101011", "00010110")
        :return: Return an int tuple like (220, 110, 96)
        """
        if single==False:
            r, g, b = val[:3]
            return int(r, 2), int(g, 2), int(b, 2)
        else:
            return int(val, 2)
    

    def _str_to_bin(self, val):
        return (''.join(format(ord(x), '016b') for x in val))


    def save_img(self,path,name=None):
        if name==None:
            name = fileHandler.get_name_dir("embeded_img","png", path=path)

        self.embed_img.save(path + "\\" + name)
    
    def save_txt(self,path,name=None):
        if name==None:
            name = fileHandler.get_name_dir("extracted_text","txt",path=path)
        
        fileHandler.write(self.extracted_text, path = path + "\\" + name)

    def resize_img(img, size):
        return img.resize(size)

    def _merge_txt_rgb(self, txt_bits, rgb):   
        r,g,b = self._int_to_bin(rgb[:3])
        r = r[:-1]+ txt_bits[0]
        g = g[:-1]+ txt_bits[1]
        b = b[:-1]+ txt_bits[2]

        new_rgb = self._bin_to_int((r,g,b))
        return new_rgb
    
    def _unmerge_txt_rgb(self, rgb):   
        """GET last bits of the 8 bit channel => like r : 0110001(1) -> 1 is the last bit."""
        r,g,b = self._int_to_bin(rgb)
        
        
        b1 = r[-1:] # last bit of the red
        b2 = g[-1:] # last bit of the green
        b3 = b[-1:] # last bit of the blue

        return b1,b2,b3


    def _resolve_place_len(self,img):
        """this function returns the embedded data length saved at the end of the picture"""
        w,h = img.size[0], img.size[1]
        max_len = int(w * h * 3 / 16) # maximum char amount in the image # +++

        max_block_len = len(str(max_len)) # maximum signable len

        bin_len = (max_block_len * 16)
        mod_bits = bin_len % 3

        if mod_bits > 0:
            bin_len += (3-mod_bits)
        
        map = img.load()
        bin_block = ""
        for i in range(1 , int(bin_len / 3) + 1)[::-1]:
            for j in range(3):
                i_b = self._int_to_bin(map[w-1, h-i][j], single = True)
                bin_block += str(i_b[-1:])
        


        num_bin = ""
        txt_len = ""
        for i in bin_block[:bin_len]:
            num_bin += i
            if len(num_bin) % 16 == 0 and len(num_bin) != 0:
                txt_len += str(self._bin_to_int(num_bin, single=True))
                num_bin = ""
        

        return int(txt_len)




    def _place_len(self, map, w, h, txt_len): 
        """this function embeds the length of the data to be recorded at the end of the picture"""
        max_len = int(w * h * 3 / 16) # maximum char amount in the image # +++
        max_block_len = len(str(max_len)) # maximum signable len
        txt_block_len = len(str(txt_len)) # text len

        empty_space = (max_block_len - txt_block_len) * "0"
        len_block = empty_space + str(min(int(txt_len),max_len))
        mod_bits = (max_block_len * 16) % 3
        bin_block = "" # binary of the len_block

        for num in len_block:
            bin_block += self._int_to_bin(int(num), single=True)

        if mod_bits > 0:
            bin_block += "0" * (3-mod_bits)
        
        counter = 0
        for i in range(1 , int(len(bin_block) / 3) + 1)[::-1]:
            b_arr = []
            for j in range(3):
                i_b = self._int_to_bin(map[w-1, h-i][j], single = True)
                b_i = self._bin_to_int(i_b[:-1] + bin_block[counter], single = True)
                b_arr.append(b_i)
                counter +=1
    
            map[w-1, h-i] = tuple(b_arr)
        
    

    def _merge_txt(self, img_p, txt_p, dest_p, showInfo=True):
        """this function Splits text into 16-bit chunks and 
        embeds it in the last bits of the image's color channels
        """
        img = Image.open(img_p)
        txt = fileHandler.read(txt_p)

        img_w, img_h = img.size[0], img.size[1]
        map = img.load()
        txt_bits = self._str_to_bin(txt) 
        text_len = len(txt) 
        mod_txt = (text_len * 16) % 3
        if mod_txt > 0:
            txt_bits += "0" * (3-mod_txt)

        counter = 0
        out_break = False
        for i in range(img_w):
            for j in range(img_h):
                if counter < text_len * 16:
                    map[i, j] = self._merge_txt_rgb(txt_bits[counter:counter+3], map[i,j])
                    counter += 3
                else:
                    out_break = True
                    break
            
            if out_break:
                break

        self._place_len(map,img.size[0],img.size[1], text_len)    
    
        self.embed_img = img
        self.save_img(dest_p)
        if showInfo:
            messagebox.showinfo("Succesful !", "Data embedding was successful.")

    def _unmerge_txt(self, img_p, dest_p, showInfo=True):
        img = Image.open(img_p)
        img_w, img_h = img.size[0], img.size[1]
        map = img.load()
        
        text_len = self._resolve_place_len(img) * 16
        counter = 0
        out_break = False
        txt_bits = ""
        
        for i in range(img_w):
            for j in range(img_h):
                if counter < text_len:
                    b1,b2,b3 = self._unmerge_txt_rgb(map[i, j])
                    txt_bits += b1+b2+b3
                    counter += 3
                else:
                    out_break = True
                    break
            
            if out_break:
                break  
        num_bin = ""

        ext_txt = ""
        for i in txt_bits:
            num_bin += i
            if len(num_bin) % 16 == 0 and len(num_bin) != 0:
                ext_txt += chr(int(num_bin[:16], 2))
                num_bin = ""

        self.extracted_text = ext_txt
        self.save_txt(dest_p)
        if showInfo:
            messagebox.showinfo("Succesful !", "Data extraction was successful.")


if __name__ == "__main__":
    stg = ImgStg() 
    SourceImagePath = "./resources/test.png"
    textPath = "./resources/text.txt"
    EmbededImagePath = "embeded_img0.png"
    destPath = "."
    stg._merge_txt(SourceImagePath, textPath, destPath)
    #stg._unmerge_txt(EmbededImagePath, destPath)
