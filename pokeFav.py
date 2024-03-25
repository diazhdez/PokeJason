import conexion as db
import requests

# Solicitar al usuario que ingrese el nombre del Pokémon
pokemon_name = input("Ingrese el nombre del Pokémon: ")

# Establecer conexión con la base de datos
cursor = db.conexion.cursor()

# Crear tabla para almacenar los datos de los Pokémon favoritos
cursor.execute("CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY, name TEXT, type TEXT)")

# Hacer la solicitud a la API para obtener información sobre el Pokémon especificado
api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
response = requests.get(api_url)

if response.status_code == 200:
    pokemon_data = response.json()
    pokemon_id = pokemon_data["id"]
    pokemon_name = pokemon_data["name"]
    pokemon_types = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
    # Convierte la lista de tipos en una cadena separada por comas
    pokemon_types_str = ", ".join(pokemon_types)

    # Insertar el Pokémon en la tabla de favoritos
    sql = """INSERT INTO favorites (id, name, type) VALUES (%s, %s, %s)"""
    datos = (pokemon_id, pokemon_name, pokemon_types_str)
    cursor.execute(sql, datos)
    db.conexion.commit()
    print(f"Datos de {pokemon_name} guardados correctamente")
else:
    print(f"Error al obtener datos del Pokémon {pokemon_name}")

# Cerrar el cursor y la conexión con la base de datos
cursor.close()
db.conexion.close()
