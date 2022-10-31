import string
import re
from sys import stdin

tipoVias = ['CARRERA', 'CUENTAS CORRIDAS', 'AVENIDA CARRERA', 'AVENIDA CALLE', 'CIRCUNVALAR', 'AVENIDA CLL',
            'AVENIDA CRA', 'AVENIDA KRA', 'TRANSVERSAL', 'AVENIDA CL', 'AVENIDA KR', 'AVENIDA CR', 'CARRETERA',
            'AUTOPISTA', 'AVENIDA C', 'AVENIDA K', 'CIRCULAR', 'DIAGONAL', 'PEATONAL', 'VARIANTE', 'AVENIDA', 'BULEVAR',
            'TRONCAL', 'PASAJE', 'CALLE', 'PASEO', 'TRANS', 'DIAG', 'CRA', 'KRA', 'CLL', 'CIR', 'CRV', 'AUT', 'VIA',
            'KR', 'CR', 'CL', 'CT', 'CQ', 'CV', 'CC', 'AU', 'AV', 'AC', 'AK', 'BL', 'DG', 'PJ', 'PS', 'PT', 'TV', 'TR',
            'TC', 'VT', 'VI', 'DK', 'DC']

mensaje = ''
aceptacion = True
simbolo = False
tipoViasRurales=['CORREGIMIENTO', 'CARRETERA', 'KILOMETRO', 'PROPIEDAD',
                 'MUNICIPIO',	'HACIENDA',	'VARIANTE',	'ENTRADA',
                 'CAMINO',	'BARRIO',	'PREDIO',	'SECTOR',	'VEREDA',
                 'FINCA',	'CARR',	'CASA',	'CORR',	'LOTE',	'BRR',	'FCA',
                 'MCP',	'SEC',	'VTE',	'VDA',	'VRD',	'VIA',	'CN',	'CT',
                 'CA',	'CS',	'BR',	'EN',	'FI',	'HC',	'KM',
                 'PD',	'LT',	'SC',	'VT',	'VI']

# QO
def estadoInicial(direccion, posicion):
    expresion_numeros = re.compile("[0-9]")
    global mensaje
    global aceptacion
    if len(direccion) == posicion:
        mensaje += '1'
        aceptacion = False
        ###print(aceptacion)
        estadoFinal(direccion, posicion)
    # SALTO DE INICIAL A Q9

    elif direccion[posicion] == ' ':
        # SALTO DE INICIAL A Q9
        ###print('Entra estado inicial espacio')
        estado2(direccion, posicion)

    elif direccion[posicion + 1] in string.ascii_uppercase:
        # SALTO DE A Q9
        ###print('Entra estado inicial sin espacio')
        mensaje += '0'
        estado2(direccion, posicion)
    elif direccion[posicion] in string.ascii_uppercase or expresion_numeros.match(direccion[posicion]):
        mensaje += '0'
        estado2(direccion, posicion)

    else:
        return 'DIRECCION INVALIDA'

def estadoInicialRural(direccion, posicion):
    if direccion.startswith('KILOMETRO') or direccion.startswith('KM'):
        validarKM(direccion, posicion)
    else:
        #print(direccion[posicion+1])
        #print('NO KM')
        estado2Rural(direccion, posicion+1)


def validarKM(direccion, posicion):
    global aceptacion
    global mensaje
    expresion_numeros = re.compile("[0-9]")
    if len(direccion) < posicion + 1:
        #print('1 ESTADO VALIDAR KM')
        aceptacion = False
        mensaje += '1'
        estadoFinal(direccion, posicion)

    elif direccion[posicion]==' ':
        validarKM(direccion, posicion+1)
    elif expresion_numeros.match(direccion[posicion]):
        #print('NUMERO DESPUES OK')
        validarKM(direccion, posicion+1)

    elif (direccion[posicion-1]=='+' or direccion[posicion]=='+' or direccion[posicion:posicion+3]=='MAS') and (expresion_numeros.match(direccion[posicion-1]) or expresion_numeros.match(direccion[posicion-2])):
        if direccion[posicion:posicion+3]=='MAS':
            aceptacion = False
            #print('VALIDAR MAS DESPUES DE KM')
            validarMasKm(direccion, posicion+3)
        else:
            aceptacion = False
            #print('VALIDAR + DESPUES DE KM')
            validarMasKm(direccion, posicion+1)
    elif direccion[posicion] in string.ascii_uppercase:
        for i in tipoViasRurales:

            if direccion[posicion:posicion+len(i)] in tipoViasRurales:
                #print(direccion[posicion:posicion + len(i)])
                aceptacion = False
                #print('ENTRA VALIDAR SEGUNDO TIPO DE VIA')
                estado3Rural(direccion, posicion+len(i))
                return True
    else:
        mensaje+='2'
        estadoFinal(direccion, posicion)

def validarMasKm(direccion, posicion):
    #print(direccion[posicion])
    global aceptacion
    global mensaje
    expresion_numeros = re.compile("[0-9]")
    if len(direccion) < posicion + 1:
        #print('1 ESTADO VALIDAR KM +')
        aceptacion = False
        mensaje += '1'
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ':
        validarMasKm(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion]) or direccion[posicion]=='M':
        #print('NUMERO DESPUES DE MAS')
        estado2Rural(direccion, posicion + 1)
    elif direccion[posicion] == ' ' and expresion_numeros.match(direccion[posicion]):
        mensaje+='0'
        aceptacion = False
        estado2Rural(direccion, posicion + 1)
    elif direccion[posicion] in string.ascii_uppercase:
        #print('LETRA DESPUES DE MAS')
        mensaje+='1'
        aceptacion= False
        estadoFinal(direccion, posicion)

#NOMBRE PRIMER TIPO DE VIA
def estado2Rural(direccion, posicion):
    expresion_numeros = re.compile("[0-9]")
    global aceptacion
    global mensaje
    if len(direccion) < posicion + 1:
        mensaje += '1'
        aceptacion = False
        estadoFinal(direccion, posicion)

    elif direccion[posicion]==' ':
        estado2Rural(direccion, posicion+1)
    elif direccion[posicion] in string.ascii_uppercase or expresion_numeros.match(direccion[posicion]):
        for i in tipoViasRurales:

            if direccion[posicion:posicion+len(i)] in tipoViasRurales:
                #print(direccion[posicion:posicion + len(i)])
                aceptacion = False
                #print('ENTRA VALIDAR SEGUNDO TIPO DE VIA')
                estado3Rural(direccion, posicion+len(i))
                return True

        aceptacion = False
        #print(direccion[posicion] + 'entra')
        estado2Rural(direccion, posicion + 1)


# VALIDAR SEGUNDO TIPO DE VIA RURAL
def estado3Rural (direccion, posicion):
    #print('Segundo tipo de via rural')
    global mensaje
    global aceptacion

    if direccion[posicion]==' ':
        aceptacion = False
        mensaje+='0'
        estado3Rural(direccion, posicion+1)
    else:
        aceptacion = False
        mensaje += '0'
        estado4Rural(direccion, posicion)


def estado4Rural (direccion, posicion):
    #print('Validar complemento segund tipo de via')
    expresion_numeros = re.compile("[0-9]")
    global aceptacion
    global mensaje
    if len(direccion) < posicion + 1:
        #print('1 ESTADO FINAL RURAL')
        mensaje += '1'
        aceptacion = True
        estadoFinal(direccion, posicion+1)

    elif direccion[posicion] in string.ascii_uppercase or expresion_numeros.match(direccion[posicion]) or direccion[posicion]==' ':
        mensaje += '0'
        #print(direccion[posicion] + ' entra')
        aceptacion = True
        estado4Rural(direccion, posicion+1)

# Q9
def estado2(direccion, posicion):

    global mensaje
    global aceptacion
    expresion_numeros = re.compile("[0-9]")
    if len(direccion) < posicion + 1:
        ###print('1 ESTADO 2 TAMAÑO')
        mensaje += '1'
        aceptacion = False
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ':
        ###print('SALTO ESPACIO')
        estado2(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion]):
        ###print('Salto Q9 a Q10/ Salto de Q10 a Q10')
        # Q9   =>Q10
        # Q10  =>Q10
        mensaje += '0'
        estado2(direccion, posicion + 1)
    elif direccion[posicion] in string.ascii_uppercase:
        # Q10 =>Q12
        # Q9  =>Q11
        # Salto a estado 11
        ###print('Salto Q9 a Q11 o Q10 a Q12 o Q10 a Q11 o Q10 a Q13 ----CON/SIN ESPACIOS----')
        estado3(direccion, posicion)

    elif direccion[posicion:posicion + 6] == 'NUMERO':
        ###print('VARIABLE NUMERO')
        mensaje += '0'
        aceptacion = False
        estado6(direccion, posicion + 6)
    elif direccion[posicion:posicion + 3] == 'NO.' or direccion[posicion:posicion + 3] == 'NRO' or direccion[
                                                                                                   posicion:posicion + 3] == 'NUM':
        mensaje += '0'
        #print('ENTRA')
        ###print('VARIABLES NO. O NUM O NRO')
        aceptacion = False
        estado6(direccion, posicion + 2)
    elif direccion[posicion:posicion + 2] == 'NO' or direccion[posicion:posicion + 2] == 'N°' or direccion[
                                                                                                 posicion:posicion + 2] == 'N.':
        mensaje += '0'
        ###print('VARIABLES NO-N°-N.')
        aceptacion = False
        estado6(direccion, posicion + 2)
    elif direccion[posicion] == 'N' or direccion[posicion] == '#' or direccion[posicion] == '-':
        mensaje += '0'
        ###print('VARIABLES # O N')
        aceptacion = False
        estado8(direccion, posicion + 1)


# Q11
def estado3(direccion, posicion):
    global mensaje
    global aceptacion
    if len(direccion) < posicion + 1:
        ###print('1 ESTADO 3 TAMAÑO')
        aceptacion = False
        mensaje += '1'
        estadoFinal(direccion, posicion)
    elif direccion[posicion:posicion + 3] == 'BIS':
        aceptacion = False
        ###print('SALTO Q13 A Q14 PALABRA BIS')
        # SALTO PARA ENTRAR A BIS
        mensaje += '0'
        estado5(direccion, posicion + 3)
    elif direccion[posicion:posicion + 4] == 'ESTE':
        ###print('SALTO Q13 A Q19 ESTE')
        mensaje += '0'
        estado6(direccion, posicion + 4)
    elif direccion[posicion:posicion + 5] == 'NORTE' or direccion[posicion:posicion + 5] == 'OESTE':
        ###print('SALTO Q13 A Q19 OESTE O NORTE')
        mensaje += '0'
        aceptacion = False
        estado6(direccion, posicion + 5)
    elif direccion[posicion:posicion + 3] == 'SUR':
        ###print('SALTO Q13 A Q19 SUR')
        mensaje += '0'
        aceptacion = False
        estado6(direccion, posicion + 3)
    elif direccion[posicion] in string.ascii_uppercase or direccion[posicion] == ' ':
        # Q11 => Q11
        ###print('SALTO ESTADO Q11 A Q11')
        mensaje += '0'
        aceptacion = False
        estado3(direccion, posicion + 1)
    else:
        estado4(direccion, posicion)


def estado4(direccion, posicion):
    global mensaje
    expresion_numeros = re.compile("[0-9]")
    if len(direccion) < posicion + 1:
        ###print('1 ESTADO 4 TAMAÑO')
        mensaje += '1'
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ':
        ###print('SALTO 13 A 14 ESPACIO')
        estado4(direccion, posicion + 1)
    # SALTO A ESATDO DE BIS
    # Q13 => Q14
    elif direccion[posicion:posicion + 2] == 'BIS':
        ###print('SALTO DE 13 A 14 ---DIRECCION CON BIS---')
        mensaje += '0'
        estado5(direccion, posicion + 2)
    else:
        ###print('DIRECCION SIN BIS')
        estado6(direccion, posicion)


# ESTADO PARA LA PALABRA BIS
def estado5(direccion, posicion):
    global mensaje
    global aceptacion
    expresion_numeros = re.compile("[0-9]")
    if len(direccion) < posicion + 1:
        ###print('1 ESTADO 5 TAMAÑO')
        aceptacion = aceptacion
        mensaje += '1'
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ' or direccion[posicion] == '#':
        ###print('SALTO ESPACIO BIS')
        estado5(direccion, posicion + 1)
    # BIS SIN COMPLEMENTO
    elif direccion[posicion] == ' ' or expresion_numeros.match(direccion[posicion]):
        ###print('BIS SIN COMPLEMENTO')
        estado6(direccion, posicion)
        # COMPLEMENTO BIS
    elif direccion[posicion] in string.ascii_uppercase:
        ###print('VALIDAR COMPLEMENTO BIS')
        estado7(direccion, posicion)


def estado7(direccion, posicion):
    global mensaje
    global aceptacion
    ###print(len(direccion[posicion:posicion+2]))

    ###print(direccion[posicion] in string.ascii_uppercase)

    expresion_numeros = re.compile("[0-9]")
    if len(direccion) < posicion + 1:
        ###print('1 ESTADO 7 TAMAÑO')
        aceptacion = aceptacion
        mensaje += '1'
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ':
        estado7(direccion, posicion + 1)
    elif direccion[posicion:posicion + 5] == 'NORTE' or direccion[posicion:posicion + 4] == 'ESTE' or direccion[posicion:posicion + 5] == 'OESTE' or direccion[posicion:posicion + 3] == 'SUR':
        if direccion[posicion:posicion + 5] == 'NORTE':
            mensaje += '0'
            ###print('NORTE')
            estado6(direccion, posicion + 5)
        elif direccion[posicion:posicion + 4] == 'ESTE':
            mensaje += '0'
            ###print('ESTE')
            estado6(direccion, posicion + 4)
        elif direccion[posicion:posicion + 5] == 'OESTE':
            mensaje += '0'
            ###print('OESTE')
            estado6(direccion, posicion + 5)
        elif direccion[posicion:posicion + 3] == 'SUR':
            mensaje += '0'
            ###print('SUR 1')
            estado6(direccion, posicion + 3)
    elif (direccion[posicion:posicion + 3] in string.ascii_uppercase) and \
            (direccion[posicion:posicion + 5] != 'NORTE' or direccion[posicion:posicion + 4] != 'ESTE' or
             direccion[posicion:posicion + 5] != 'OESTE' or direccion[posicion:posicion + 3] != 'SUR') \
            and len(direccion[posicion:posicion+3])==3:
        mensaje += '1'
        ###print(len(direccion[posicion:posicion + 3]))
        aceptacion = False
        ###print('1 ESTADO 7 BIS CON 3 LETRAS SEGUIDAS SIN ESPACIO')
        estado6(direccion, posicion+3)
    elif len(direccion[posicion:posicion+3])==3 and direccion[posicion] in string.ascii_uppercase and direccion[posicion + 1] in string.ascii_uppercase and expresion_numeros.match(direccion[posicion + 2]) :
        ###print('1 ESTADO 7 TAMAÑO Bis Letra LETRA NUMERO --NO APLICA')
        mensaje += '1'
        estado6(direccion, posicion + 1)

    elif len(direccion[posicion:posicion+2])==2 and direccion[posicion] in string.ascii_uppercase and direccion[posicion + 1] in string.ascii_uppercase:
        for i in tipoVias:
            if direccion[posicion:posicion + len(i)] in tipoVias:
                ###print(direccion[posicion:posicion + len(i)])
                ###print('Entra validar via generadora')
                ###print(posicion + len(i))
                estado6(direccion, posicion + len(i))
                break

        ###print('BIS LETRA LETRA')
        mensaje += '0'
        estado6(direccion, posicion + 2)
    elif expresion_numeros.match(direccion[posicion]) and expresion_numeros.match(direccion[posicion + 1]):
        ###print('Bis Letra nunmero')
        mensaje += '0'
        estado7(direccion, posicion + 1)
    elif len(direccion[posicion:posicion])>=3 and (direccion[posicion] in string.ascii_uppercase and expresion_numeros.match(
            direccion[posicion + 1]) or expresion_numeros.match(direccion[posicion + 1]) and expresion_numeros.match(
            direccion[posicion])):
        ###print('BIS LETRAS NUMEROS LETRA')
        estado7(direccion, posicion + 1)
    elif len(direccion[posicion:posicion+3])==3 and (expresion_numeros.match(direccion[posicion - 1]) and direccion[
        posicion + 1] in string.ascii_uppercase or expresion_numeros.match(direccion[posicion]) and direccion[
        posicion + 1] in string.ascii_uppercase):
        ###print('BIS LETRA NUMERO LETRA')
        mensaje += '0'
        estado6(direccion, posicion + 1)
    elif direccion[posicion] in string.ascii_uppercase or direccion[posicion + 1] == ' ':
        ###print('BIS LETRA O BIS SOLO')
        estado6(direccion, posicion + 1)
    else:
        estado6(direccion, posicion + 1)


# ESTADO 21 CARACTER # EN PLACA
def estado6(direccion, posicion):
    global simbolo
    expresion_numeros = re.compile("[0-9]")
    global mensaje
    global aceptacion

    if len(direccion) < posicion + 1:
        if (direccion[posicion - 1] == '-' or direccion[posicion - 1] == ' ' or expresion_numeros.match(direccion[posicion - 1])) and (
                direccion[posicion - 2] in string.ascii_uppercase or expresion_numeros.match(direccion[posicion - 2])):
            ###print('SEIS FALSE')
            aceptacion = False
            aceptacion = aceptacion
            mensaje += '1'
            estadoFinal(direccion, posicion)
        else:
            ###print('1 ESTADO 6 TAMAÑO')
            ###print(aceptacion)
            aceptacion = aceptacion
            mensaje += '1'
            estadoFinal(direccion, posicion)

    elif direccion[posicion] == ' ':
        estado6(direccion, posicion + 1)

    elif direccion[posicion:posicion + 5] == 'NORTE' or direccion[posicion:posicion + 4] == 'ESTE' or direccion[posicion:posicion + 5] == 'OESTE' or direccion[posicion:posicion + 3] == 'SUR':
        if direccion[posicion:posicion + 5] == 'NORTE':

            ###print('NORTE')
            mensaje += '0'
            estado6(direccion, posicion + 5)
        elif direccion[posicion:posicion + 4] == 'ESTE':

            ###print('ESTE')
            mensaje += '0'
            estado6(direccion, posicion + 4)
        elif direccion[posicion:posicion + 5] == 'OESTE':

            ###print('OESTE')
            mensaje += '0'
            estado6(direccion, posicion + 5)
        elif direccion[posicion:posicion + 3] == 'SUR':

            ###print('SUR 2')
            mensaje += '0'
            estado6(direccion, posicion + 3)
    elif direccion[posicion:posicion + 6] == 'NUMERO':
        ###print('VARIABLE NUMERO')
        aceptacion = False
        mensaje += '0'
        estado8(direccion, posicion + 6)
    elif direccion[posicion:posicion + 3] == 'NO.' or direccion[posicion:posicion + 3] == 'NRO' or direccion[
                                                                                                   posicion:posicion + 3] == 'NUM':
        mensaje += '0'
        ###print('VARIABLES NO. O NUM O NRO')
        aceptacion = False
    elif direccion[posicion:posicion + 2] == 'NO' or direccion[posicion:posicion + 2] == 'N°' or direccion[posicion:posicion + 2] == 'N.':
        mensaje += '0'
        ###print('VARIABLES NO-N°-N.')
        aceptacion = False
        estado8(direccion, posicion + 2)
    elif direccion[posicion] == 'N' or direccion[posicion] == '#' or direccion[posicion] == '-':
        mensaje += '0'
        ###print('VARIABLES # O N salto 8')
        aceptacion = False
        simbolo=True
        estado8(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion]) and direccion[posicion - 1] in string.ascii_uppercase:
        mensaje += '1'
        ###print('1 NUMERO DESPUES DE LETRA EN PLACA')
        aceptacion = False
        estado8(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion]) or direccion[posicion:posicion + 3] == 'BIS' \
        or (direccion[posicion] in string.ascii_uppercase and expresion_numeros.match(direccion[posicion-1]) or expresion_numeros.match(direccion[posicion-2])):
        ###print('VALIDAR NUMERO EN LA PLACA ' + direccion[posicion])
        if direccion[posicion:posicion + 3] == 'BIS':
            aceptacion = False
            estado8(direccion, posicion)
        elif expresion_numeros.match(direccion[posicion]) and len(direccion) == posicion:
            ###print('Mne')
            mensaje+='1'
            aceptacion = False
            estado8(direccion, posicion)

        else:
            ###print('Mensaje')
            aceptacion = True
            estado6(direccion, posicion + 1)
    elif direccion[posicion] in string.ascii_uppercase:
        mensaje+='0'
        estado14(direccion, posicion)
    else:
        ###print('1 ESTADO 6 ELSE DIRECTO ' + direccion[posicion])
        mensaje += '1'
        estado8(direccion, posicion + 1)


def estado15viasSecundarios(direccion, posicion):
    global mensaje

    for i in tipoVias:
        size = 0
        if direccion.startswith(i, 0, len(i)) and direccion[posicion:posicion + len(i)]:
            ###print(direccion[posicion:posicion + len(i)])
            ###print(direccion.startswith(i, 0, len(i)))
            mensaje += '1'
            ###print('REPETIDO')
            ###print('AV' in tipoVias)
            estadoFinal(direccion, posicion)
            break

        else:
            return False


# TRANSICION 24-23 O 24-24
def estado8(direccion, posicion):
    global mensaje
    global aceptacion
    expresion_numeros = re.compile("[0-9]")
    if len(direccion) < posicion + 1:
        ###print(direccion[posicion - 1])
        ###print(direccion[posicion - 2])
        if (direccion[posicion - 1] == '-' or direccion[posicion - 1] == ' ' or expresion_numeros.match(
                direccion[posicion - 1])) and (
                direccion[posicion - 2] in string.ascii_uppercase or expresion_numeros.match(direccion[posicion - 2])):
            ###print('8 FALSE')
            aceptacion = True
            aceptacion = aceptacion
            mensaje += '1'
            estadoFinal(direccion, posicion)
        else:
            ###print('1 ESTADO 6 TAMAÑO')
            ###print(aceptacion)
            aceptacion = aceptacion
            mensaje += '1'
            estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ':
        estado8(direccion, posicion + 1)
    elif direccion[posicion:posicion + 3] == 'BIS' and direccion[posicion + 3] != '-':
        aceptacion= False
        ###print('BIS PLACA COMPLEMENTO 0')
        estado11(direccion, posicion + 3)
    elif direccion[posicion:posicion + 3] == 'BIS' and direccion[posicion + 3] == '-':
        ###print('BIS SIN COMPLEMENTO')
        estado12(direccion, posicion + 3)
    elif direccion[posicion:posicion + 5] == 'NORTE' or direccion[posicion:posicion + 4] == 'ESTE' or direccion[posicion:posicion + 5] == 'OESTE' or direccion[posicion:posicion + 3] == 'SUR':
        ###print('Cardinales estado 8')
        mensaje += '0'
        if direccion[posicion:posicion + 5] == 'NORTE':
            ###print('NORTE')
            mensaje += '0'
            estado12(direccion, posicion + 5)
        elif direccion[posicion:posicion + 4] == 'ESTE':
            ###print('ESTE')
            mensaje += '0'
            estado6(direccion, posicion + 4)
        elif direccion[posicion:posicion + 5] == 'OESTE':
            ###print('OESTE')
            mensaje += '0'
            estado12(direccion, posicion + 5)
        elif direccion[posicion:posicion + 3] == 'SUR':
            ###print('SUR 3')
            mensaje += '0'
            estado12(direccion, posicion + 3)
    elif (direccion[posicion] in string.ascii_uppercase or direccion[posicion]==' ') and simbolo==True:
        estado14(direccion, posicion+1)
    elif direccion[posicion] in string.ascii_uppercase and (
            expresion_numeros.match(direccion[posicion - 1]) or expresion_numeros.match(direccion[posicion - 2])):
        if direccion[posicion - 1] in string.ascii_uppercase or expresion_numeros.match(direccion[posicion - 1]) or \
                direccion[posicion - 1] == ' ':
            ###print(direccion[posicion])
            ###print('NUMERO LETRA DESPUES DE # ')
            mensaje += '0'
            estado8(direccion, posicion + 1)
    elif direccion[posicion] in string.ascii_uppercase and direccion[posicion - 1] == ' ' or direccion[posicion-1] == '#' and direccion[posicion] in string.ascii_uppercase:
        ###print('1 ESTADO 8 TAMAÑO SOLO LETRA DESPUES DE # --NO VALIDO--')
        mensaje += '1'
        estado9(direccion, posicion)
    elif direccion[posicion] == ' ':
        estado8(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion]) or direccion[posicion] in string.ascii_uppercase:
        if len(direccion)==posicion:
            mensaje+='1'
            aceptacion = False
        else:
            aceptacion = True
            ###print('NUMEROS DESPUES DE # ' + direccion[posicion])
            mensaje += '0'
            estado8(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion - 1]) and direccion[posicion] in string.ascii_uppercase:
        mensaje += '0'
        aceptacion = True
        ###print('Numero letra ' + direccion[posicion])
        estado9(direccion, posicion + 1)
        # SALTO DE 28-33
    elif direccion[posicion] == '-' and direccion[posicion - 3:posicion] != 'BIS':
        aceptacion = False
        ###print('SALTO A ESTADO  9 - SIN BIS')
        estado12(direccion, posicion)
    else:
        return False


def estado9(direccion, posicion):
    global mensaje
    global aceptacion
    expresion_numeros = re.compile("[0-9]")
    if len(direccion) < posicion + 1:
        aceptacion = aceptacion
        ###print('1 ESTADO 9 TAMAÑO')
        mensaje += '1'
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ' or direccion[posicion] == '-':
        ###print(direccion[posicion] + ' Repetir estado 9 espacio 0 -')
        estado9(direccion, posicion + 1)
    elif direccion[posicion:posicion + 3] == 'BIS' and direccion[posicion:posicion + 4] != '-':
        aceptacion =False
        ###print('BIS PLACA COMPLEMENTO')
        estado11(direccion, posicion + 3)
    elif direccion[posicion:posicion + 3] == 'BIS' and direccion[posicion:posicion + 4] == '-':
        ###print('BIS SIN COMPLEMENTO')
        estado12(direccion, posicion + 3)
    elif direccion[posicion] in string.ascii_uppercase and expresion_numeros.match(direccion[posicion - 1]) and \
            direccion[posicion + 1] in string.ascii_uppercase == False:
        mensaje += '0'
        ###print('NUMERO LETRA')
        estado10(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion - 1]) and direccion[
        posicion] in string.ascii_uppercase and expresion_numeros.match(direccion[posicion + 2]):
        mensaje += '1'
        ###print('DOBLE NUMERO DE PLACA # ' + direccion[posicion])
        estado10(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion - 1]) and direccion[posicion] in string.ascii_uppercase:
        mensaje += '1'
        ###print('1 LETRA DESPUES DE NUMERO DE # ' + direccion[posicion])
        estado10(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion]):
        ###print('NUMERO ESTADO 9 ' + direccion[posicion])
        mensaje += '0'
        estado9(direccion, posicion + 1)
    elif direccion[posicion] in string.ascii_uppercase and expresion_numeros.match(direccion[posicion - 1]) and \
            direccion[posicion + 1] in string.ascii_uppercase:
        mensaje += '1'
        ###print('1 ESTADO 9 TAMAÑO NUMERO LETRA LETRA --NO APLICA--')
        estado10(direccion, posicion + 1)
    else:

        estado10(direccion, posicion)


def estado10(direccion, posicion):
    if direccion[posicion] == ' ':
        estado10(direccion, posicion + 1)
    else:
        estado11(direccion, posicion + 1)


def estado11(direccion, posicion):
    expresion_numeros = re.compile("[0-9]")
    ###print(direccion[posicion] + ' e11')
    global mensaje

    if len(direccion) <= posicion + 1:
        ###print('1 ESTADO 11 TAMAÑO')
        mensaje += '1'
        estadoFinal(direccion, posicion)

    elif direccion[posicion] == ' ' or direccion[posicion] == '-':
        estado11(direccion, posicion + 1)
    elif direccion[posicion] in string.ascii_uppercase and expresion_numeros.match(
            direccion[posicion + 1]) and expresion_numeros.match(direccion[posicion + 2]) and expresion_numeros.match(
            direccion[posicion + 3]) and direccion[posicion + 4] in string.ascii_uppercase:
        ###print('BIS LETRA TRIPLE NUMERO LETRA')
        mensaje += '0'
        estado12(direccion, posicion + 5)
    elif direccion[posicion] in string.ascii_uppercase and expresion_numeros.match(
            direccion[posicion + 1]) and expresion_numeros.match(direccion[posicion + 2]) and expresion_numeros.match(
        direccion[posicion + 3]):
        ###print('BIS LETRA TRIPLE NUMERO')
        mensaje += '0'
        estado12(direccion, posicion + 4)
    elif direccion[posicion] in string.ascii_uppercase and expresion_numeros.match(
            direccion[posicion + 1]) and expresion_numeros.match(direccion[posicion + 2]):
        ###print('BIS LETRA DOBLE NUMERO')
        mensaje += '0'
        estado12(direccion, posicion + 3)
    elif direccion[posicion] in string.ascii_uppercase and direccion[posicion + 1] in string.ascii_uppercase:
        ###print('BIS DOBLE LETRA')
        mensaje += '0'
        estado12(direccion, posicion + 2)


    elif direccion[posicion] in string.ascii_uppercase:
        ###print('BIS LETRA')
        mensaje += '0'
        estado12(direccion, posicion + 1)

    elif direccion[posicion] in string.ascii_uppercase and direccion[posicion + 1] in string.ascii_uppercase and \
            direccion[posicion + 2] in string.ascii_uppercase:
        ###print('1 ESTADO 11 TRIPLE LETRA DOBLE BIS')
        mensaje += '1'
        estado12(direccion, posicion + 3)
    elif direccion[posicion] in string.ascii_uppercase and direccion[
        posicion + 1] in string.ascii_uppercase and expresion_numeros.match(direccion[posicion + 2]):
        ###print('1 ESTADO 11 DOBLE LETRA BIS 2 CON NUMEROS --NO SIRVE--')
        mensaje += '1'
        estado12(direccion, posicion + 2)
    elif expresion_numeros.match(direccion[posicion]):
        mensaje += '0'
        estado12(direccion, posicion+1)
    else:
        ###print('1 ESTADO 11 ELSE DIRECTO')

        mensaje += '1'
        estado12(direccion, posicion + 1)


def estado12(direccion, posicion):
    expresion_numeros = re.compile("[0-9]")
    global mensaje
    global aceptacion
    if len(direccion) < posicion + 1:
        ###print('1 ESTADO 12 TAMAÑO ¿PUEDE FINALIZAR LA CADENA EN ESTE MOMENTO?')
        ###print(aceptacion)
        aceptacion = aceptacion
        mensaje += '0'
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ':
        estado12(direccion, posicion + 1)
    elif direccion[posicion:posicion + 5] == 'NORTE' or direccion[posicion:posicion + 4] == 'ESTE' or direccion[
                                                                                                      posicion:posicion + 5] == 'OESTE' or direccion[
                                                                                                                                           posicion:posicion + 3] == 'SUR':
        if direccion[posicion:posicion + 5] == 'NORTE':
            ###print('NORTE')
            mensaje += '0'
            estado13(direccion, posicion + 5)
        elif direccion[posicion:posicion + 4] == 'ESTE':
            ###print('ESTE')
            mensaje += '0'
            estado13(direccion, posicion + 4)
        elif direccion[posicion:posicion + 5] == 'OESTE':
            ###print('OESTE')
            mensaje += '0'
            estado13(direccion, posicion + 5)
        elif direccion[posicion:posicion + 3] == 'SUR':
            ###print('SUR 4')
            mensaje += '0'
            estado13(direccion, posicion + 3)
    elif direccion[posicion:posicion + 6] == 'NUMERO':
        ###print('VARIABLE NUMERO')
        mensaje += '0'
        estado13(direccion, posicion + 6)
    elif direccion[posicion:posicion + 3] == 'NO.' or direccion[posicion:posicion + 3] == 'NRO' or direccion[
                                                                                                   posicion:posicion + 3] == 'NUM':
        mensaje += '0'
        ###print('VARIABLES NO. O NUM O NRO')
        estado13(direccion, posicion + 3)
    elif direccion[posicion:posicion + 2] == 'NO' or direccion[posicion:posicion + 2] == 'N°' or direccion[
                                                                                                 posicion:posicion + 2] == 'N.':
        mensaje += '0'
        ###print('VARIABLES NO-N°-N.')
        estado13(direccion, posicion + 2)
    elif direccion[posicion] == 'N' or direccion[posicion] == '#' or direccion[posicion] == '-':
        mensaje += '0'
        ###print('VARIABLES # O N')
        aceptacion = False

        estado12(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion]) or (
            expresion_numeros.match(direccion[posicion - 1]) and direccion[posicion] in string.ascii_uppercase):
        mensaje += '0'
        ###print('NUMERO ' + direccion[posicion])
        aceptacion = True
        estado12(direccion, posicion + 1)
        if direccion[posicion] == ' ':
            estado12(direccion, posicion + 1)
    elif direccion[posicion] == ' ' and expresion_numeros.match(direccion[posicion + 1]):
        ###print('Espacio numero')
        mensaje += '0'
        estado12(direccion, posicion + 1)

    elif direccion[posicion] == ' ' and direccion[posicion + 1] in string.ascii_uppercase or direccion[posicion ] in string.ascii_uppercase:
        ###print('Complementos')

        estado14(direccion, posicion + 1)
    else:
        ###print('1 ESTADO 12 ELSE')
        ###print(direccion[posicion] + ' aaa')
        mensaje += '1'
        estado13(direccion, posicion + 1)


def estado13(direccion, posicion):
    global mensaje
    expresion_numeros = re.compile("[0-9]")
    if len(direccion) == posicion:
        mensaje += '0'
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == ' ':
        mensaje += '0'
        estado13(direccion, posicion + 1)
    elif direccion[posicion] == '-':
        mensaje += '0'
        estado13(direccion, posicion + 1)
    elif expresion_numeros.match(direccion[posicion]):
        mensaje += '0'
        estado14(direccion, posicion)
    elif direccion[posicion] in string.ascii_uppercase:
        mensaje += '0'
        estado14(direccion, posicion)
    else:
        mensaje += '1'
        ###print('1 ELSE DIRECTO ESTADO 14 ')
        estado14(direccion, posicion)


# COMPLEMENTO
def estado14(direccion, posicion):
    expresion_numeros = re.compile("[0-9]")
    global mensaje
    global aceptacion

    if len(direccion) <= posicion + 1:
        ###print('1 ESTADO 12 TAMAÑO ¿PUEDE FINALIZAR LA CADENA EN ESTE MOMENTO? COM')
        mensaje += '1'
        aceptacion = aceptacion
        estadoFinal(direccion, posicion)
    elif direccion[posicion] == '-' or direccion[posicion] == ' ':
        mensaje += '0'
        aceptacion = True
        estado14(direccion, posicion + 1)
    elif direccion[posicion] in string.ascii_uppercase or expresion_numeros.match(direccion[posicion]):
        mensaje += '0'
        aceptacion = True
        estado14(direccion, posicion + 1)

def estadoFinal(direccion, posicion):
    global aceptacion
    if (mensaje[len(mensaje) - 1] == '1' and aceptacion != False and mensaje.count('1') == 1 and mensaje.count(
            '2') == 0) or (aceptacion != False and mensaje[len(mensaje) - 1] == '0' and mensaje.count('1') == 0):
        #print('--- ' + direccion + ' TRUE' + ' --- MENSAJE --- ' + mensaje)
        aceptacion = True
    elif mensaje.count('1') > 1 or aceptacion == False or mensaje[len(mensaje) - 1] != '1' or mensaje.count('2')>=1:
        ##print('--- ' + direccion + ' FALSE '+ ' ---MENSAJE--- ' + mensaje)
        aceptacion = False



def isAddress(direccion):
    global mensaje
    direccionmayuscula = direccion.upper()
    global aceptacion
    global simbolo
    mensaje =''
    ##reemplazo = direccionmayuscula.replace('  ', ' ')
    reemplazo = direccionmayuscula.replace('N°', '#')
    aceptacion = True
    simbolo = False
    if 'AVENIDA CALLE' or 'AVENIDA CARRERA' or 'AVENIDA KARRERA' or 'AVENIDA CARRERA' or 'AV CARRERA' or 'AV CALLE' or 'DIAGONAL CRA' or 'DIAGONAL CARRERA' or 'DG CRA' or 'DIAGONAL CALLE' or 'DIAGONAL CL' in reemplazo:
        if 'AVENIDA CALLE' in reemplazo:
            reemplazo = direccionmayuscula.replace('AVENIDA CALLE', 'AC')
        elif 'AV. CALLE' in reemplazo:
            reemplazo = direccionmayuscula.replace('AV CALLE', 'AC')

        elif 'AVENIDA KARRERA' in reemplazo:
            reemplazo = direccionmayuscula.replace('AVENIDA KARRERA', 'AK')
        elif 'AVENIDA KARRERA' in reemplazo:
            reemplazo = direccionmayuscula.replace('AV CARRERA', 'AK')
        elif 'AVENIDA CARRERA' in reemplazo:
            reemplazo = direccionmayuscula.replace('AVENIDA CARRERA', 'AK')
        elif 'DIAGONAL CRA' or 'DIAGONAL CARRERA' or 'DG CRA' in reemplazo:
            if 'DIAGONAL CRA'in reemplazo:
                reemplazo = direccionmayuscula.replace('DIAGONAL CRA', 'DK')
            elif 'DIAGONAL CARRERA' in reemplazo:
                reemplazo = direccionmayuscula.replace('DIAGONAL CARRERA', 'DK')
            elif 'DG CRA' in reemplazo:
                reemplazo = direccionmayuscula.replace('DG CRA', 'DK')
        elif 'DIAGONAL CALLE' or 'DIAGONAL CL' in reemplazo:
            if 'DIAGONAL CALLE' in reemplazo:
                reemplazo = direccionmayuscula.replace('DIAGONAL CALLE', 'DC')
            elif 'DIAGONAL CL' in reemplazo:
                reemplazo = direccionmayuscula.replace('DIAGONAL CL', 'DC')
    else:
        reemplazo = direccionmayuscula
    for i in tipoVias:
        if reemplazo.count(i) > 1:
            mensaje += '2'
            estadoFinal(reemplazo, 0)
        elif reemplazo.startswith(i, 0, len(i)):
            estadoInicial(reemplazo, len(i))
            break
    else:
        for j in tipoViasRurales:
            if reemplazo.count(j)>1:
                mensaje += '2'
                estadoFinal(direccion, 0)
            elif reemplazo.startswith(j, 0, len(j)):

                estadoInicialRural(reemplazo, len(j))
                break

        else:
            return False
    return aceptacion

if __name__ == '__main__':
    #isAddress('VEREDA EL MONTILLO cl SIATAME 43 PROPIEDAD PINZON')
    #print(str(aceptacion))
    direcciones = stdin.read().split('\n')
    for i in direcciones:
        print(isAddress(i))