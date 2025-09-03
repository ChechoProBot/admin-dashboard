from backend.db_utils import get_propiedades, get_unidades, get_propietarios

print('🔍 VERIFICACIÓN DE FUNCIONES DE BASE DE DATOS')
print('=' * 50)

print('\n🏢 PROPIEDADES:')
propiedades = get_propiedades()
print(f'Total: {len(propiedades)}')
for prop in propiedades:
    print(f'  ID: {prop["id"]}, Nombre: {prop["nombre"]}, Dirección: {prop["direccion"]}')

print('\n🏠 UNIDADES:')
unidades = get_unidades()
print(f'Total: {len(unidades)}')
for unidad in unidades:
    print(f'  ID: {unidad["id"]}, Propiedad: {unidad["propiedad"]}, Unidad: {unidad["unidad"]}, Coeficiente: {unidad["coeficiente"]}')

print('\n👥 PROPIETARIOS:')
propietarios = get_propietarios()
print(f'Total: {len(propietarios)}')
for prop in propietarios:
    print(f'  ID: {prop["id"]}, Nombre: {prop["nombre"]}, Email: {prop["email"]}, Propiedad: {prop["propiedad"]}, Unidad: {prop["unidad"]}')

print('\n✅ Todas las funciones de base de datos están funcionando correctamente!')
