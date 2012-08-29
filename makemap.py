import os
import sys
import time
import ordat.cta
import svgcuts

stns = ordat.cta.Station.all
points = [st.loc for st in stns]
minlat = min([lat for (lat, lon) in points])
minlon = min([lon for (lat, lon) in points])
maxlat = max([lat for (lat, lon) in points])
maxlon = max([lon for (lat, lon) in points])
lats = maxlat - minlat
lons = maxlon - minlon
aspect = lons / lats

#print 'aspect ratio: ' aspect

width = 8.0 # inches?
height = width / aspect
lonmul = width / lons
latmul = height / lats
station_sz = width / 150.0
train_sz = width / 180.0

def mapping(lat, lon) :
	# ha ha mercator
	x = lonmul * (lon - minlon)
	y = latmul * (maxlat - lat)
	return x,y

def draw_indicator(lat, lon, layer, sz, **kwargs) :
	x, y = mapping(lat, lon)
	_sz = sz / 2.0
	p1 = svgcuts.Point(x + _sz, y + _sz)
	p2 = svgcuts.Point(x + _sz, y - _sz)
	p3 = svgcuts.Point(x - _sz, y - _sz)
	p4 = svgcuts.Point(x - _sz, y + _sz)
	layer.add_line(svgcuts.Line(p1, p2, unit="in", **kwargs))
	layer.add_line(svgcuts.Line(p2, p3, unit="in", **kwargs))
	layer.add_line(svgcuts.Line(p3, p4, unit="in", **kwargs))
	layer.add_line(svgcuts.Line(p4, p1, unit="in", **kwargs))

svgfn = sys.argv[1]
key = sys.argv[2]
train = ordat.cta.Train(key=key)
tracker = ordat.cta.panopticon.Tracker()

while True :
	layer = svgcuts.Layer(width, height, unit="in")
	for lat, lon in points :
		draw_indicator(lat, lon, layer, station_sz, color='white')
	for rn, line, lat, lon in tracker.step() :
		draw_indicator(lat, lon, layer, train_sz, color='#%s' % line.hexcolor)
	layer.write(svgfn + '.incomplete')
	if os.path.exists(svgfn) :
		os.unlink(svgfn)
	os.rename(svgfn + '.incomplete', svgfn)
	print time.ctime(), ' wrote updated map'
	time.sleep(6.0)
