import pandas as pd 
import random
from faker import Faker
from datetime import datetime
import os

fake = Faker("es_MX")

RAW_CSV = "data/raw/calidad.csv"

PROCESSED_XLSX= "data/processed/datos_limpios.xlsx"

PROCESSED_KPIS_XLSX = "data/processed/kpis_calidad.xlsx"

def generar_datos_calidad(num_registros=300):
    data= []
    maquinas = ["Maq_A","Maq_B","Maq_C",None]
    turnos = ["Turno_1","Turno_2","Turno_3",""]
    productos=["producto_X","Producto_Y","Producto_Z",None]

    for i in range (1 , num_registros +1 ):
     registro = {
        "registro_id":i,
        "fecha":fake.date_between(start_date="-1y", end_date="today")
        ,"maquina": random.choice(maquinas),
        "turno": random.choice(turnos),
        "producto": random.choice(productos),
        "piezas_producidas": random.randint(-5,50),
        "piezas_defectuosas": random.randint(-3,10)
     }
     data.append(registro)
    
    
    df = pd.DataFrame(data)
    os.makedirs ("data/raw",exist_ok=True)
    df.to_csv(RAW_CSV, index=False)
    return df 

def leer_datos():
   return pd.read_csv(RAW_CSV)

def limpiar_datos(df):
    total_registros = len(df)
    df_limpio = df[
        (df["piezas_producidas"] > 0) &
        (df["piezas_defectuosas"] >= 0) &
        df["maquina"].notna() &
        df["turno"].notna() &
        df["producto"].notna() &
        (df["maquina"].str.strip() != "") &
        (df["turno"].str.strip() != "") &
        (df["producto"].str.strip() != "")
    ]
    eliminados = total_registros - len(df_limpio)
    return df_limpio, total_registros, eliminados

def calcular_kpis(df,umbral_defectos=0.05):
   df["tasa_defectos"] = df ["piezas_defectuosas"]/df["piezas_producidas"]
   df["bandera_calidad"] = df["tasa_defectos"].apply(lambda x: "OK" if x <= umbral_defectos else "NO OK")

   kpis = {
      "total_registros":len(df),
      "total_producidas":df["piezas_producidas"].sum(),
      "total_defectuosas":df["piezas_defectuosas"].sum(),
      "promedio_tasa_defectos": df["tasa_defectos"].mean()

   }
   df_kpis = pd.DataFrame([kpis])
   return df, df_kpis


def guardar_excel(df_limpio,df_kpis):
     os.makedirs("data/processed",exist_ok= True)
     with pd.ExcelWriter(PROCESSED_XLSX, engine="openpyxl" ) as writer:
      df_limpio.to_excel(writer,sheet_name = "datos_limpios",index=False)
      df_kpis.to_excel(writer,sheet_name = "kpis_calidad",index=False)

def main():
   print("Iniciando ETL de calidad")

   print("Generando datos de calidad")

   generar_datos_calidad()

   print("Leyendo datos")
   df = leer_datos()

   print("Aplicando reglas de calidad")
   df_limpio,total,eliminado = limpiar_datos(df)

   print("Calculamos metricas de calidad")
   df_limpio,df_kpis = calcular_kpis(df_limpio)

   print("Guardando Excel para Power Bi")
   guardar_excel(df_limpio,df_kpis)

   print("\n Resumen ETL")
   print(f"Registros totales:{total}")
   print(f"Registros eliminados{eliminado}")
   print(f"Registros finales{len(df_limpio)}")
   print(f"Total producidos {df_kpis['total_producidas'][0]}")
   print(f"Total defectuosas{df_kpis['total_defectuosas'][0]}")
   print(f"Promedio tasa de defectos: {df_kpis['promedio_tasa_defectos'][0]:.2%}")

   print("ETL Finalizado correctamente.Excel listo para Power BI")

if __name__ == "__main__":
    main()
