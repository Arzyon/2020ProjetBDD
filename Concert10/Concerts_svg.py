#!/usr/bin/env python
# encoding: utf-8
# Généré par Mocodo 2.3.7 le Thu, 22 Oct 2020 02:54:06

from __future__ import division
from math import hypot

import time, codecs

import json

with codecs.open('Concerts_geo.json') as f:
    geo = json.loads(f.read())
(width,height) = geo.pop('size')
for (name, l) in geo.items(): globals()[name] = dict(l)
card_max_width = 22
card_max_height = 15
card_margin = 5
arrow_width = 12
arrow_half_height = 6
arrow_axis = 8
card_baseline = 3

def cmp(x, y):
    return (x > y) - (x < y)

def offset(x, y):
    return (x + card_margin, y - card_baseline - card_margin)

def line_intersection(ex, ey, w, h, ax, ay):
    if ax == ex:
        return (ax, ey + cmp(ay, ey) * h)
    if ay == ey:
        return (ex + cmp(ax, ex) * w, ay)
    x = ex + cmp(ax, ex) * w
    y = ey + (ay-ey) * (x-ex) / (ax-ex)
    if abs(y-ey) > h:
        y = ey + cmp(ay, ey) * h
        x = ex + (ax-ex) * (y-ey) / (ay-ey)
    return (x, y)

def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch):
    
    def card_pos(twist, shift):
        compare = (lambda x1_y1: x1_y1[0] < x1_y1[1]) if twist else (lambda x1_y1: x1_y1[0] <= x1_y1[1])
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (xg, yg) = line_intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = line_intersection(ex, ey, ew + cw, eh, ax, ay)
        if compare((xg, xb)):
            if compare((xg, ex)):
                if compare((yb, ey)):
                    return (xb - correction, yb)
                return (xb - correction, yb + ch)
            if compare((yb, ey)):
                return (xg, yg + ch - correction)
            return (xg, yg + correction)
        if compare((xb, ex)):
            if compare((yb, ey)):
                return (xg - cw, yg + ch - correction)
            return (xg - cw, yg + correction)
        if compare((yb, ey)):
            return (xb - cw + correction, yb)
        return (xb - cw + correction, yb + ch)
    
    def arrow_pos(direction, ratio):
        (x0, y0) = line_intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = line_intersection(ax, ay, aw, ah, ex, ey)
        if direction == "<":
            (x0, y0, x1, y1) = (x1, y1, x0, y0)
        (x, y) = (ratio * x0 + (1 - ratio) * x1, ratio * y0 + (1 - ratio) * y1)
        return (x, y, x1 - x0, y0 - y1)
    
    straight_leg_factory.card_pos = card_pos
    straight_leg_factory.arrow_pos = arrow_pos
    return straight_leg_factory


def curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, spin):
    
    def bisection(predicate):
        (a, b) = (0, 1)
        while abs(b - a) > 0.0001:
            m = (a + b) / 2
            if predicate(bezier(m)):
                a = m
            else:
                b = m
        return m
    
    def intersection(left, top, right, bottom):
       (x, y) = bezier(bisection(lambda p: left <= p[0] <= right and top <= p[1] <= bottom))
       return (int(round(x)), int(round(y)))
    
    def card_pos(shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal)
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin > 0:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction + shift, bot + ch)
            if (xr == RIG and yr >= top) or yr == BOT:
                return (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) + correction + shift)
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) + correction + shift - cw, TOP + ch)
            return (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction + shift + ch)
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) + correction + shift - cw, bot + ch)
        if xr == RIG or (yr == TOP and xr >= rig):
            return (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction + shift + ch)
        if yr == TOP or (xr == LEF and yr <= top):
            return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction + shift, TOP + ch)
        return (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) + correction + shift)
    
    def arrow_pos(direction, ratio):
        t0 = bisection(lambda p: abs(p[0] - ax) > aw or abs(p[1] - ay) > ah)
        t3 = bisection(lambda p: abs(p[0] - ex) < ew and abs(p[1] - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * ratio
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)
    
    diagonal = hypot(ax - ex, ay - ey)
    (x, y) = line_intersection(ex, ey, ew + cw / 2, eh + ch / 2, ax, ay)
    k = (cw *  abs((ay - ey) / diagonal) + ch * abs((ax - ex) / diagonal))
    (x, y) = (x - spin * k * (ay - ey) / diagonal, y + spin * k * (ax - ex) / diagonal)
    (hx, hy) = (2 * x - (ex + ax) / 2, 2 * y - (ey + ay) / 2)
    (x1, y1) = (ex + (hx - ex) * 2 / 3, ey + (hy - ey) * 2 / 3)
    (x2, y2) = (ax + (hx - ax) * 2 / 3, ay + (hy - ay) * 2 / 3)
    (kax, kay) = (ex - 2 * hx + ax, ey - 2 * hy + ay)
    (kbx, kby) = (2 * hx - 2 * ex, 2 * hy - 2 * ey)
    bezier = lambda t: (kax*t*t + kbx*t + ex, kay*t*t + kby*t + ey)
    derivate = lambda t: (2*kax*t + kbx, 2*kay*t + kby)
    
    curved_leg_factory.points = (ex, ey, x1, y1, x2, y2, ax, ay)
    curved_leg_factory.card_pos = card_pos
    curved_leg_factory.arrow_pos = arrow_pos
    return curved_leg_factory


def upper_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w - r, y, "a", r, r, 90, 0, 1, r, r, "V", y + h, "h", -w, "V", y + r, "a", r, r, 90, 0, 1, r, -r]])

def lower_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w, y, "v", h - r, "a", r, r, 90, 0, 1, -r, r, "H", x + r, "a", r, r, 90, 0, 1, -r, -r, "V", y, "H", w]])

def arrow(x, y, a, b):
    c = hypot(a, b)
    (cos, sin) = (a / c, b / c)
    return " ".join([str(x) for x in [ "M", x, y, "L", x + arrow_width * cos - arrow_half_height * sin, y - arrow_half_height * cos - arrow_width * sin, "L", x + arrow_axis * cos, y - arrow_axis * sin, "L", x + arrow_width * cos + arrow_half_height * sin, y + arrow_half_height * cos - arrow_width * sin, "Z"]])

def safe_print_for_PHP(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf8"))


lines = '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
lines += '\n\n<svg width="%s" height="%s" view_box="0 0 %s %s"\nxmlns="http://www.w3.org/2000/svg"\nxmlns:link="http://www.w3.org/1999/xlink">' % (width,height,width,height)
lines += u'\\n\\n<desc>Généré par Mocodo 2.3.7 le %s</desc>' % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
lines += '\n\n<rect id="frame" x="0" y="0" width="%s" height="%s" fill="%s" stroke="none" stroke-width="0"/>' % (width,height,colors['background_color'] if colors['background_color'] else "none")

lines += u"""\n\n<!-- Association se dérouler -->"""
(x,y) = (cx[u"se dérouler"],cy[u"se dérouler"])
(ex,ey) = (cx[u"concert"],cy[u"concert"])
leg=straight_leg_factory(ex,ey,39,59,x,y,42,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(True,shift[u"se dérouler,concert"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"lieu"],cy[u"lieu"])
leg=straight_leg_factory(ex,ey,33,76,x,y,42,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"se dérouler,lieu"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-se dérouler">""" % {}
path = upper_round_rect(-42+x,-25+y,84,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-42+x,0.0+y,84,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="84" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -42+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -42+x, 'y0': 0+y, 'x1': 42+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">se dérouler</text>""" % {'x': -35+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association bénéficier de -->"""
(x,y) = (cx[u"bénéficier de"],cy[u"bénéficier de"])
(ex,ey) = (cx[u"concert"],cy[u"concert"])
leg=straight_leg_factory(ex,ey,39,59,x,y,47,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"bénéficier de,concert"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"entracte"],cy[u"entracte"])
leg=straight_leg_factory(ex,ey,40,34,x,y,47,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"bénéficier de,entracte"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-bénéficier de">""" % {}
path = upper_round_rect(-47+x,-25+y,94,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-47+x,0.0+y,94,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="94" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -47+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -47+x, 'y0': 0+y, 'x1': 47+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">bénéficier de</text>""" % {'x': -40+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association comporter(ticket) -->"""
(x,y) = (cx[u"comporter(ticket)"],cy[u"comporter(ticket)"])
(ex,ey) = (cx[u"lieu"],cy[u"lieu"])
leg=curved_leg_factory(ex,ey,33,76,x,y,69,25,22+2*card_margin,15+2*card_margin,-0.75)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"comporter(ticket),lieu"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"catégorie"],cy[u"catégorie"])
leg=straight_leg_factory(ex,ey,43,42,x,y,69,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"comporter(ticket),catégorie"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-comporter(ticket)">""" % {}
path = upper_round_rect(-69+x,-25+y,138,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-69+x,0.0+y,138,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="138" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -69+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -69+x, 'y0': 0+y, 'x1': 69+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">comporter(ticket)</text>""" % {'x': -54+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">prix_final(selon cas)</text>""" % {'x': -62+x, 'y': 17.8+y, 'text_color': colors['association_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association possède -->"""
(x,y) = (cx[u"possède"],cy[u"possède"])
(ex,ey) = (cx[u"lieu"],cy[u"lieu"])
leg=straight_leg_factory(ex,ey,33,76,x,y,32,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"possède,lieu"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"place"],cy[u"place"])
leg=straight_leg_factory(ex,ey,103,34,x,y,32,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"possède,place"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-possède">""" % {}
path = upper_round_rect(-32+x,-25+y,64,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-32+x,0.0+y,64,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="64" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -32+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -32+x, 'y0': 0+y, 'x1': 32+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">possède</text>""" % {'x': -25+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association appartenir -->"""
(x,y) = (cx[u"appartenir"],cy[u"appartenir"])
(ex,ey) = (cx[u"catégorie"],cy[u"catégorie"])
leg=straight_leg_factory(ex,ey,43,42,x,y,39,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"appartenir,catégorie"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"place"],cy[u"place"])
leg=straight_leg_factory(ex,ey,103,34,x,y,39,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"appartenir,place"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-appartenir">""" % {}
path = upper_round_rect(-39+x,-25+y,78,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-39+x,0.0+y,78,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="78" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -39+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -39+x, 'y0': 0+y, 'x1': 39+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">appartenir</text>""" % {'x': -32+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association souslieu -->"""
(x,y) = (cx[u"souslieu"],cy[u"souslieu"])
(ex,ey) = (cx[u"lieu"],cy[u"lieu"])
leg=curved_leg_factory(ex,ey,33,76,x,y,32,25,21+2*card_margin,15+2*card_margin,-1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"souslieu,lieu,-1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"lieu"],cy[u"lieu"])
leg=curved_leg_factory(ex,ey,33,76,x,y,32,25,22+2*card_margin,15+2*card_margin,1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"souslieu,lieu,1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12" onmouseover="show(evt,'lieu')" onmouseout="hide(evt)" style="cursor: pointer;">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
path=arrow(*leg.arrow_pos(">",ratio[u"souslieu,lieu,1.0"]))
lines += u"""\n<path d="%(path)s" fill="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'stroke_color': colors['leg_stroke_color']}
lines += u"""\n<g id="association-souslieu">""" % {}
path = upper_round_rect(-32+x,-25+y,64,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-32+x,0.0+y,64,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="64" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -32+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -32+x, 'y0': 0+y, 'x1': 32+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">souslieu</text>""" % {'x': -25+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_lieu</text>""" % {'x': -25+x, 'y': 17.8+y, 'text_color': colors['association_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association référencé -->"""
(x,y) = (cx[u"référencé"],cy[u"référencé"])
(ex,ey) = (cx[u"salle"],cy[u"salle"])
leg=straight_leg_factory(ex,ey,60,59,x,y,36,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"référencé,salle"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"lieu"],cy[u"lieu"])
leg=straight_leg_factory(ex,ey,33,76,x,y,36,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(True,shift[u"référencé,lieu"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-référencé">""" % {}
path = upper_round_rect(-36+x,-25+y,72,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-36+x,0.0+y,72,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="72" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -36+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -36+x, 'y0': 0+y, 'x1': 36+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">référencé</text>""" % {'x': -29+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association correspond -->"""
(x,y) = (cx[u"correspond"],cy[u"correspond"])
(ex,ey) = (cx[u"concert"],cy[u"concert"])
leg=straight_leg_factory(ex,ey,39,59,x,y,41,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"correspond,concert"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"affiche"],cy[u"affiche"])
leg=straight_leg_factory(ex,ey,35,59,x,y,41,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"correspond,affiche"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-correspond">""" % {}
path = upper_round_rect(-41+x,-25+y,82,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-41+x,0.0+y,82,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="82" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -41+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -41+x, 'y0': 0+y, 'x1': 41+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">correspond</text>""" % {'x': -34+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association interpréteur principal -->"""
(x,y) = (cx[u"interpréteur principal"],cy[u"interpréteur principal"])
(ex,ey) = (cx[u"morceau"],cy[u"morceau"])
leg=straight_leg_factory(ex,ey,41,51,x,y,72,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"interpréteur principal,morceau"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"interprète"],cy[u"interprète"])
leg=straight_leg_factory(ex,ey,45,93,x,y,72,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"interpréteur principal,interprète"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-interpréteur principal">""" % {}
path = upper_round_rect(-72+x,-25+y,144,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-72+x,0.0+y,144,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="144" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -72+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -72+x, 'y0': 0+y, 'x1': 72+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">interpréteur principal</text>""" % {'x': -65+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association secondaire -->"""
(x,y) = (cx[u"secondaire"],cy[u"secondaire"])
(ex,ey) = (cx[u"interprète"],cy[u"interprète"])
leg=straight_leg_factory(ex,ey,45,93,x,y,40,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"secondaire,interprète"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"spécialité"],cy[u"spécialité"])
leg=straight_leg_factory(ex,ey,54,42,x,y,40,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"secondaire,spécialité"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-secondaire">""" % {}
path = upper_round_rect(-40+x,-25+y,80,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-40+x,0.0+y,80,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="80" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -40+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -40+x, 'y0': 0+y, 'x1': 40+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">secondaire</text>""" % {'x': -33+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association travailleur -->"""
(x,y) = (cx[u"travailleur"],cy[u"travailleur"])
(ex,ey) = (cx[u"personne"],cy[u"personne"])
leg=straight_leg_factory(ex,ey,43,59,x,y,38,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"travailleur,personne"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"salle"],cy[u"salle"])
leg=straight_leg_factory(ex,ey,60,59,x,y,38,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"travailleur,salle"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-travailleur">""" % {}
path = upper_round_rect(-38+x,-25+y,76,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-38+x,0.0+y,76,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="76" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -38+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -38+x, 'y0': 0+y, 'x1': 38+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">travailleur</text>""" % {'x': -31+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association enregistrer -->"""
(x,y) = (cx[u"enregistrer"],cy[u"enregistrer"])
(ex,ey) = (cx[u"concert"],cy[u"concert"])
leg=straight_leg_factory(ex,ey,39,59,x,y,41,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"enregistrer,concert"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"disque"],cy[u"disque"])
leg=straight_leg_factory(ex,ey,41,42,x,y,41,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"enregistrer,disque"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-enregistrer">""" % {}
path = upper_round_rect(-41+x,-25+y,82,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-41+x,0.0+y,82,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="82" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -41+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -41+x, 'y0': 0+y, 'x1': 41+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">enregistrer</text>""" % {'x': -34+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association disposer -->"""
(x,y) = (cx[u"disposer"],cy[u"disposer"])
(ex,ey) = (cx[u"concert"],cy[u"concert"])
leg=straight_leg_factory(ex,ey,39,59,x,y,33,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"disposer,concert"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"bande_promo"],cy[u"bande_promo"])
leg=straight_leg_factory(ex,ey,57,59,x,y,33,25,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"disposer,bande_promo"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-disposer">""" % {}
path = upper_round_rect(-33+x,-25+y,66,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-33+x,0.0+y,66,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="66" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -33+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -33+x, 'y0': 0+y, 'x1': 33+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">disposer</text>""" % {'x': -26+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association programme -->"""
(x,y) = (cx[u"programme"],cy[u"programme"])
(ex,ey) = (cx[u"morceau"],cy[u"morceau"])
leg=straight_leg_factory(ex,ey,41,51,x,y,55,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"programme,morceau"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"concert"],cy[u"concert"])
leg=straight_leg_factory(ex,ey,39,59,x,y,55,25,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(True,shift[u"programme,concert"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-programme">""" % {}
path = upper_round_rect(-55+x,-25+y,110,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-55+x,0.0+y,110,25,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="110" height="50" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -55+x, 'y': -25+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -55+x, 'y0': 0+y, 'x1': 55+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">programme</text>""" % {'x': -36+x, 'y': -7.3+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">ordre (position)</text>""" % {'x': -48+x, 'y': 17.8+y, 'text_color': colors['association_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity salle -->"""
(x,y) = (cx[u"salle"],cy[u"salle"])
lines += u"""\n<g id="entity-salle">""" % {}
lines += u"""\n	<g id="frame-salle">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="120" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -60+x, 'y': -59+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="120" height="93" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -60+x, 'y': -34.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="120" height="118" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -60+x, 'y': -59+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -60+x, 'y0': -34+y, 'x1': 60+x, 'y1': -34+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">salle</text>""" % {'x': -14+x, 'y': -41.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">nom(varchar(42))</text>""" % {'x': -55+x, 'y': -16.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -55+x, 'y0': -14+y, 'x1': 55+x, 'y1': -14+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">adr</text>""" % {'x': -55+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">directeur</text>""" % {'x': -55+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">charge_com</text>""" % {'x': -55+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">chef_regi</text>""" % {'x': -55+x, 'y': 51.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity bande_promo -->"""
(x,y) = (cx[u"bande_promo"],cy[u"bande_promo"])
lines += u"""\n<g id="entity-bande_promo">""" % {}
lines += u"""\n	<g id="frame-bande_promo">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="114" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -57+x, 'y': -59+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="114" height="93" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -57+x, 'y': -34.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="114" height="118" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -57+x, 'y': -59+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -57+x, 'y0': -34+y, 'x1': 57+x, 'y1': -34+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">bande_promo</text>""" % {'x': -42+x, 'y': -41.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_bande_promo</text>""" % {'x': -52+x, 'y': -16.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -52+x, 'y0': -14+y, 'x1': 51+x, 'y1': -14+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">taille (en ko)</text>""" % {'x': -52+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">format</text>""" % {'x': -52+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">mots clés</text>""" % {'x': -52+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">durée</text>""" % {'x': -52+x, 'y': 51.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity concert -->"""
(x,y) = (cx[u"concert"],cy[u"concert"])
lines += u"""\n<g id="entity-concert">""" % {}
lines += u"""\n	<g id="frame-concert">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="78" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -39+x, 'y': -59+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="78" height="93" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -39+x, 'y': -34.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="78" height="118" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -39+x, 'y': -59+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -39+x, 'y0': -34+y, 'x1': 39+x, 'y1': -34+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">concert</text>""" % {'x': -23+x, 'y': -41.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_concert</text>""" % {'x': -34+x, 'y': -16.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -34+x, 'y0': -14+y, 'x1': 30+x, 'y1': -14+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">date</text>""" % {'x': -34+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">heure</text>""" % {'x': -34+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">salle_spect</text>""" % {'x': -34+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">theme</text>""" % {'x': -34+x, 'y': 51.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity entracte -->"""
(x,y) = (cx[u"entracte"],cy[u"entracte"])
lines += u"""\n<g id="entity-entracte">""" % {}
lines += u"""\n	<g id="frame-entracte">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="80" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -40+x, 'y': -34+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="80" height="43" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -40+x, 'y': -9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="80" height="68" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -40+x, 'y': -34+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -40+x, 'y0': -9+y, 'x1': 40+x, 'y1': -9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">entracte</text>""" % {'x': -26+x, 'y': -16.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_entracte</text>""" % {'x': -35+x, 'y': 8.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -35+x, 'y0': 11+y, 'x1': 34+x, 'y1': 11+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">situe</text>""" % {'x': -35+x, 'y': 25.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity affiche -->"""
(x,y) = (cx[u"affiche"],cy[u"affiche"])
lines += u"""\n<g id="entity-affiche">""" % {}
lines += u"""\n	<g id="frame-affiche">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="70" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -35+x, 'y': -59+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="70" height="93" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -35+x, 'y': -34.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="70" height="118" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -35+x, 'y': -59+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -35+x, 'y0': -34+y, 'x1': 35+x, 'y1': -34+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">affiche</text>""" % {'x': -21+x, 'y': -41.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_affiche</text>""" % {'x': -30+x, 'y': -16.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -30+x, 'y0': -14+y, 'x1': 29+x, 'y1': -14+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">img_imp</text>""" % {'x': -30+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">img_web</text>""" % {'x': -30+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">colori</text>""" % {'x': -30+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">prof_coul</text>""" % {'x': -30+x, 'y': 51.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity lieu -->"""
(x,y) = (cx[u"lieu"],cy[u"lieu"])
lines += u"""\n<g id="entity-lieu">""" % {}
lines += u"""\n	<g id="frame-lieu">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="66" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -33+x, 'y': -76+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="66" height="127" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -33+x, 'y': -51.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="66" height="152" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -33+x, 'y': -76+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -33+x, 'y0': -51+y, 'x1': 33+x, 'y1': -51+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">lieu</text>""" % {'x': -11+x, 'y': -58.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_lieu</text>""" % {'x': -28+x, 'y': -33.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -28+x, 'y0': -31+y, 'x1': 13+x, 'y1': -31+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">nom</text>""" % {'x': -28+x, 'y': -16.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">adr</text>""" % {'x': -28+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">localité</text>""" % {'x': -28+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">dep</text>""" % {'x': -28+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">soustype</text>""" % {'x': -28+x, 'y': 51.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity personne -->"""
(x,y) = (cx[u"personne"],cy[u"personne"])
lines += u"""\n<g id="entity-personne">""" % {}
lines += u"""\n	<g id="frame-personne">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -43+x, 'y': -59+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="93" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -43+x, 'y': -34.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="118" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -43+x, 'y': -59+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -43+x, 'y0': -34+y, 'x1': 43+x, 'y1': -34+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">personne</text>""" % {'x': -29+x, 'y': -41.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_personne</text>""" % {'x': -38+x, 'y': -16.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -38+x, 'y0': -14+y, 'x1': 37+x, 'y1': -14+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">nom</text>""" % {'x': -38+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">prénom</text>""" % {'x': -38+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">tél</text>""" % {'x': -38+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">email</text>""" % {'x': -38+x, 'y': 51.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity disque -->"""
(x,y) = (cx[u"disque"],cy[u"disque"])
lines += u"""\n<g id="entity-disque">""" % {}
lines += u"""\n	<g id="frame-disque">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -41+x, 'y': -42+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="59" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -41+x, 'y': -17.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="84" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -41+x, 'y': -42+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -41+x, 'y0': -17+y, 'x1': 41+x, 'y1': -17+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">disque</text>""" % {'x': -20+x, 'y': -24.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_disque</text>""" % {'x': -36+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -36+x, 'y0': 3+y, 'x1': 23+x, 'y1': 3+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">nom</text>""" % {'x': -36+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">prix_disque</text>""" % {'x': -36+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity catégorie -->"""
(x,y) = (cx[u"catégorie"],cy[u"catégorie"])
lines += u"""\n<g id="entity-catégorie">""" % {}
lines += u"""\n	<g id="frame-catégorie">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -43+x, 'y': -42+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="59" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -43+x, 'y': -17.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="84" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -43+x, 'y': -42+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -43+x, 'y0': -17+y, 'x1': 43+x, 'y1': -17+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">catégorie</text>""" % {'x': -29+x, 'y': -24.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_catégorie</text>""" % {'x': -38+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -38+x, 'y0': 3+y, 'x1': 37+x, 'y1': 3+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">nom</text>""" % {'x': -38+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">prix_ref</text>""" % {'x': -38+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity spécialité -->"""
(x,y) = (cx[u"spécialité"],cy[u"spécialité"])
lines += u"""\n<g id="entity-spécialité">""" % {}
lines += u"""\n	<g id="frame-spécialité">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="108" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -54+x, 'y': -42+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="108" height="59" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -54+x, 'y': -17.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="108" height="84" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -54+x, 'y': -42+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -54+x, 'y0': -17+y, 'x1': 54+x, 'y1': -17+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">spécialité</text>""" % {'x': -29+x, 'y': -24.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_spécialité</text>""" % {'x': -49+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -49+x, 'y0': 3+y, 'x1': 27+x, 'y1': 3+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">nom (ex: violon</text>""" % {'x': -49+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">harpe)</text>""" % {'x': -49+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity place -->"""
(x,y) = (cx[u"place"],cy[u"place"])
lines += u"""\n<g id="entity-place">""" % {}
lines += u"""\n	<g id="frame-place">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="206" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -103+x, 'y': -34+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="206" height="43" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -103+x, 'y': -9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="206" height="68" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -103+x, 'y': -34+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -103+x, 'y0': -9+y, 'x1': 103+x, 'y1': -9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">place</text>""" % {'x': -16+x, 'y': -16.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_place</text>""" % {'x': -98+x, 'y': 8.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -98+x, 'y0': 11+y, 'x1': -47+x, 'y1': 11+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">XXXstatut(vendu/réservé FNAC)</text>""" % {'x': -98+x, 'y': 25.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity morceau -->"""
(x,y) = (cx[u"morceau"],cy[u"morceau"])
lines += u"""\n<g id="entity-morceau">""" % {}
lines += u"""\n	<g id="frame-morceau">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -41+x, 'y': -51+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="77" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -41+x, 'y': -26.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="102" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -41+x, 'y': -51+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -41+x, 'y0': -26+y, 'x1': 41+x, 'y1': -26+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">morceau</text>""" % {'x': -27+x, 'y': -33.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_morceau</text>""" % {'x': -36+x, 'y': -8.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -36+x, 'y0': -6+y, 'x1': 36+x, 'y1': -6+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">auteur</text>""" % {'x': -36+x, 'y': 8.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">titre</text>""" % {'x': -36+x, 'y': 25.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">durée</text>""" % {'x': -36+x, 'y': 42.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity interprète -->"""
(x,y) = (cx[u"interprète"],cy[u"interprète"])
lines += u"""\n<g id="entity-interprète">""" % {}
lines += u"""\n	<g id="frame-interprète">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="25" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -45+x, 'y': -93+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="161" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -45+x, 'y': -68.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="186" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="2"/>""" % {'x': -45+x, 'y': -93+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -45+x, 'y0': -68+y, 'x1': 45+x, 'y1': -68+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">interprète</text>""" % {'x': -31+x, 'y': -75.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">id_interprète</text>""" % {'x': -40+x, 'y': -50.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -40+x, 'y0': -48+y, 'x1': 39+x, 'y1': -48+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">nom</text>""" % {'x': -40+x, 'y': -33.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">prénom</text>""" % {'x': -40+x, 'y': -16.3+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">tel</text>""" % {'x': -40+x, 'y': 0.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">email</text>""" % {'x': -40+x, 'y': 17.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">naiss</text>""" % {'x': -40+x, 'y': 34.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">nat</text>""" % {'x': -40+x, 'y': 51.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">resu_bio</text>""" % {'x': -40+x, 'y': 68.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Verdana" font-size="12">spe_ppal</text>""" % {'x': -40+x, 'y': 85.8+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}
annotation_overlay_height = 40
annotation_baseline = 24
annotation_font = {u'family': u'Verdana', u'size': 14}
annotation_text_color = "#f7f7f7"
annotation_color = "#b35806"
annotation_opacity = 0.9

lines += '\n\n<!-- Annotations -->'
lines += '\n<script type="text/ecmascript">'
lines += '\n<![CDATA['
lines += '\n	function show(evt, text) {'
lines += '\n		var pos = (evt.target.getAttribute("y") < %s) ? "bottom" : "top"' % (height - annotation_overlay_height - card_margin)
lines += '\n		var annotation = document.getElementById(pos + "_annotation_EA5bXBfp")'
lines += '\n		annotation.textContent = text'
lines += '\n		annotation.setAttributeNS(null, "visibility", "visible");'
lines += '\n		document.getElementById(pos + "_overlay_EA5bXBfp").setAttributeNS(null, "visibility", "visible");'
lines += '\n	}'
lines += '\n	function hide(evt) {'
lines += '\n		document.getElementById("top_annotation_EA5bXBfp").setAttributeNS(null, "visibility", "hidden");'
lines += '\n		document.getElementById("top_overlay_EA5bXBfp").setAttributeNS(null, "visibility", "hidden");'
lines += '\n		document.getElementById("bottom_annotation_EA5bXBfp").setAttributeNS(null, "visibility", "hidden");'
lines += '\n		document.getElementById("bottom_overlay_EA5bXBfp").setAttributeNS(null, "visibility", "hidden");'
lines += '\n	}'
lines += '\n]]>'
lines += '\n</script>'
lines += '\n<rect id="top_overlay_EA5bXBfp" x="0" y="0" width="%s" height="%s" fill="%s" stroke-width="0" opacity="%s" visibility="hidden"/>' % (width, annotation_overlay_height, annotation_color, annotation_opacity)
lines += '\n<text id="top_annotation_EA5bXBfp" text-anchor="middle" x="%s" y="%s" fill="%s" font-family="%s" font-size="%s" visibility="hidden"></text>' % (width/2, annotation_baseline, annotation_text_color, annotation_font['family'], annotation_font['size'])
lines += '\n<rect id="bottom_overlay_EA5bXBfp" x="0" y="%s" width="%s" height="%s" fill="%s" stroke-width="0" opacity="%s" visibility="hidden"/>' % (height-annotation_overlay_height, width, annotation_overlay_height, annotation_color, annotation_opacity)
lines += '\n<text id="bottom_annotation_EA5bXBfp" text-anchor="middle" x="%s" y="%s" fill="%s" font-family="%s" font-size="%s" visibility="hidden"></text>' % (width/2, height-annotation_overlay_height+annotation_baseline, annotation_text_color, annotation_font['family'], annotation_font['size'])
lines += u'\n</svg>'

with codecs.open("Concerts.svg", "w", "utf8") as f:
    f.write(lines)
safe_print_for_PHP(u'Fichier de sortie "Concerts.svg" généré avec succès.')