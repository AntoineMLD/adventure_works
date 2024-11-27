import pandas as pd
import sys

def parquet_to_csv(parquet_file):
    
    try:
        df = pd.read_parquet(parquet_file, engine='pyarrow')  
        # Génére le nom du fichier CSV 
        csv_file = parquet_file.rsplit('.', 1)[0] + '.csv'
        
        # Sauvegarde en CSV
        df.to_csv(csv_file, index=False, header=True)
        print(f"Conversion réussie. Fichier CSV généré : {csv_file}")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_parquet_to_csv.py <chemin_du_fichier_parquet>")
    else:
        parquet_file = sys.argv[1]
        parquet_to_csv(parquet_file)
