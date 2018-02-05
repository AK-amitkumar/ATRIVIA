# -*- coding: utf-8 -*-

    
to_19_de = ('Null', 'Eins', 'Zwei',  'Drei', 'Vier',   u'Fünf',   'Sechs',
          'Sieben', 'Acht', 'Neun', 'Zehn',   'Elf', u'Zwölf', 'Dreizehn',
          'Vierzehn', u'Fünfzehn', 'Sechzehn', 'Siebzehn', 'Achtzehn', 'Neunzehn' )
tens_de = ( 'Zwanzig', u'Dreiβig', 'Vierzig', u'Fünfzig', 'Sechzig', 'Siebzig', 'Achtzig', 'Neunzig')
denom_de = ('',
          'Tausend',     'Million',         'Milliarde',       'Billion',       'Quadrillion',
          'Trillion',  'Sextillion',      'Septillion',    'Octillion',      'Nonillion',
          'Decillion',    'Undecillion',     'Duodecillion',  'Tredecillion',   'Quattuordecillion',
          'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion' )

def _convert_nn_de(val):
    """ convert a value < 100 to French
    """
    if val < 20:
        return to_19_de[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_de)):
        if dval + 10 > val:
            if val % 10:
                if dval == 70 or dval == 90:
                    return tens_de[dval / 10 - 3] + '-' + to_19_de[val % 10 + 10]
                else:
                    return dcap + '-' + to_19_de[val % 10]
            return dcap

def _convert_nnn_de(val):
    """ convert a value < 1000 to french
    
        special cased because it is the level that kicks 
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        if rem == 1:
            word = 'Eins Hundert'
        else:
            word = to_19_de[rem] + ' Hundert'
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn_de(mod)
    return word

def duch_number(val):
    if val < 100:
        return _convert_nn_de(val)
    if val < 1000:
        return _convert_nnn_de(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_de))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            if l == 1:
                ret = 'Eins' + denom_de[didx]
            else:
                ret = _convert_nnn_de(l) + ' ' + denom_de[didx]
            if r > 0:
                ret = ret + ', ' + duch_number(r)
            return ret

def amount_to_text_de(number, currency):
    number = '%.2f' % number
    units_name = currency
    list = str(number).split('.')
    start_word = duch_number(abs(int(list[0])))
    end_word = duch_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and ' Zentimeter' or ' Rappen'
    final_result = start_word + ' ' + units_name + ' ' + end_word + ' ' + cents_name
    return final_result