'''
 * Descripción: Consulta masiva de clima y amenaza para clientes agro
 * documentos relacionados: Consulta API de clima
 * autores: Mayra Melo, Edwin Torres
 * email: edwin.torres@segurosbolivar.com
 * version: 1.0.0
 * status: <develop_released_final>
 * fecha: <fecha_ultima_actualizacion> 
 * --------------------------------- TODO -------------------------------------------------
 * Lista de feature por hacer
 * ----------------------------------------------------------------------------------------
 *
 * --------------------------------- ISSUES -----------------------------------------------
 * Lista de prblemas conocidos
 * ----------------------------------------------------------------------------------------
'''

import requests, pdb, datetime, json, os, datetime
import pandas as pd

def amenazaSB(id, lat, lon):
  '''
  Código usado para la extracción de información histórica del país
  historico(lat = 3.5411832796311127, lon = -76.49579105674458, fecha = '2022-01-09')
  
 
  Descripción general de la función:
  Función que extrae los pronósticos del clima y los valores de amenaza para un archivo masivo

  Args:
    id (str) : Id del cliente
    lat (int) : Latitud en forma decimal
    lon (int) : Longitud en forma decimal
    

  Returns:
    return (tipo) : Descripcion del elemento retornado

  '''
 
  lat = str(lat)
  lon = str(lon)
 
  url = f'https://www.segurosbolivar.com/arcgis/rest/services/ServiciosAgro/amenazasAgro/GPServer/agro/execute?longitud={lon}&latitud={lat}&env%3AoutSR=&env%3AprocessSR=&returnZ=false&returnM=false&returnTrueCurves=false&returnFeatureCollection=false&context=&f=json'
  print(url)

  ## Clima
  url2 = f'http://ec2-35-153-192-47.compute-1.amazonaws.com:8098/pronosticoClima/?lat={lat}&lon={lon}&id=id1&lugar=colombia'
  print(url2)

  res = requests.get(url)
 
  data = res.json()

  res2 = requests.get(url2)
 
  data2 = res2.json()

  bdAmen = pd.json_normalize(data['results'][0]['value']['features'][0]['attributes'])

  bdPron = pd.json_normalize(data2[1])

  union = pd.concat([bdAmen, bdPron], axis = 1)
  union['id'] = id


 
  return(union)


base=pd.read_csv('C:/Users/aleja/OneDrive/Documents/BASES_ENTRADA_Y_SALIDA/Coordenadas_entrada.csv',sep=';',decimal=',',encoding='latin-1')



#pdb.set_trace()
antes = datetime.datetime.now()
baseVacia = pd.DataFrame([])
for id1, lat, lon in zip(base.ID, base.LAT, base.LONG):
  print(id1, lat, lon)
  try:
      union = amenazaSB(lat = lat, lon = lon, id = id1)
     
  except:
      continue
  baseVacia = pd.concat([baseVacia, union])

ahora = datetime.datetime.now()
baseVacia
#\
#from google.colab import files
baseVacia.to_csv('C:/Users/aleja/OneDrive/Documents/BASES_ENTRADA_Y_SALIDA/SALIDA PRONOSTICO.csv')
#files.download('filename.csv')
#print(ahora- antes)
