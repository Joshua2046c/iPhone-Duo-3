# cell: retainer
w=param('retainer_width',33.1)
h=param('retainer_height',78.6)
t=param('retainer_thickness',1.0)
relief=param('retainer_roof_relief',0.2)
end_land=param('retainer_end_bond_land',2.3)
side_land=param('retainer_side_bond_land',2.1)
rail_y=param('retainer_rail_relief_y',13.7)
# Centred full cover with asymmetrical shell outline and an open hinge-side rail relief.
skin=param('retainer_decor_skin',0.2)
corner_r=param('retainer_corner_radius',10.15)
left_r=param('retainer_left_corner_radius',0.6)
outline=RectangleRounded(w,h,corner_r)+Pos(-w/4,0)*Rectangle(w/2,h)
outline=fillet([v for v in outline.vertices() if abs(v.X+w/2)<1e-6],radius=left_r)
body=Pos(0,0,-skin)*extrude(outline,amount=t+skin)
cut_left=-w/2-1
cut_right=w/2-end_land
if relief>0:
 body -= Pos((cut_left+cut_right)/2,rail_y,t-relief/2+0.5)*Box(cut_right-cut_left,h-2*side_land,relief+1)


assert 0<=relief<t+skin
assert len(body.solids())==1
body.color=Color(0.80,0.015,0.055)
publish('retainer',body,'03 平整内盖板',material='petg')
