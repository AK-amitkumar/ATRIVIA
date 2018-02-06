# -*- coding: utf-8 -*-


to_19_ar = ( 'صفر',  'واحد',   'اثنان',  'ثلاثة', 'أربعة',   'خمسة',   'ستة',
          'سبعة', 'ثمانية', 'تسعة', 'عشرة',   'أحد عشر', 'اثني عشر', 'ثلاثة عشر',
          'أربعة عشرة', 'خمسة عشر', 'السادس عشر', 'سبعة عشر', 'ثمانية عشرة', 'تسعة عشر' )

tens_ar  = ( 'عشرون', 'ثلاثون', 'أربعين', 'خمسون', 'ستون', 'سبعون', 'ثمانون', 'تسعين')

denom_ar = ( '',
          'ألف',   'مليون',   'مليار',   'تريليون',   'كوادريليون',
          'كينتيليون',   'سكستيليون',   'سيبتيليون',   'أوكتيليون',   'نونيليون',
          'ديكليون',    'وندسيليون',   'دوديسيليون',   'تريديسيليون',   'كواتورديسيليون',
          'سيكسديسيليون',   'سبتمبر',   'أوكتوديسيليون',   'نوفيمدسيليون',   'فيجينتيليون' )

def _convert_nn_ar(val):
    """ convert a value < 100 to arabic
    """
    if val < 20:
        return to_19_ar[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_ar)):
        if dval + 10 > val:
            if val % 10:
                if dval == 70 or dval == 90:
                    return tens_ar[dval / 10 - 3] + '-' + to_19_ar[val % 10 + 10]
                else:
                    return dcap + '-' + to_19_ar[val % 10]
            return dcap

def _convert_nnn_ar(val):
    """ convert a value < 1000 to arabic
    
        special cased because it is the level that kicks 
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        if rem == 1:
            word = 'مئة واحد'
        else:
            word = to_19_ar[rem] + 'مئة'
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn_ar(mod)
    return word

def arabic_number(val):
    if val < 100:
        return _convert_nn_ar(val)
    if val < 1000:
        return _convert_nnn_ar(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_ar))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            if l == 1:
                ret = 'واحد' + denom_ar[didx] 
            else:
                ret = _convert_nnn_ar(l) + ' ' + denom_ar[didx]
            if r > 0:
                ret = ret + ', ' + arabic_number(r)
            return ret

def amount_to_text_ar(number, currency):
    number = '%.2f' % number
    units_name = currency
    list = str(number).split('.')
    start_word = arabic_number(abs(int(list[0])))
    end_word = arabic_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and ' سنتا' or ' سنتا'
    final_result = start_word + ' ' + units_name + ' ' + end_word + ' ' + cents_name
    return final_result