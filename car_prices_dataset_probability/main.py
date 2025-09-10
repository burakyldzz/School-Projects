#KÜTÜPHANELER-------------------------------------------------------------------------------------------------------------------

import pandas as pd
#internetten aldığım veri setini işleyebilmek için dahil ediyorum

import numpy as np
#z değerini kullanmak ve Q değerlerini bulmak için ekledim

from scipy import stats
#chi-square kritik değerlerini kullanmak için ekledim

from math import sqrt
#istatistiksel tanımlayıcıların hesaplanmasında karekök alma işlemini kullanacağım için
#matematik kütüphanesinden sqrt yani karekök fonksiyonunu dahil ediyorum

#VERİLERİ OKUMA VE FİLTRELEME-------------------------------------------------------------------------------------------------------------------

df = pd.read_csv("C:/Users/Ahmet Burak Yıldız/Downloads/cars_tr.csv")

df["fiyat(TRY)"] = df["fiyat(TRY)"].astype(str) #fiyat sütununu önce string'e çevirir
df["fiyat(TRY)"] = df["fiyat(TRY)"].str.replace(r"[^\d]", "", regex=True) #sonra ₺, nokta, boşluk, vb. karakterleri temizler bu sayede sadece sayılar kalır
df["fiyat(TRY)"] = pd.to_numeric(df["fiyat(TRY)"], errors="coerce") #fiyat sütunu numerik sayıya çevirilir

istanbul_fiyatlar = df[df["il"] == "İstanbul"]["fiyat(TRY)"] #İstanbul'da satılan araçların fiyatları
diger_fiyatlar = df[df["il"] != "İstanbul"]["fiyat(TRY)"] #İstanbul harici illerimizde satılan araçların fiyatları

#İSTATİSTİKSEL TANIMLAYICILARIN HESAPLANMASI-------------------------------------------------------------------------------------------------------------------
def hesapla_mean(series): #bu fonksiyon kendisine gönderilen listenin mean değerini hesaplıyor
    veri = series.dropna() #gönderilen listede NaN (bilgisi bulunmayan veri) varsa onu listeden çıkarıyoruz
    if len(veri) == 0:
        return None  #boş liste varsa None döndür
    return sum(veri) / len(veri)


hesaplanan_ortalama = hesapla_mean(diger_fiyatlar) #burada parantez içinde olan değer (istanbul/diğer) fonksiyona gönderiliyor, sonuç aşağıda print ediyor.
print(f"Ortalama fiyat: {hesaplanan_ortalama:.2f} TL")



#-------------------------------------------------------------------------------------------------------------------
def hesapla_median(series): #bu fonksiyon kendisine gönderilen listenin median değerini hesaplıyor
    veri = series.dropna() #gönderilen listede NaN (bilgisi bulunmayan veri) varsa onu listeden çıkarıyoruz
    if len(veri) == 0:
        return None  # Boş liste varsa None döndür
    sirali = sorted(veri)  #küçükten büyüğe sıralar
    n = len(sirali)
    orta = n // 2

    if n % 2 == 1:
        return sirali[orta]  #tek sayıda eleman varsa ortadaki
    else:
        return (sirali[orta - 1] + sirali[orta]) / 2  #çiftse ortadaki iki verinin ortalaması

medyan_fiyat = hesapla_median(diger_fiyatlar) #burada parantez içinde olan değer (istanbul/diğer) fonksiyona gönderiliyor, sonuç aşağıda print ediyor.
print(f"Medyan fiyat: {medyan_fiyat:.2f} TL")



#-------------------------------------------------------------------------------------------------------------------
def hesapla_variance(series): #bu fonksiyon kendisine gönderilen listenin variance değerini hesaplıyor
    veri = series.dropna() #gönderilen listede NaN (bilgisi bulunmayan veri) varsa onu listeden çıkarıyoruz
    n = len(veri) #listesinin sayısını hesaplıyoruz
    if n < 2:
        return None  # En az 2 veri gerekli
#varyans hesaplanması (lecture 7 sunumunun 30.sayfasındaki formüle göre)
    toplam_kareler = sum([x**2 for x in veri]) #her değerin karesini alır ve toplar
    ortalama = hesapla_mean(series) #ortalama hesaplar
    varyans = (toplam_kareler - n * (ortalama ** 2)) / (n - 1) #formülde yerine koyup hesaplama yapar

    return varyans

varyans_fiyat = hesapla_variance(diger_fiyatlar) #burada parantez içinde olan değer (istanbul/diğer) fonksiyona gönderiliyor, sonuç aşağıda print ediyor.
print(f"Fiyatların varyansı: {varyans_fiyat:.2f} TL")



#-------------------------------------------------------------------------------------------------------------------
def hesapla_standart_deviation(series): #bu fonksiyon kendisine gönderilen listenin standart deviation değerini hesaplıyor
    varyans = hesapla_variance(series) #std değeri varyans değerinin kareköküne eşit olduğu için önce varyansı hesaplaması için gerekli fonksiyona gönderiyorum
    if varyans == None: #boş değer dönmesi durumunda bir hata kontrolü
        return None
    standart_deviation = sqrt(varyans) #burada da varyansın karekökünü alıyorum

    return standart_deviation

std = hesapla_standart_deviation(diger_fiyatlar) #burada parantez içinde olan değer (istanbul/diğer) fonksiyona gönderiliyor, sonuç aşağıda print ediyor.
print(f"Standart deviatlation: {std:.2f} TL")



#-------------------------------------------------------------------------------------------------------------------
def hesapla_standard_error(series): #bu fonksiyon kendisine gönderilen listenin standart error değerini hesaplıyor
    veri = series.dropna()
    n = len(veri) #listesinin sayısını hesaplıyoruz
    if n < 2:
        return None  #yetersiz veri varsa hata döndür
    standart_sapma = hesapla_standart_deviation(veri)
    standard_error = standart_sapma / sqrt(n) #standart sapmayı listedeki sayının kareköküne bölüyoruz
    return standard_error

se = hesapla_standard_error(diger_fiyatlar) #burada parantez içinde olan değer (istanbul/diğer) fonksiyona gönderiliyor, sonuç aşağıda print ediyor.
print(f"Standart hata: {se:.2f}")



#Q1, Q3 HESAPLANMASI-------------------------------------------------------------------------------------------------------------------
q1_diger = np.percentile(diger_fiyatlar, 25)        #burada prencentile formülü ile Q1 (25) ve Q3 (75) hesaplayıp yazdırıyor
q1_istanbul = np.percentile(istanbul_fiyatlar, 25)
q3_diger = np.percentile(diger_fiyatlar, 75)
q3_istanbul = np.percentile(istanbul_fiyatlar, 75)
print("1. Çeyrek (Q1) İstanbul:", q1_istanbul)
print("1. Çeyrek (Q1) Diğer:", q1_diger)
print("3. Çeyrek (Q3) İstanbul:", q3_istanbul)
print("3. Çeyrek (Q3) Diğer:", q3_diger)



#CONFIDENCE INTERVAL-------------------------------------------------------------------------------------------------------------------
    #mean için ci
z = 1.96 #%95 güven aralığı için z değeri
mean_for_ci=hesapla_mean(diger_fiyatlar) #istanbul veya diğer illerden hangisi için ci(confidence interval) bulmak istiyorsak buraya onu yazıyoruz
ci_mean_lower = mean_for_ci - z * (hesapla_standart_deviation(diger_fiyatlar)/sqrt(len(diger_fiyatlar)))
ci_mean_upper = mean_for_ci + z * (hesapla_standart_deviation(diger_fiyatlar)/sqrt(len(diger_fiyatlar)))
#yukarıdaki iki satır confidence interval hesaplamasının alt ve üst sınırını hesaplıyor
# (istanbul için hesaplıyor diğerleri için parantez içindeki kısımlar diğer_fiyatlar olarak değiştirilmeli)
print(f"%95 Güven Aralığı (Mean): [{ci_mean_lower:.2f}, {ci_mean_upper:.2f}] TL") #burda sonuçları yazdırıyoruz

    #variance için ci(chi-square test)
#[(n-1).(s^2)/ x^2(a/2) , (n-1).(s^2)/ x^2(1-a/2)] -> chi-square test
#a = 1 - 0.95 = 0.05 güven düzeyi
#n-1 serbestlik derecesidir = örneklem sayısı -1

n = len(diger_fiyatlar) #istanbul veya diğer için fiyatların adedi
varyans = hesapla_variance(diger_fiyatlar) #varyans hesaplıyoruz

# ki-kare kritik değerlerini bulmak için eklediğimiz kütüphaneyi kullanıyoruz
chi2_lower = stats.chi2.ppf(0.975, n-1) #1 - a/2 = 0.975
chi2_upper = stats.chi2.ppf(0.025, n-1) #a/2 = 0.05 / 2 = 0.025

ci_alt = ((n-1) * varyans) / chi2_lower
ci_ust = ((n-1) * varyans) / chi2_upper
print(f"%95 Güven aralığı (varyans): [{ci_alt:.2f}, {ci_ust:.2f}]")



#MINIMUM SAMPLE SIZE-------------------------------------------------------------------------------------------------------------------

z = 1.645  # %90 güven düzeyi için z-değeri
#E = 1154820.95(mean)  * 0.1 = 115482 istanbul için maksimum hata payı(ortalama değerin 0.1 i)
#E = 690733.82(mean) * 0.1 = 69073  diğer için maksimum hata payı(ortalama değerin 0.1 i)
s1 = hesapla_standart_deviation(istanbul_fiyatlar)
s2 = hesapla_standart_deviation(diger_fiyatlar) #girilen değer için standart sapma

mi = (z * s1 / 115482) ** 2 #minimum örneklem büyüklüğü(istanbul için hata payı ile hesaplanan)
print(f"Gerekli minimum örneklem büyüklüğü(İstanbul): {mi}")
md = (z * s2 / 69073) ** 2 #minimum örneklem büyüklüğü(Diğer için hata payı ile hesaplanan)
print(f"Gerekli minimum örneklem büyüklüğü(Diğer): {md}")



#HYPOTHESIS TESTING-------------------------------------------------------------------------------------------------------------------
    #t-test
x1 = hesapla_mean(istanbul_fiyatlar) #ortalamalar hesaplandı
x2 = hesapla_mean(diger_fiyatlar)

s1_sq = hesapla_variance(istanbul_fiyatlar) #varyanslar hesaplandı
s2_sq = hesapla_variance(diger_fiyatlar)

n1 = len(istanbul_fiyatlar) #örneklem uzunluğu hesaplandı
n2 = len(diger_fiyatlar)

t_stat = (x1 - x2) / sqrt((s1_sq / n1) + (s2_sq / n2)) # formülde yerine yerleştirildi
print(f"Hesaplanan t-istatistiği: {t_stat:.4f}")