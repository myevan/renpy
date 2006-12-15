#!/usr/bin/python

import os
import re
import sys
import time

import inspect

sys.path.append('..')
sys.path.append('../module')

import renpy
renpy.import_all()

keywords = [
    r'\bimage\b',
    r'\bscene\b',
    r'\bshow\b',
    r'\bhide\b',
    r'\binit\b',
    r'\$',
    r'\blabel\b',
    r'\bmenu\b',
    r'\bset\b',
    r'\bif\b',
    r'\bwhile\b',
    r'\bjump\b',
    r'\blabel\b',
    r'\bcall\b',
    r'\breturn\b',
    r'\bfrom\b',
    r'\belif\b',
    r'\belse\b',
    r'\bpass\b',
    r'\bwith\b',
    r'\bat\b',
    r'\bpython\b',
    ]

kwre = '|'.join(keywords)

def example(m):
    s = m.group(1)
    rv = ""
    pos = 0

    while pos < len(s):

        m = re.compile(r'(?s)"(([^"]|\\.)*)"').match(s, pos)
        if m:
            rv += '"<span class="string">%s</span>"' % m.group(1)
            pos = m.end()
            continue

        m = re.compile(r"(?s)'(([^']|\\.)*)'").match(s, pos)
        if m:
            rv += '\'<span class="string">%s</span>\'' % m.group(1)
            pos = m.end()
            continue

        m = re.compile(r"(?s)(#[^\n]+)").match(s, pos)
        if m:
            rv += '<span class="comment">%s</span>' % m.group(1)
            pos = m.end()
            continue


        m = re.compile(kwre).match(s, pos)
        if m:
            rv += '<span class="keyword">%s</span>' % m.group(0)
            pos = m.end()
            continue


        rv += s[pos]
        pos += 1
        

    return "<example>" + rv + "</example>"

def function(m):

    name = m.group(1)
    print >>sys.stderr, name


    store = vars(renpy.store)
    renpy.store.renpy = renpy.exports

    func = eval(name, store)

    if isinstance(func, renpy.curry.Curry):
        if func.callable == renpy.curry.Curry:
            func = func.args[0]
        else:
            func = func.callable
    
    doc = func.__doc__

    if inspect.isclass(func):
        func = func.__init__
        if func.__doc__:
            doc += "\n" + func.__doc__

        a, b, c, d = inspect.getargspec(func)
        args = inspect.formatargspec(a[1:], b, c, d)
    else:
        args = inspect.formatargspec(*inspect.getargspec(func))
        
    args = re.sub(r"'\\x00\\x01.*?\\xff'", "im.ramp(0, 255)", args)
    args = args.replace("&", "&amp;")
    args = args.replace("<=>", "&lt;=&gt;")
    args = re.sub(r'<.*?>', '...', args)
    args = args.replace("<", "&lt;")
    args = args.replace("\"", "&quot;")

    docparas = []


    for p in re.split(r'\n\s*\n', doc):
        p = p.strip()
        p = re.sub(r"\@param (\w+):", r'<param>\1</param> -', p)
        p = "<p>" + p + "</p>"

        docparas.append(p)

    doc = '\n'.join(docparas)
    
    return '<function name="%(name)s" sig="%(args)s">%(doc)s</function>' % locals()

def include(m):

    f = file(m.group(1))
    rv = f.read()
    f.close()
    return rv
        
class ret_none(object):
    def __getattr__(self, k):
        return None
    

def main():

    f = file(sys.argv[1])
    s = f.read()
    f.close()

    os.chdir("..")


    try:
        renpy.game.options = ret_none()
        renpy.main.main("dump_styles")
    except "foo":
        pass

    os.chdir("doc")

    s = re.sub(r"<!-- func ?(\S+) ?-->", function, s)
    s = re.sub(r"<!-- include (\S+) -->", include, s)
    s = re.sub(r"<!-- date -->", time.strftime("%04Y-%02m-%02d %02H:%02M"), s)
    s = re.sub(r"(?s)<example>(.*?)</example>", example, s)

    print s

if __name__ == "__main__":
    main()