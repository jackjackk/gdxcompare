_regs = '(world|r5.*)'
#_regs = '(world|r5.*|china|usa|europe|india)'


def regify(l):
    return ('('+('|'.join([x.replace('|',r'\|') for x in l]))+')$')


filt_dict = {
    'db': [
        [r'Investment\|Energy Demand', 'Transportation', '', '', _regs],
        ['Final Energy$', 'Transportation', '', '', _regs],
        ['Secondary Energy$', 'Hydrogen', '', '', _regs],
        ['Energy Service', 'Transportation', '', '', _regs],
        ['Emissions', 'CO2', 'Energy|Demand|Transportation', '', '', _regs],
        ['Price', '', '', '', _regs]]
}
