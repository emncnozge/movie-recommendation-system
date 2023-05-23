import csv
import nltk
from nltk.corpus import stopwords

# Stop words listesini indirmek için bu satırı çalıştırın
nltk.download('stopwords')

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))  # İngilizce stop words listesi
    words = text.split()  # Metni kelimelere ayır
    filtered_words = [word for word in words if word.lower() not in stop_words]  # Stop words olmayan kelimeleri filtrele
    filtered_text = ' '.join(filtered_words)  # Filtrelenmiş kelimeleri tekrar birleştir
    return filtered_text

input_file = 'reviewsClean.csv'  # Giriş CSV dosyasının adı
output_file = 'output.csv'  # Çıkış CSV dosyasının adı
csv.field_size_limit(2**31 - 1)

with open(input_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames
    data = []
    for row in reader:
        row['reviews'] = remove_stopwords(row['reviews'])
        data.append(row)

with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("Stop words kaldırma işlemi tamamlandı. Sonuç dosyası:", output_file)
