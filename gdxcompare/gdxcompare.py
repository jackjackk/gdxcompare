# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 14:24:21 2012

@author: Marangoni
"""
from __future__ import print_function

import importlib
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

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('gdxcompare')
logger.debug('Logger created')


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def add_to_dompool(new_sorted_elemlist, dompool):
    i = -1
    for i,elemlist in enumerate(dompool):
        n = len(elemlist)
        is_new_list_in_elemlist = True
        for e in new_sorted_elemlist:
            try:
                candidate_idx = np.searchsorted(elemlist,e)
            except:
                candidate_idx = -1
            if (candidate_idx == n) or (e != elemlist[candidate_idx]):
                is_new_list_in_elemlist = False
                break
        if is_new_list_in_elemlist:
            return i
    dompool.append(new_sorted_elemlist)
    return i+1


colors_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
styles_list = ["null", "Dygraph.DASHED_LINE", "[2, 2]", "Dygraph.DOT_DASH_LINE", "null", "Dygraph.DASHED_LINE", "[2, 2]", "Dygraph.DOT_DASH_LINE"]
points_list = ["false", "false", "false", "false", "true", "true", "true", "true", ]

import pandas as pd
import json


def assignStylesAndColorsToSeries(labels, i_style_field=None, delimiter='_'):
    dreplace = {}
    x = pd.DataFrame([u.replace('/','_').split(delimiter) for u in labels]).T.drop_duplicates().T
    idx4color = list(range(x.shape[1]))
    dfdict = {}
    strings2unquote = []
    if i_style_field is not None:
        sstyle = x.iloc[:,i_style_field]
        words_list = sstyle.unique()
        dfdict['strokePattern'] = (sstyle + '_sp').values
        dreplace.update(dict(zip(words_list + '_sp', styles_list)))
        dfdict['drawPoints'] = (sstyle + '_dp').values
        dreplace.update(dict(zip(words_list + '_dp', points_list)))
        idx4color.pop(i_style_field)
        strings2unquote = list(set(styles_list)) + list(set(points_list))
    scolor = x.iloc[:, idx4color].apply(lambda u: delimiter.join(u), axis=1)
    dfdict['color'] = scolor.values
    dreplace.update(dict(zip(scolor.unique(), colors_list)))
    df = pd.DataFrame(dfdict, index=labels)
    js2write = json.dumps(df.replace(dreplace).T.to_dict())
    for s in strings2unquote:
        js2write = js2write.replace(f'"{s}"', s)
    return js2write


def main():
    usage = "usage: %prog [options] gdx1 gdx2 ..."
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-e','--style', action='store', type='int', dest='style_field', default = None, help='Field number identifying the line style, after splitting name by _')
    parser.add_option('-m','--xmax', action='store', type='int', dest='xmax', default = 0, help='Max value for x-axis [0 = no max]')
    parser.add_option('-f','--xmin', action='store', type='int', dest='xmin', default = 0, help='Min value for x-axis [0 = no min]')
    parser.add_option('-y','--ymax', action='store', type='int', dest='ymax', default = 0, help='Max value for y-axis [0 = no min]')
    parser.add_option('-r','--rename', action='store', type='string', dest='rename_string', default = '', help='Comma-separated list of new names to give to gdx')
    #parser.add_option('-s','--symb', action='store', type='string', dest='symb_regex', default = '^[A-Z_]+$', help='Name of the set used as x-axis')
    parser.add_option('-s','--symb', action='store', type='string', dest='symb_regex', default = '', help='Regex to filter names of the symbols to plot')
    parser.add_option('-p','--profile', action='store', type='string', dest='prof', default = '', help='Name of file under profiles subdir with predefined symbol regex to use (w/o ".py")')
    parser.add_option('-x','--xlambda', action='store', type='string', dest='xlambda', default = '', help='Lambda function applied to each element of the x-axis')
    parser.add_option('-w','--witch', action="store_true", dest="bwitch", default=False, help='Flag to get some WITCH-related flags')
    parser.add_option('-d','--disaggsymb', action="store_true", dest="disaggsymb", default=False, help='Flag to disaggregate large symbols across elements of the first domain')
    parser.add_option('-t','--twosymb', action='store', type='string', dest='twosymb_regex', default = '', help='Regex to filter names of the symbols to plot')

    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(0)

    if options.bwitch and (options.xlambda == ''):
        options.xlambda = '2005+5*(x-1)'


    comparePath = os.path.dirname(os.path.realpath(__file__)) #os.path.abspath(os.path.split(sys.argv[0])[0])
    filt_dict = None
    filt = None
    class dummy_symb_regex: pass
    if options.prof != '':
        try:
            prof_module = importlib.import_module(f'gdxcompare.profiles.{options.prof}')
        except:
            prof_module = importlib.import_module(f'profiles.{options.prof}')
        filt_dict = prof_module.filt_dict
        options.symb_regex = f'^{"|".join(filt_dict.keys())}$'
    if options.symb_regex.startswith('@'):
        symb_regex = dummy_symb_regex()
        symb_regex.match = lambda x : eval(options.symb_regex[1:])
    else:
        symb_regex = re.compile(options.symb_regex) #,re.IGNORECASE)

    if options.twosymb_regex != '':
        options.disaggsymb = True
    twosymb_regex = re.compile(options.twosymb_regex)

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

    with open(os.path.join(comparePath,'data.js'), 'w') as fout:
        y_range = 'null'
        if options.ymax != 0:
            y_range = f'[0, {options.ymax}]'
        fout.write(f'var yRange = {y_range};\n')
        fout.write('var symbList = [\n')
        lastnamePlaceholder = 'z'*10
        symb2gdxlist_dict = {}
        symb2desc_dict = {}
        ngdx = len(gdxList)
        grange = list(range(ngdx))
        for ig,gpath in enumerate(gdxList):
            g = GdxFile(gpath)
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
        for s,realgdxlist in symb2gdxlist_dict.items():
            if len(realgdxlist) < 2:
                continue
            try:
                try:
                    filt = filt_dict[s]
                except:
                    pass
                svar = gload(s,[gdxList[ig] for ig in realgdxlist],clear=True,filt=filt,single=False,remove_underscore=False,returnfirst=True)
            except AssertionError as e:
                message = e.args[0]
                logger.info(message)
                continue
            except Exception as e:
                traceback.print_exc()
                #if s.name == 'Q_EN':
                #    bDone = True
                logger.info('Skipping {}'.format(s))
                continue
            symb2data_dict = {}
            if options.disaggsymb:
                for domfirst_entry in svar.index.levels[1].values:
                    snew = '{}|{}'.format(s,domfirst_entry)
                    symb2data_dict[snew] = svar.xs(domfirst_entry, axis=0, level=1)
                    symb2desc_dict[snew] = symb2desc_dict[s] + ' ({})'.format(domfirst_entry)
            else:
                symb2data_dict[s] = svar

            for s, svar in symb2data_dict.items():
                if not twosymb_regex.match(s):
                    continue
                try:
                    df = svar.unstack(0)
                    domlist = []
                    try:
                        df.axes[0].levels
                    except:
                        df = pd.concat({' ':df})  # workaround for menuHandler.js
                    levels_list = df.axes[0].levels
                    ilev2values = lambda df, iax: df.index.get_level_values(iax).unique()
                    nx = len(levels_list)
                    for iax in reversed(list(range(len(levels_list)))):
                        ax = ilev2values(df, iax)
                        tfound = True
                        for x in ax:
                            try:
                                int(x)
                            except:
                                tfound = False
                                break
                        if tfound == True:
                            axsnotime = list(range(nx))
                            axsnotime.pop(iax)
                            newaxslist = axsnotime+[iax,]
                            #df = df.reorder_levels(axsnotime+[iax,]).sort()
                            #if iax < nx-1:
                            #    df = df.swaplevel(iax,nx-1).unstack().stack() #.sortlevel(nx-1)
                            logger.info('found time at iax = {}'.format(iax))
                            break
                    if not tfound:
                        logger.info('Skipping {} (no x-axis found)'.format(s))
                        continue
                    #df2 = df.copy()
                    #df.index = pd.MultiIndex.from_product([range(len(item)) for item in df.axes[0].levels])
                    # For each row of data, of index x, build a new index where (x_i) is
                    sorted_levels_values = []
                    for i in list(range(nx)):
                        sorted_values = np.sort(ilev2values(df,i))
                        if i==iax:
                            sorted_values = sorted_values[(sorted_values>xaxisMin) & (sorted_values<xaxisMax)]
                        domlist.append(add_to_dompool(sorted_values, dompool))
                    #df.index = pd.MultiIndex.from_tuples([tuple([np.searchsorted(sorted_levels_values[i],x[i]) for i in range(nx)]) for x in df.index])
                    data = {}
                    for k,v in df.T.iteritems():
                        if nx == 1:
                            k = [k]
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
                        data[','.join(['%d' % np.searchsorted(dompool[domlist[i]],k[i]) for i in newaxslist])] = [float('%.2e' % x) if x != 0.0 else 'null' for x in list(val2write)]
                    if domcounter>0:
                        fout.write(',\n')
                    fout.write('new Symb("%s","%s",%s,%s)' % (s, symb2desc_dict[s].replace('"',"'"), str([domlist[i] for i in newaxslist]), str(data).replace("'null'",'null')))
                    domcounter += nx
                except AssertionError as e:
                    message = e.args[0]
                    logger.info(message)
                except Exception as e:
                    traceback.print_exc()
                    #if s.name == 'Q_EN':
                    #    bDone = True
                    logger.info('Skipping {}'.format(s))

        fout.write('];\n')
        fout.write('var setList = [\n')
        for idom,d in enumerate(dompool):
            if idom > 0:
                fout.write(',\n')
            if isinstance(d[-1], np.int64):
                dlist = list(d)
                drange = list(range(1,int(d[-1])+1))
                if (options.xlambda != '') and (dlist == drange):
                    d = [eval(options.xlambda) for x in d]
            fout.write('new Set("s%d",%s)' % (idom,str([x if x != '' else '(none)' for x in d])))
        fout.write('];\n')

        labels = [g.split('\\')[-1] for g in gdxNames]
        fout.write('var series = %s;' % str(labels))
        fout.write(f'var seriesOptions = {assignStylesAndColorsToSeries(labels, options.style_field)};')

    open_file(os.path.join(comparePath,'compare.html'))


if __name__ == '__main__':
    main()
