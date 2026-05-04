import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# 1. DOSYA YOLLARINI OTOMATİK BULMA (Kalıcı Çözüm)
# Kodun çalıştığı yeri bulup, ana klasörü (BASE_DIR) belirliyoruz.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'network_data.csv')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Eğer results klasörü yoksa veya yanlışlıkla silindiyse hata vermesin diye otomatik oluşturuyoruz.
os.makedirs(RESULTS_DIR, exist_ok=True)

# 2. VERİ SETİNİ YÜKLEME
# Bulduğumuz kesin dosya yolunu kullanarak veriyi okuyoruz (ayırıcı: noktalı virgül).
data = pd.read_csv(DATA_PATH, sep=';')

# 3. GRAF NESNESİNİ OLUŞTURMA
G = nx.Graph()

# 4. DÜĞÜM VE KENARLARI EKLEME
for index, row in data.iterrows():
    G.add_edge(row['Source_Node'], 
               row['Destination_Node'], 
               weight=row['Cost_USD'])

# 5. MINIMUM SPANNING TREE (MST) HESAPLAMA
mst = nx.minimum_spanning_tree(G, weight='weight')

# 6. SONUÇLARIN HESAPLANMASI VE KAYDEDİLMESİ
total_cost = mst.size(weight='weight')
results_text = f"Minimum Spanning Tree Toplam Kablolama Maliyeti: {total_cost} USD\n"
results_text += "Secilen Baglantilar:\n"

for u, v, d in mst.edges(data=True):
    results_text += f"- {u} ile {v} arasi: {d['weight']} USD\n"

# Metin dosyasını güvenli yola (results klasörüne) kaydetme
output_txt_path = os.path.join(RESULTS_DIR, 'solution_output.txt')
with open(output_txt_path, 'w', encoding='utf-8') as f:
    f.write(results_text)

# 7. GÖRSELLEŞTİRME
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G)

nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray', width=1)
nx.draw_networkx_edges(mst, pos, edge_color='red', width=3)
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Kampus Fiber Optik Ag Optimizasyonu (MST)")
plt.axis('off')

# Grafiği güvenli yola (results klasörüne) kaydetme
output_png_path = os.path.join(RESULTS_DIR, 'network_visualization.png')
plt.savefig(output_png_path)

print(f"Islem tamamlandi! Sonuclar su klasore kaydedildi: {RESULTS_DIR}")