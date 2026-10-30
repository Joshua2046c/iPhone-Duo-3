# cell: spine
# One developed sheet, two endpoint poses. Not a continuous phone hinge simulation.
import math
h=param('spine_height',84.0)
t=param('spine_thickness',0.76)
tail_h=param('spine_sliding_tail_height',115.3)
assert 0<tail_h<=h
span=param('spine_bridge_span',11.9)
r=param('spine_bend_radius',1.6)
tail_l=param('spine_tail_length',30.0)
tab_l=param('spine_glue_tab_length',8.0)
slot_l=param('spine_slot_length',22.5)
slot_w=param('spine_slot_width',3.2)
slot_r=param('spine_slot_corner_radius',2.1)
assert 0<2*slot_r<min(slot_l,slot_w)
slot_profile=RectangleRounded(slot_l,slot_w,slot_r)
assert abs(slot_profile.area-(slot_l*slot_w-(4-math.pi)*slot_r**2))<1e-5
slot_x=param('spine_slot_center_from_bend',17.0)
slot_y1=param('spine_slot_y1',-25.0)
slot_y2=param('spine_slot_y2',25.0)
flat=param('spine_flat_pose',False)
free_l=span+math.pi*r
tip_r=param('spine_tail_corner_radius',3.0)
# Keep the existing flat underside and closed reference outside surface.
REFERENCE_THICKNESS=0.15
R=r+REFERENCE_THICKNESS/2
z0=-R
A=math.pi*r/2
end_s=free_l+tail_l
assert 0<t<R and abs(h-tail_h)<1e-6
def point(x,z):
 return (x,-h/2,z)
def lower_p(ss,rr):
 angle=ss/r
 return point(-rr*math.sin(angle),-rr*math.cos(angle))
def upper_p(angle,rr):
 return point(-rr*math.cos(angle),span+rr*math.sin(angle))
def make_sheet(flat_pose):
 if flat_pose:
  edges=[Line(point(tab_l,z0),point(-end_s,z0)),
         Line(point(-end_s,z0),point(-end_s,z0+t)),
         Line(point(-end_s,z0+t),point(tab_l,z0+t)),
         Line(point(tab_l,z0+t),point(tab_l,z0))]
 else:
  edges=[Line(point(tab_l,-R),point(0,-R)),
   ThreePointArc(lower_p(0,R),lower_p(A/2,R),lower_p(A,R)),
   Line(point(-R,0),point(-R,span)),
   ThreePointArc(upper_p(0,R),upper_p(math.pi/4,R),upper_p(math.pi/2,R)),
   Line(point(0,span+R),point(tail_l,span+R)),
   Line(point(tail_l,span+R),point(tail_l,span+R-t)),
   Line(point(tail_l,span+R-t),point(0,span+R-t)),
   ThreePointArc(upper_p(math.pi/2,R-t),upper_p(math.pi/4,R-t),upper_p(0,R-t)),
   Line(point(-R+t,span),point(-R+t,0)),
   ThreePointArc(lower_p(A,R-t),lower_p(A/2,R-t),lower_p(0,R-t)),
   Line(point(0,-R+t),point(tab_l,-R+t)),
   Line(point(tab_l,-R+t),point(tab_l,-R))]
 section=Face(Wire([edge for curve in edges for edge in curve.edges()]))
 sheet=extrude(section,amount=h,dir=(0,1,0))
 tip_x=-end_s if flat_pose else tail_l
 corner_edges=[]
 for edge in sheet.edges():
  bb=edge.bounding_box()
  if abs(bb.size.Z-t)<1e-6 and bb.size.X<1e-6 and bb.size.Y<1e-6 and abs(bb.min.X-tip_x)<1e-6 and abs(abs(bb.min.Y)-tail_h/2)<1e-6:
   corner_edges.append(edge)
 assert len(corner_edges)==2
 prior_volume=sheet.volume
 sheet=fillet(corner_edges,radius=tip_r)
 if flat_pose:
  assert abs(prior_volume-sheet.volume-2*(1-math.pi/4)*tip_r**2*t)<1e-4
 for yy in (slot_y1,slot_y2):
  if flat_pose:
   sheet-=Pos(-free_l-slot_x,yy,z0-1)*extrude(slot_profile,amount=t+2)
  else:
   sheet-=Pos(slot_x,yy,span-R-1)*extrude(slot_profile,amount=2*R+2)
   slot_min=slot_x-slot_l/2
   if slot_min<0:
    assert slot_min+slot_r<=-A and slot_min>=-A-span
    sheet-=Pos(-R/2,yy,span+R/2)*Box(R+0.02,slot_w,R+0.02)
    sheet-=Pos(-R+2*t,yy,span+A+slot_x)*Rot(0,-90,0)*extrude(slot_profile,amount=4*t)
 assert len(sheet.solids())==1
 return sheet
body=make_sheet(flat)
if flat:
 assert abs(body.bounding_box().min.Z-z0)<1e-6
 assert abs(body.bounding_box().size.Z-t)<1e-6
 expected_area=(end_s+tab_l)*h-2*(1-math.pi/4)*tip_r**2-2*slot_profile.area
 assert abs(body.volume-expected_area*t)<1e-5, 'Uniform sheet volume does not match footprint times thickness'
print('Uniform thickness',t,'flat bottom',z0,'no depressed band or transition')
print('Slots',slot_l,slot_w,'corner R',slot_r,'center from bend',slot_x,'Y',slot_y1,slot_y2)
print('Developed free length',free_l,'total',end_s+tab_l,'flat',flat)
publish('spine',body,'02 等厚护轴薄片',material='tpu')
