import pandas as pd

df = pd.read_csv("C:/Users/Ahmet Burak Yıldız/Downloads/cars_tr.csv")

df["fiyat(TRY)"] = df["fiyat(TRY)"].astype(str) #fiyat sütununu önce string'e çevirir
df["fiyat(TRY)"] = df["fiyat(TRY)"].str.replace(r"[^\d]", "", regex=True) #sonra ₺, nokta, boşluk, vb. karakterleri temizler
df["fiyat(TRY)"] = pd.to_numeric(df["fiyat(TRY)"], errors="coerce") #fiyat sütunu numerik sayıya çevirilir

istanbul_fiyatlar = df[df["il"] == "İstanbul"]["fiyat(TRY)"] #İstanbul'da satılan araçların fiyatları
diger_fiyatlar = df[df["il"] != "İstanbul"]["fiyat(TRY)"] #İstanbul harici illerimizde satılan araçların fiyatları

print("İstanbul'daki fiyat sayısı:", len(istanbul_fiyatlar.dropna()))
print("Diğer şehirlerdeki fiyat sayısı:", len(diger_fiyatlar.dropna()))

