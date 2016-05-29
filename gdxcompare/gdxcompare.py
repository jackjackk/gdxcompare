#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 14:24:21 2012

@author: Marangoni
"""
import sys, os
from gdxpy import *
import numpy as np
import re
import traceback
#import sets as setsLib
import collections
import optparse
import pdb
import subprocess

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def add_to_doompol(new_sorted_elemlist):
    i = -1
    for i,elemlist in enumerate(dompool):
        n = len(elemlist)
        is_new_list_in_elemlist = True
        for e in new_sorted_elemlist:
            candidate_idx = np.searchsorted(elemlist,e)
            if (candidate_idx == n) or (e != elemlist[candidate_idx]):
                is_new_list_in_elemlist = False
                break
        if is_new_list_in_elemlist:
            return i
    dompool.append(new_sorted_elemlist)
    return i+1

usage = "usage: %prog [options] gdx1 gdx2 ..."
parser = optparse.OptionParser(usage=usage)
parser.add_option('-m','--xmax', action='store', type='int', dest='xmax', default = 0, help='Max value for x-axis [0 = no max]')
parser.add_option('-f','--xmin', action='store', type='int', dest='xmin', default = 0, help='Min value for x-axis [0 = no min]')
parser.add_option('-r','--rename', action='store', type='string', dest='rename_string', default = '', help='Comma-separated list of new names to give to gdx')
#parser.add_option('-s','--symb', action='store', type='string', dest='symb_regex', default = '^[A-Z_]+$', help='Name of the set used as x-axis')
parser.add_option('-s','--symb', action='store', type='string', dest='symb_regex', default = '', help='Regex to filter names of the symbols to plot')
parser.add_option('-p','--profile', action='store', type='string', dest='prof', default = '', help='Name of file under profiles subdir with predefined symbol regex to use (w/o ".py")')
(options, args) = parser.parse_args()

if len(args) == 0:
    parser.print_help()
    sys.exit(0)

comparePath = os.path.dirname(os.path.realpath(__file__)) #os.path.abspath(os.path.split(sys.argv[0])[0])
filt_dict = None
class dummy_symb_regex: pass
if options.symb_regex == '' and options.prof != '':
    with open (os.path.join(comparePath,'profiles','%s.py'%(options.prof)), "r") as fileprof:
        prof = eval(fileprof.read())
    if isinstance(prof,dict):
        options.symb_regex = '^({0})$'.format('|'.join(prof.keys()))
        filt_dict = prof
    else:
        options.symb_regex = prof
if options.symb_regex[0] == '@':
    symb_regex = dummy_symb_regex()
    symb_regex.match = lambda x : eval(options.symb_regex[1:])
else:
    symb_regex = re.compile(options.symb_regex) #,re.IGNORECASE)

xaxisMax = options.xmax
if xaxisMax==0:
    xaxisMax = np.inf
else:
    xaxisMax +=1
xaxisMin = options.xmin
if xaxisMin==0:
    xaxisMin = -np.inf
else:
    xaxisMin -=1
gdxList = args
gdxNames = []
if options.rename_string == '':
    for i,gname in enumerate(gdxList):
        gdxNames.append(gname[:-4])
else:
    gdxNames = options.rename_string.split(',')
    if len(gdxNames) != len(gdxList):
        raise Exception('Please provide a rename list with the same number of elements as the gdx')

fout = file(os.path.join(comparePath,'data.txt'),'w')
fout.write('var symbList = [\n')

lastnamePlaceholder = 'z'*10
symb2gdxlist_dict = {}
symb2desc_dict = {}
ngdx = len(gdxList)
grange = range(ngdx)
for ig,gpath in enumerate(gdxList):
    g = gdxfile(gpath)
    for s in g.get_symbols_list():
        if not symb_regex.match(s.name):
            continue
        try:
            symb2gdxlist_dict[s.name].append(ig)
        except:
            symb2gdxlist_dict[s.name] = [ig,]
            symb2desc_dict[s.name] = s.desc
domcounter = 0
bDone = False
dompool = []
for s,realgdxlist in symb2gdxlist_dict.iteritems():
    if len(realgdxlist) < 2:
        continue
    try:
        try:
            filt = filt_dict[s]
        except:
            filt = None
        svar = gload(s,[gdxList[ig] for ig in realgdxlist],reshape=False,clear=True,filt=filt,single=False,remove_underscore=False,returnfirst=True)
    except AssertionError as e:
        message = e.args[0]
        print message
        continue
    except Exception as e:
        traceback.print_exc()
        #if s.name == 'Q_EN':
        #    bDone = True
        print 'Skipping',s
        continue
    try:
        df = svar.stack().unstack(0)
        domlist = []
        try:
            nx = len(df.axes[0].levels)
        except:
            nx = 2
            df = pd.concat([df.stack()],keys=['only']).unstack(0)
        for iax,ax in reversed(list(enumerate(df.axes[0].levels))):
            tfound = True
            for x in ax:
                try:
                    int(x)
                except:
                    tfound = False
                    break
            if tfound == True:
                axsnotime = range(nx)
                axsnotime.pop(iax)
                newaxslist = axsnotime+[iax,]
                #df = df.reorder_levels(axsnotime+[iax,]).sort()
                #if iax < nx-1:
                #    df = df.swaplevel(iax,nx-1).unstack().stack() #.sortlevel(nx-1)
                print 'found time at iax =',iax
                break
        if not tfound:
            print 'Skipping',s,'(no x-axis found)'
            continue
        #df2 = df.copy()
        #df.index = pd.MultiIndex.from_product([range(len(item)) for item in df.axes[0].levels])
        # For each row of data, of index x, build a new index where (x_i) is
        sorted_levels_values = []
        for i in range(nx):
            sorted_values = np.sort(df.axes[0].levels[i].values)
            if i==iax:
                sorted_values = sorted_values[(sorted_values>xaxisMin) & (sorted_values<xaxisMax)]
            domlist.append(add_to_doompol(sorted_values))
        #df.index = pd.MultiIndex.from_tuples([tuple([np.searchsorted(sorted_levels_values[i],x[i]) for i in range(nx)]) for x in df.index])
        data = {}
        for k,v in df.T.iteritems():
            if ((xaxisMin != 0) and (k[iax] < xaxisMin)) or ((xaxisMax != np.inf) and (k[iax] > xaxisMax)):
                continue
            val2write = np.zeros(ngdx)
            #for i2read,i2write in enumerate(realgdxlist):
            #    y = v.values[i2read]
            #    if np.isnan(y) or (y > 1e200):
            #        y = 0.
            #    val2write[i2write] = y
            for ig,g in enumerate(gdxList):
                try:
                    y = v[g[:-4]]
                    if (not np.isnan(y)) and (y < 1e200):
                        val2write[ig] = y
                except:
                    pass
            data[','.join(['%d' % np.searchsorted(dompool[domlist[i]],k[i]) for i in newaxslist])] = [float('%.2e' % x) for x in list(val2write)]
        if domcounter>0:
            fout.write(',\n')
        fout.write('new Symb("%s","%s",%s,%s)' % (s, symb2desc_dict[s], str([domlist[i] for i in newaxslist]), str(data)))
        domcounter += nx
    except AssertionError as e:
        message = e.args[0]
        print message
    except Exception as e:
        traceback.print_exc()
        #if s.name == 'Q_EN':
        #    bDone = True
        print 'Skipping',s

fout.write('];\n')
fout.write('var setList = [\n')
for idom,d in enumerate(dompool):
    if idom > 0:
        fout.write(',\n')
    fout.write('new Set("s%d",%s)' % (idom,str(list(d))))
fout.write('];\n')


fout.write('var series = %s;' % str([g.split('\\')[-1] for g in gdxNames]))

fout.close()

open_file(os.path.join(comparePath,'compare.html'))
