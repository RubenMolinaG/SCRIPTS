#!/bin/bash

# Uso: ./<nombre_script>.sh <nombre_dominio>
# Ejemplo: ./as_passwd.sh /opt/wl/wl14/user_projects/domains/DOMINIO_PRUEBAS

DOMAIN=${1?}
DATE=$(date +%Y/%m/%d\ %H:%M:%S)

# Cargar variables de entorno necesarias.
function load_vars(){
	if [[ -f ${1}/bin/setDomainEnv.sh ]]; then
		source ${1}/bin/setDomainEnv.sh
		echo "${DATE} - Variables de entorno cargadas con exito"
		return 0
	else
		echo "${DATE} - Fichero 'setDomainEnv.sh' NO encontrado en la ruta '${DOMAIN}/bin'"
		echo "${DATE} - PATH --> ${1}/bin/setDomainEnv.sh"
		exit 1
	fi
}

# Comprobar si estas en el nodo donde se ejecuta el AS.
function check_AS_node(){
	if [[ ! -f ${DOMAIN}/servers/AdminServer/security/boot.properties ]]; then
		echo "${DATE} - Fichero 'boot.properties' NO encontrado"
		echo "${DATE} - Este script se debe lanzar sobre el nodo que ejecute el AS del dominio"
		exit 1
	fi
}

# Funcion principal
function main(){
	check_AS_node "$@"
	load_vars "$@"
	java weblogic.WLST << EOF
from weblogic.security.internal import BootProperties
BootProperties.load("${DOMAIN}/servers/AdminServer/security/boot.properties", false)
prop = BootProperties.getBootProperties()
print "Username: " + prop.getOneClient()
print "Password: " + prop.getTwoClient()
exit()
EOF
}

# Inicio del script
main "$@"
