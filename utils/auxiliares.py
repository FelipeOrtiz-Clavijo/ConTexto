import os
import pickle
import re
import time
import win32com.client

######### Definición de funciones para buscar en el texto  #########
def buscar_en_texto(texto, lista=[]):
    return any(i in texto for i in lista)


def esta_en_texto(texto, lista=[], lista_2=[]):
    isin = False
    cuenta = 0
    for string in lista:
        if all(i in texto for i in string.split('|')):
            if string not in lista_2:
                return True
            else:
                cuenta += 1
                if cuenta > 1:
                    return True
    return isin

# Función para verificar si un directorio existe o no.
# Si el directorio no existe, lo crea
def verificar_crear_dir(ubicacion_directorio):
    if not os.path.exists(ubicacion_directorio):
        os.makedirs(ubicacion_directorio)


# Función para pasar de texto enriquecido a texto plano
def striprtf(text):
    """
    Extract text in RTF Files. Refactored to use with Python 3.x
    Source:
        http://stackoverflow.com/a/188877
    Code created by Markus Jarderot: http://mizardx.blogspot.com
    """
    pattern = re.compile(
        r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)",
        re.I)
   # control words which specify a "destionation".
    destinations = frozenset((
        'aftncn', 'aftnsep', 'aftnsepc', 'annotation', 'atnauthor', 'atndate', 'atnicn', 'atnid',
        'atnparent', 'atnref', 'atntime', 'atrfend', 'atrfstart', 'author', 'background',
        'bkmkend', 'bkmkstart', 'blipuid', 'buptim', 'category', 'colorschememapping',
        'colortbl', 'comment', 'company', 'creatim', 'datafield', 'datastore', 'defchp', 'defpap',
        'do', 'doccomm', 'docvar', 'dptxbxtext', 'ebcend', 'ebcstart', 'factoidname', 'falt',
        'fchars', 'ffdeftext', 'ffentrymcr', 'ffexitmcr', 'ffformat', 'ffhelptext', 'ffl',
        'ffname', 'ffstattext', 'field', 'file', 'filetbl', 'fldinst', 'fldrslt', 'fldtype',
        'fname', 'fontemb', 'fontfile', 'fonttbl', 'footer', 'footerf', 'footerl', 'footerr',
        'footnote', 'formfield', 'ftncn', 'ftnsep', 'ftnsepc', 'g', 'generator', 'gridtbl',
        'header', 'headerf', 'headerl', 'headerr', 'hl', 'hlfr', 'hlinkbase', 'hlloc', 'hlsrc',
        'hsv', 'htmltag', 'info', 'keycode', 'keywords', 'latentstyles', 'lchars', 'levelnumbers',
        'leveltext', 'lfolevel', 'linkval', 'list', 'listlevel', 'listname', 'listoverride',
        'listoverridetable', 'listpicture', 'liststylename', 'listtable', 'listtext',
        'lsdlockedexcept', 'macc', 'maccPr', 'mailmerge', 'maln', 'malnScr', 'manager', 'margPr',
        'mbar', 'mbarPr', 'mbaseJc', 'mbegChr', 'mborderBox', 'mborderBoxPr', 'mbox', 'mboxPr',
        'mchr', 'mcount', 'mctrlPr', 'md', 'mdeg', 'mdegHide', 'mden', 'mdiff', 'mdPr', 'me',
        'mendChr', 'meqArr', 'meqArrPr', 'mf', 'mfName', 'mfPr', 'mfunc', 'mfuncPr', 'mgroupChr',
        'mgroupChrPr', 'mgrow', 'mhideBot', 'mhideLeft', 'mhideRight', 'mhideTop', 'mhtmltag',
        'mlim', 'mlimloc', 'mlimlow', 'mlimlowPr', 'mlimupp', 'mlimuppPr', 'mm', 'mmaddfieldname',
        'mmath', 'mmathPict', 'mmathPr', 'mmaxdist', 'mmc', 'mmcJc', 'mmconnectstr',
        'mmconnectstrdata', 'mmcPr', 'mmcs', 'mmdatasource', 'mmheadersource', 'mmmailsubject',
        'mmodso', 'mmodsofilter', 'mmodsofldmpdata', 'mmodsomappedname', 'mmodsoname',
        'mmodsorecipdata', 'mmodsosort', 'mmodsosrc', 'mmodsotable', 'mmodsoudl',
        'mmodsoudldata', 'mmodsouniquetag', 'mmPr', 'mmquery', 'mmr', 'mnary', 'mnaryPr',
        'mnoBreak', 'mnum', 'mobjDist', 'moMath', 'moMathPara', 'moMathParaPr', 'mopEmu',
        'mphant', 'mphantPr', 'mplcHide', 'mpos', 'mr', 'mrad', 'mradPr', 'mrPr', 'msepChr',
        'mshow', 'mshp', 'msPre', 'msPrePr', 'msSub', 'msSubPr', 'msSubSup', 'msSubSupPr', 'msSup',
        'msSupPr', 'mstrikeBLTR', 'mstrikeH', 'mstrikeTLBR', 'mstrikeV', 'msub', 'msubHide',
        'msup', 'msupHide', 'mtransp', 'mtype', 'mvertJc', 'mvfmf', 'mvfml', 'mvtof', 'mvtol',
        'mzeroAsc', 'mzeroDesc', 'mzeroWid', 'nesttableprops', 'nextfile', 'nonesttables',
        'objalias', 'objclass', 'objdata', 'object', 'objname', 'objsect', 'objtime', 'oldcprops',
        'oldpprops', 'oldsprops', 'oldtprops', 'oleclsid', 'operator', 'panose', 'password',
        'passwordhash', 'pgp', 'pgptbl', 'picprop', 'pict', 'pn', 'pnseclvl', 'pntext', 'pntxta',
        'pntxtb', 'printim', 'private', 'propname', 'protend', 'protstart', 'protusertbl', 'pxe',
        'result', 'revtbl', 'revtim', 'rsidtbl', 'rxe', 'shp', 'shpgrp', 'shpinst',
        'shppict', 'shprslt', 'shptxt', 'sn', 'sp', 'staticval', 'stylesheet', 'subject', 'sv',
        'svb', 'tc', 'template', 'themedata', 'title', 'txe', 'ud', 'upr', 'userprops',
        'wgrffmtfilter', 'windowcaption', 'writereservation', 'writereservhash', 'xe', 'xform',
        'xmlattrname', 'xmlattrvalue', 'xmlclose', 'xmlname', 'xmlnstbl',
        'xmlopen',
    ))
    # Translation of some special characters.
    specialchars = {
        'par': '\n',
        'sect': '\n\n',
        'page': '\n\n',
        'line': '\n',
        'tab': '\t',
        'emdash': '\u2014',
        'endash': '\u2013',
        'emspace': '\u2003',
        'enspace': '\u2002',
        'qmspace': '\u2005',
        'bullet': '\u2022',
        'lquote': '\u2018',
        'rquote': '\u2019',
        'ldblquote': '\201C',
        'rdblquote': '\u201D',
    }
    stack = []
    # Whether this group (and all inside it) are "ignorable".
    ignorable = False
    # Number of ASCII characters to skip after a unicode character.
    ucskip = 1
    curskip = 0             # Number of ASCII characters left to skip
    out = []                # Output buffer.
    #    for match in pattern.finditer(text.decode()):
    for match in pattern.finditer(text):
        word, arg, hex, char, brace, tchar = match.groups()
        if brace:
            curskip = 0
            if brace == '{':
                # Push state
                stack.append((ucskip, ignorable))
            elif brace == '}':
                # Pop state
                try:
                    ucskip, ignorable = stack.pop()
                except BaseException:
                    pass
        elif char:  # \x (not a letter)
            curskip = 0
            if char == '~':
                if not ignorable:
                    out.append('\xA0')
            elif char in '{}\\':
                if not ignorable:
                    out.append(char)
            elif char == '*':
                ignorable = True
        elif word:  # \foo
            curskip = 0
            if word in destinations:
                ignorable = True
            elif ignorable:
                pass
            elif word in specialchars:
                out.append(specialchars[word])
            elif word == 'uc':
                ucskip = int(arg)
            elif word == 'u':
                c = int(arg)
                if c < 0:
                    c += 0x10000
                if c > 127:
                    out.append(chr(c))  # NOQA
                else:
                    out.append(chr(c))
                curskip = ucskip
        elif hex:  # \'xx
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                c = int(hex, 16)
                if c > 127:
                    out.append(chr(c))  # NOQA
                else:
                    out.append(chr(c))
        elif tchar:
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                out.append(tchar)
    return ''.join(out)

# Función para convertir un archivo word a pdf
def word_a_pdf(archivo_entrada, archivo_salida):
    wdFormatPDF = 17
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = True
    time.sleep(3)
    doc = word.Documents.Open(archivo_entrada)
    doc.SaveAs(archivo_salida, FileFormat=wdFormatPDF)
    doc.Close()
    return


######### Definición de funciones para guardar y cargar objetos Python  #########

def guardar_objeto(objeto, nombre_archivo):
    with open(nombre_archivo, 'wb') as handle:
        pickle.dump(objeto, handle, protocol=pickle.HIGHEST_PROTOCOL)

def cargar_objeto(nombre_archivo):
    with open(nombre_archivo, 'rb') as handle:
        objeto = pickle.load(handle)
    return objeto