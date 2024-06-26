from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
import pickle
import dbm as db
from tkinter import messagebox

class Example(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack()
        cerceve = LabelFrame(self,bd=3, relief=SUNKEN,width=10,height=10)
        cerceve.grid(row=0, column=0, sticky=E, padx=3, pady=3)

        cerceve1 = LabelFrame(self, bd = 3 , relief=SUNKEN,width=10,height=10)
        cerceve1.grid(row = 1 , column=0,sticky=W,padx=3,pady=3)
        
        kategori = ['Yiyecek', 'İçecek', 
                'Giyim', 'Elektronik','Ev']
        
        self.lb_kategori = Listbox(cerceve, selectmode="single",width=14, exportselection = 0 )
        for indeks, secenekler in enumerate(kategori):
            self.lb_kategori.insert(indeks, secenekler)
        self.lb_kategori.grid(column=0, row=0,rowspan=2, sticky=W)
        
        
        self.lb_satisliste = Listbox(cerceve1,selectmode="single",width=140, )
        self.lb_satisliste.grid(column = 0,row = 1,rowspan=10)
        
        self.pack()

        isim_label =Label(cerceve, text="İsim")
        isim_label.grid(column=1, row=0, sticky=EW, padx=1, pady=1)

        self.var_isim = StringVar()
        isim_entry = Entry(cerceve,textvariable= self.var_isim,relief=RAISED)
        isim_entry.grid(column=1, row=1, sticky=E, padx=1, pady=1)

        
        self.marka_label =Label(cerceve, text="Marka",)
        self.marka_label.grid(column=2, row=0, sticky=EW, padx=1, pady=1)

        self.var_marka = StringVar()
        self.marka_entry =Entry(cerceve,textvariable=self.var_marka,relief=RAISED)
        self.marka_entry.grid(column=2, row=1, sticky=E, padx=1, pady=1)

        self.tanim_label =Label(cerceve, text="Tanım")
        self.tanim_label.grid(column=3, row=0, sticky=EW, padx=1, pady=1)

        self.var_tanim = StringVar()
        self.tanim_entry =Entry(cerceve,relief=RAISED)
        self.tanim_entry.grid(column=3, row=1, sticky=E, padx=1, pady=1)

        self.stok_label =Label(cerceve, text="Stok")
        self.stok_label.grid(column=4, row=0, sticky=EW, padx=1, pady=1)

        self.var_stok = IntVar()
        self.stok_entry =Entry(cerceve,textvariable=self.var_stok,relief=RAISED)
        self.stok_entry.grid(column=4, row=1, sticky = E, padx=1, pady=1)

        self.fiyat_label =Label(cerceve, text="  Fiyat")
        self.fiyat_label.grid(column=5, row=0, sticky = EW, padx=1, pady=1)

        self.var_fiyat = DoubleVar()
        self.fiyat_entry =Entry(cerceve,textvariable=self.var_fiyat,relief=RAISED)
        self.fiyat_entry.grid(column=5, row=1, sticky=E, padx=1, pady=1)

        self.link_label =Label(cerceve, text="Link")
        self.link_label.grid(column=6, row=0, sticky=EW, padx=1, pady=1)

        self.var_link = StringVar()
        self.link_entry =Entry(cerceve,textvariable= self.var_link,relief=RAISED)
        self.link_entry.grid(column=6, row=1, sticky=E, padx=1, pady=1)

        self.ekle=Button(cerceve, text= "Ekle", relief=RAISED, command= self.urun_kayit)
        self.ekle.grid(column=7, row=0, sticky=EW, padx=1, pady=1)

        self.sat = Button(cerceve1,text = "1 adet sat",relief=RAISED,command = self.satis)
        self.sat.grid(column=7,columnspan=2,row = 5,sticky=E,padx=1,pady=1)

        
        self.lb_goruntule()
        
        
    def lb_goruntule(self):
        """
            Database içindeki bilgilerin lb de görüntülenmesini sağlar.
        
                                                                        """
        self.lb_satisliste.delete(0,END)
        
        self.dosya = db.open('urunler','c')
        self.liste=[]
        for deger in self.dosya.keys():
            self.degerler= pickle.loads(self.dosya[deger])
            self.anahtar=pickle.loads(deger)
            self.liste.append(self.degerler)
        for indeks,i in enumerate(self.liste):
            deger_string= "Kategori: {} | {} - {}, {}TL, stok: {}".format(i["kategori"],i["isim"],i["marka"],i["fiyat"],i["stok"])

            self.lb_satisliste.insert(indeks,deger_string)
        self.liste2 = self.liste[::-1]

        
    def urun_kayit(self):
        """
            Girilen ürün bilgilerini database'e yazan fonksiyon
                                                                """
        self.lb_goruntule()
        try:
            
            
            self.indeksNo = self.lb_kategori.curselection()
            self.count0 = 0
            for x in self.liste :
                self.count0 += 1

            for count in range(1):
                
                self.urun = {
                "kategori" : self.lb_kategori.get(self.indeksNo),
                "isim":self.var_isim.get(),
                "marka":self.var_marka.get(),
                "fiyat":self.var_fiyat.get(),
                "stok":self.var_stok.get()}
            
            
            if self.count0 == 0:
                self.count = 0
            else:
                self.count = self.count0

            self.dosya[pickle.dumps(self.count)] = pickle.dumps(self.urun)

        except tk.TclError:
            messagebox.showinfo('Hata', 'Ürün ekleme işlemi için  bir kategori seçimi yapın')
        
        self.lb_goruntule()
        
        
    def satis(self):
        
        """
            seçilen ürenlerin stok değerini 
            1 azaltan fonksiyon .
                                        """
        
        try:
            
            
            self.satis_indeksleme()
            
            aranan_urun = pickle.loads(self.dosya[self.keys1])
            if  aranan_urun["stok"] > 0 :
                aranan_urun["stok"] -= 1  
            else:
                messagebox.showinfo('Hata','Ürün Tükenmiştir')
            
            self.dosya[pickle.dumps(self.key)] = pickle.dumps(aranan_urun)
            self.lb_goruntule()

        
        except IndexError:
            
            messagebox.showinfo('Hata', 'Satışı yapılacak ürünü seçin')
            

    def satis_indeksleme(self):
            
            self.indeksNo1 = self.lb_satisliste.curselection()
            indeks = (self.indeksNo1[0])
            
            for self.keys1 in self.dosya.keys():
                self.key = pickle.loads(self.keys1) 
                if self.key == indeks:
                    break

                    

def main():
    
    root = Tk()
    root.title("Satış Ekranı")
    app = Example(root)
    root.mainloop()
    
main()
