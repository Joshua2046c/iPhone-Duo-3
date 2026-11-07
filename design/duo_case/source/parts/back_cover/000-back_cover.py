# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# cell: back_cover
# User-reference height; raised perimeter wall retains the open hinge side.
PHONE_H = 117.8
wall_h=param('back_cover_wall_height',6.2)
PHONE_W=param('back_cover_phone_width',81.0)
reduction=param('back_cover_hinge_side_reduction',3.1)
shift=reduction/2
inset=param('back_cover_extra_hinge_inset',1.0)
inner_left_r=param('back_cover_inner_left_radius',1.0)
cam_inner_expand=param('back_cover_camera_inner_expansion',4.0)
cam_inner_depth=param('back_cover_camera_inner_depth',3.9)
land_h=param('back_cover_camera_vertical_land_height',0.3)
clearance=param('back_cover_fit_clearance',0.25)
wall=param('back_cover_wall',1.6)
plate=param('back_cover_plate',3.4)
seat_z=param('back_cover_phone_seat_z',2.4)
radius=param('back_cover_corner_radius',10.0)
lip=param('back_cover_corner_inward',0.7)
lip_h=param('back_cover_lip_height',0.7)
cam_w=param('back_cover_camera_width',55.0)
cam_h=param('back_cover_camera_height',23.0)
cam_x=param('back_cover_camera_x',10.0)
cam_y=param('back_cover_camera_y',42.5)
vol_x=param('back_cover_volume_x',6.0)
vol_w=param('back_cover_volume_opening',34.0)
power_y=param('back_cover_power_y',18.0)
power_l=param('back_cover_power_opening',21.0)
shutter_y=param('back_cover_shutter_y',-27.0)
shutter_l=param('back_cover_shutter_opening',23.0)
bottom_w=param('back_cover_bottom_opening',50.0)
bottom_x=param('back_cover_bottom_opening_x',0.45)
glue_l=param('back_cover_glue_recess_length',8.3)
glue_h=param('back_cover_glue_recess_height',115.0)
glue_y=param('back_cover_glue_recess_y',13.7)
glue_depth=param('back_cover_glue_recess_depth',1.2)
corner_soft=param('back_cover_left_corner_radius',1.0)
opening_soft=param('back_cover_opening_edge_radius',0.3)
turn=param('back_cover_opening_turn_radius',1.0)
def outline(w,h,r):
 return RectangleRounded(w,h,r)+Pos(-w/4,0)*Rectangle(w/2,h)
wi,hi=PHONE_W+2*clearance,PHONE_H+2*clearance
wo,ho=wi+2*wall,hi+2*wall
edge_x=shift-wo/2+inset
outside_z=seat_z-plate
outer=Pos(shift+inset/2,0)*outline(wo-inset,ho,radius+wall)
inner=Pos(shift,0)*outline(wi,hi,radius)
inner=fillet([v for v in inner.vertices() if abs(v.X+wi/2-shift)<1e-6],radius=inner_left_r)
# Move the retained inner walls toward the phone center; preserve the external envelope.
inner_wall_inset=param('back_cover_inner_wall_inset',0.045)
assert 0<=inner_wall_inset<inner_left_r-lip
inner=offset(inner,amount=-inner_wall_inset)
left_vertices=[v for v in outer.vertices() if abs(v.X-edge_x)<1e-6]
assert len(left_vertices)==2
outer=fillet(left_vertices,radius=corner_soft)
# Paired closing magnet seat on the marked central wall's top face.
# The common magnet dimensions live here; the front cover reads the same interface.
closing_mag_l=param('back_cover_closing_magnet_length',10.08)
closing_mag_w=param('back_cover_closing_magnet_width',1.6)
closing_mag_d=param('back_cover_closing_magnet_depth',1.03)
closing_mag_wall=param('back_cover_closing_magnet_surround',1.2)
closing_mag_floor=param('back_cover_closing_magnet_floor',1.2)
closing_mag_y=(shutter_y+shutter_l/2+turn+power_y-power_l/2-turn)/2
closing_mag_inner_x=shift+wi/2
closing_mag_x=closing_mag_inner_x+closing_mag_wall+closing_mag_w/2
closing_mag_boss_w=closing_mag_w+2*closing_mag_wall
closing_mag_boss_l=closing_mag_l+2*closing_mag_wall
closing_mag_raise=param('back_cover_closing_magnet_height_raise',0.05)
closing_mag_top=seat_z+wall_h+closing_mag_raise
closing_mag_bottom=outside_z
closing_mag_boss_h=closing_mag_top-closing_mag_bottom
# Match the original central wall's complete side-to-side span.
closing_mag_requested_blend=param('back_cover_closing_magnet_blend_length',2.2)
closing_mag_span=power_y-power_l/2-turn-(shutter_y+shutter_l/2+turn)
closing_mag_blend=closing_mag_requested_blend
closing_mag_land_l=closing_mag_span-2*closing_mag_blend
assert closing_mag_land_l>closing_mag_l
closing_mag_base_x=shift+wo/2
closing_mag_outer_x=closing_mag_x+closing_mag_boss_w/2
closing_mag_y0=closing_mag_y-closing_mag_land_l/2
closing_mag_y1=closing_mag_y+closing_mag_land_l/2
# Identical circular blends and tangent straight flanks keep the rim band uniform.
from math import radians, sin, cos
closing_mag_flank_angle=param('back_cover_closing_magnet_transition_angle',70.0)
theta=radians(closing_mag_flank_angle)
delta_x=closing_mag_outer_x-closing_mag_base_x
delta_y=closing_mag_blend
closing_mag_arc_r=(delta_y-delta_x*cos(theta)/sin(theta))/(2*sin(theta)-2*(1-cos(theta))*cos(theta)/sin(theta))
closing_mag_flank_l=(delta_x-2*closing_mag_arc_r*(1-cos(theta)))/sin(theta)
assert closing_mag_arc_r>0 and closing_mag_flank_l>0
p0=(closing_mag_base_x,closing_mag_y0-closing_mag_blend)
p1=(closing_mag_outer_x,closing_mag_y0)
p2=(closing_mag_outer_x,closing_mag_y1)
p3=(closing_mag_base_x,closing_mag_y1+closing_mag_blend)
q0=(closing_mag_base_x+closing_mag_arc_r-closing_mag_arc_r*cos(theta),p0[1]+closing_mag_arc_r*sin(theta))
q1=(closing_mag_outer_x-closing_mag_arc_r+closing_mag_arc_r*cos(theta),p1[1]-closing_mag_arc_r*sin(theta))
left_flank=[
 CenterArc((closing_mag_base_x+closing_mag_arc_r,p0[1]),closing_mag_arc_r,180,-closing_mag_flank_angle),
 Line(q0,q1),
 CenterArc((closing_mag_outer_x-closing_mag_arc_r,p1[1]),closing_mag_arc_r,-closing_mag_flank_angle,closing_mag_flank_angle)]
closing_mag_mirror_plane=Plane(origin=(0,closing_mag_y,0),x_dir=(1,0,0),z_dir=(0,1,0))
right_flank=[e.mirror(closing_mag_mirror_plane) for e in left_flank]
fair_edges=left_flank+[Line(p1,p2)]+right_flank+[
 Line(p3,(closing_mag_inner_x,p3[1])),
 Line((closing_mag_inner_x,p3[1]),(closing_mag_inner_x,p0[1])),
 Line((closing_mag_inner_x,p0[1]),p0)]
print('Matching planar transition arc radius',closing_mag_arc_r,'tangent flank length',closing_mag_flank_l)
closing_mag_fair_profile=make_face(Wire(fair_edges))
closing_mag_boss=Pos(0,0,closing_mag_bottom)*extrude(closing_mag_fair_profile,amount=closing_mag_boss_h)

body=Pos(0,0,outside_z)*extrude(outer,amount=plate)
# Keep the enlarged ends on the original rounded upper side-wall silhouette.
closing_mag_local_wall_h=wall_h+closing_mag_raise
closing_mag_wall_profile=Pos(closing_mag_y,seat_z+closing_mag_local_wall_h/2)*Rectangle(closing_mag_span,closing_mag_local_wall_h)
closing_mag_top_vertices=[v for v in closing_mag_wall_profile.vertices() if abs(v.Y-closing_mag_top)<1e-6]
closing_mag_wall_profile=fillet(closing_mag_top_vertices,radius=turn)
closing_mag_wall_profile+=Pos(closing_mag_y,(outside_z+seat_z)/2)*Rectangle(closing_mag_span+2*turn,plate)
closing_mag_end_mask=Pos(closing_mag_inner_x-1,0,0)*extrude(Plane.YZ*closing_mag_wall_profile,amount=closing_mag_boss_w+2)
closing_mag_boss &= closing_mag_end_mask
body+=closing_mag_boss
# Round the exterior back-face perimeter before the independent pockets and wall cutouts.
outer_round=param('back_cover_outer_rim_radius',0.8)
rim_edges=[]
for edge in body.edges():
 bb=edge.bounding_box()
 at_outer_face=abs(bb.min.Z-outside_z)<1e-6 and abs(bb.max.Z-outside_z)<1e-6
 on_hinge=abs(bb.min.X-edge_x)<1e-6 and abs(bb.max.X-edge_x)<1e-6
 if at_outer_face and not on_hinge:
  rim_edges.append(edge)
assert len(rim_edges)==15, 'Expected one continuous outer rim including the fairing'
assert closing_mag_arc_r>outer_round
body=fillet(rim_edges,radius=outer_round)
print('Back external rim radius',outer_round,'selected perimeter edges',len(rim_edges))
# Continuous retention ledge follows every wall segment; access cuts remove wall and lip together.
# Relieve only the two large free-side corner lips; keep straight retention edges unchanged.
corner_lip_relief=param('back_cover_corner_lip_relief',0.10)
assert 0<=corner_lip_relief<lip and inner_left_r>lip
corner_lip_radius_reduction=corner_lip_relief/(2**0.5-1)
corner_lip_radius=radius-lip-corner_lip_radius_reduction
assert corner_lip_radius>0
lip_inner=Pos(shift,0)*outline(wi-2*lip,hi-2*lip,corner_lip_radius)
lip_left_vertices=[v for v in lip_inner.vertices() if abs(v.X-(shift-wi/2+lip))<1e-6]
assert len(lip_left_vertices)==2
lip_inner=fillet(lip_left_vertices,radius=inner_left_r-lip)
lip_inner=offset(lip_inner,amount=-inner_wall_inset)
print('Inner wall inward shift',inner_wall_inset,'cavity profile',inner.bounding_box().size,'straight wall thickness',wall+inner_wall_inset)
print('Free-side corner lip maximum relief',corner_lip_relief,'minimum ledge',lip-corner_lip_relief,'straight ledge',lip)
ring=extrude(outer,amount=wall_h)-extrude(inner,amount=wall_h)
ledge=extrude(outer,amount=lip_h)-extrude(lip_inner,amount=lip_h)
# The hinge-side upright ends have flat inner faces; only the upper retention lip projects inward.
hinge_open_h=hi-2*lip
hinge_cut_end=shift-wi/2+max(inner_left_r,lip)+0.2
hinge_open=Pos((edge_x-1+hinge_cut_end)/2,0,wall_h/2)*Box(hinge_cut_end-edge_x+1,hinge_open_h,wall_h+2)
# Clear the residual inner corner bulges from both upright ends before the ledge is joined.
hinge_wall_open=Pos((edge_x-1+hinge_cut_end)/2,0,wall_h/2)*Box(hinge_cut_end-edge_x+1,hi,wall_h+2)
ring-=hinge_wall_open
ring=Compound(children=ring.solids())
ledge-=hinge_open
ring+=Pos(0,0,wall_h-lip_h)*Compound(children=ledge.solids())
ring=Compound(children=ring.solids())
ring-=hinge_open
ring=Compound(children=ring.solids())
ring-=Pos(vol_x,ho/2,wall_h/2)*Box(vol_w+2*turn,2*wall+2,wall_h+2)
ring=Compound(children=ring.solids())
ring-=Pos(shift+wo/2,power_y,wall_h/2)*Box(2*wall+2,power_l+2*turn,wall_h+2)
ring=Compound(children=ring.solids())
ring-=Pos(shift+wo/2,shutter_y,wall_h/2)*Box(2*wall+2,shutter_l+2*turn,wall_h+2)
ring=Compound(children=ring.solids())
ring-=Pos(bottom_x,-ho/2,wall_h/2)*Box(bottom_w+2*turn,2*wall+2,wall_h+2)
ring=Compound(children=ring.solids())
# Round the access-wall assembly before joining its enlarged outside carrier.
floor_with_carrier=body
body=Pos(0,0,outside_z)*extrude(outer,amount=plate)
body+=Pos(0,0,seat_z)*ring
# Equal-radius ends and parallel common tangents give the requested symmetric capsule.
# Symmetric end radii are derived from short-axis height, not independent dimensions.
assert cam_w>cam_h>0
rr=cam_h/2
rl=rr
xr=cam_w/2-rr
xl=-cam_w/2+rl
nx=(rl-rr)/(xr-xl)
ny=(1-nx*nx)**0.5
tl=(xl+rl*nx,rl*ny)
tr=(xr+rr*nx,rr*ny)
glass=(Pos(xl,0)*Circle(rl)+Pos(xr,0)*Circle(rr)+
       Polygon(tl,(tl[0],-tl[1]),(tr[0],-tr[1]),tr,align=None))

# Flat exterior mouth; +4 mm inner relief. The clearance cutter reaches 3.9 mm from the phone seat.
camera_mouth_z=seat_z-cam_inner_depth
# No external raised pad or recessed ring seat: the camera surround stays on outside_z.
assert 0<land_h<plate
u0=land_h/plate
def flare_amount(u):
 return cam_inner_expand*(6*u**5-15*u**4+10*u**3)
def camera_profile(amount):
 lt=(xl+(rl+amount)*nx,(rl+amount)*ny)
 rt=(xr+(rr+amount)*nx,(rr+amount)*ny)
 return (Pos(xl,0)*Circle(rl+amount)+Pos(xr,0)*Circle(rr+amount)+
         Polygon(lt,(lt[0],-lt[1]),(rt[0],-rt[1]),rt,align=None))
land_expand=flare_amount(u0)
land_profile=camera_profile(land_expand)
sections=[]
for v in (0.0,0.1,0.25,0.5,0.75,0.9,1.0):
 u=u0+(1-u0)*v
 sk=camera_profile(flare_amount(u))
 assert len(sk.faces())==1 and len(sk.wires())==1, 'Camera station must be one closed profile'
 sections.append((Pos(cam_x,cam_y,outside_z+u*plate)*sk).faces()[0])
funnel=loft(sections,ruled=False)
# The outward offset matches the old flare at the top of the specified vertical land.
# Extend its straight cutter through free air, overlapping only inside the upper cutter.
funnel+=Pos(cam_x,cam_y,camera_mouth_z)*extrude(land_profile,amount=outside_z+land_h-camera_mouth_z+0.01)
fb=funnel.bounding_box()
assert abs(fb.min.Z-camera_mouth_z)<1e-5 and abs(fb.max.Z-seat_z)<1e-5, 'Camera funnel depth differs from 3.9 mm'
ib=offset(glass,amount=cam_inner_expand).bounding_box().size
gb=glass.bounding_box().size
assert abs(ib.X-gb.X-2*cam_inner_expand)<1e-5 and abs(ib.Y-gb.Y-2*cam_inner_expand)<1e-5, 'Inside opening offset differs from 4 mm'
# Apply this cutter after the adjacent button rim has been blended.
# The enlarged relief stops at the phone seat: extending it upward cut a notch in the perimeter rim.
# The existing 3.9 mm clearance-cut envelope extends outside the 3.4 mm back plate.
assert abs((seat_z-camera_mouth_z)-cam_inner_depth)<1e-7
# Two integral end stops leave 115.7 mm between their inward faces.
# Current bonded shield width is 115.3 mm, leaving 0.2 mm per end.
stop_gap=param('back_cover_shield_stop_spacing',115.7)
stop_land=(glue_h-stop_gap)/2
assert 0<stop_gap<glue_h and stop_land>=1.2
# Cut only between the stop faces; the uncut ends are integral pads flush with seat_z.
bond_recess_cut=Pos(edge_x+(glue_l-1)/2,glue_y,seat_z-glue_depth+(glue_depth+0.001)/2)*Box(glue_l+1,stop_gap,glue_depth+0.001)
floor_with_carrier-=bond_recess_cut
body-=bond_recess_cut
print('Bond recess end stops inner separation',stop_gap,'each end length',stop_land,'width',glue_l,'height',glue_depth,'flush top Z',seat_z)

# Profile blends are independent of the small through-thickness edge roll.
# Widen by one turn radius at each end so the original rectangular access remains clear.
eps=1e-5
openings=(
 ('y',ho/2,hi/2-inner_wall_inset,vol_x-vol_w/2-turn,vol_x+vol_w/2+turn),
 ('y',-ho/2,-hi/2+inner_wall_inset,bottom_x-bottom_w/2-turn,bottom_x+bottom_w/2+turn),
 ('x',shift+wo/2,shift+wi/2-inner_wall_inset,power_y-power_l/2-turn,power_y+power_l/2+turn),
 ('x',shift+wo/2,shift+wi/2-inner_wall_inset,shutter_y-shutter_l/2-turn,shutter_y+shutter_l/2+turn))
turn_edges=[]
for axis,outer_side,inner_side,lo,upper in openings:
 chosen=[]
 for e in body.edges():
  if e.geom_type!=GeomType.LINE:
   continue
  bb=e.bounding_box()
  amin,amax=(bb.min.X,bb.max.X) if axis=='x' else (bb.min.Y,bb.max.Y)
  bmin,bmax=(bb.min.Y,bb.max.Y) if axis=='x' else (bb.min.X,bb.max.X)
  at_end=(abs(bmin-lo)<eps and abs(bmax-lo)<eps) or (abs(bmin-upper)<eps and abs(bmax-upper)<eps)
  level=abs(bb.max.Z-bb.min.Z)<eps and (abs(bb.min.Z-seat_z)<eps or abs(bb.min.Z-seat_z-wall_h)<eps)
  through_wall=amin>=min(outer_side,inner_side)-lip-eps and amax<=max(outer_side,inner_side)+lip+eps and amax-amin>eps
  if at_end and level and through_wall:
   chosen.append(e)
 assert len(chosen)==4, 'Expected two lower and two upper profile corners'
 turn_edges.extend(chosen)
body=fillet(turn_edges,radius=turn)

# Preserve the independent bottom interface with its existing clipped R0.3 wall.
unrolled_access_body=body
# Roll the touch-facing outer U rim, including its new profile arcs.
opening_edges=[]
for axis,outer_side,inner_side,lo,upper in openings:
 chosen=[]
 for e in body.edges():
  bb=e.bounding_box()
  amin,amax=(bb.min.X,bb.max.X) if axis=='x' else (bb.min.Y,bb.max.Y)
  bmin,bmax=(bb.min.Y,bb.max.Y) if axis=='x' else (bb.min.X,bb.max.X)
  on_outer=abs(amin-outer_side)<eps and abs(amax-outer_side)<eps
  on_inner=abs(amin-inner_side)<eps and abs(amax-inner_side)<eps
  in_span=bmin>=lo-turn-eps and bmax<=upper+turn+eps
  rising=bb.max.Z-bb.min.Z>eps
  if bb.min.Z>=seat_z-eps and in_span and on_outer:
   chosen.append(e)
 assert len(chosen)>=5, 'Incomplete blended rim'
 opening_edges.extend(chosen)
body=fillet(opening_edges,radius=opening_soft)

original_bottom_body=floor_with_carrier+(body&Pos(shift,0,seat_z+wall_h/2)*Box(wo+2,ho+2,wall_h))
access_partition_y=shutter_y-shutter_l/2-2*turn
lower_access_mask=Pos(shift,(access_partition_y-ho/2-1)/2,(outside_z+seat_z+wall_h)/2)*Box(wo+20,access_partition_y+ho/2+1,plate+wall_h+2)
upper_access_mask=Pos(shift,(access_partition_y+ho/2+1)/2,(outside_z+seat_z+wall_h)/2)*Box(wo+20,ho/2+1-access_partition_y,plate+wall_h+2)
original_bottom_body &= lower_access_mask
body=unrolled_access_body

# Keep only the finished access wall above the plate, then merge it with the continuous rounded base.
finished_wall=body&Pos(shift,0,seat_z+wall_h/2)*Box(wo+2,ho+2,wall_h)
body=floor_with_carrier+finished_wall

# Constant-angle finger ramp and tangent lower corner are one opening profile.
ramp_angle=param('back_cover_button_ramp_angle',20.0)
from math import tan, radians
ramp_slope=tan(radians(ramp_angle))
ramp_specs=[
 ('power','x',shift+wi/2-inner_wall_inset,shift+wo/2,power_y,power_l),
 ('shutter','x',shift+wi/2-inner_wall_inset,shift+wo/2,shutter_y,shutter_l),
 ('volume','y',hi/2-inner_wall_inset,ho/2,vol_x,vol_w)]
ramp_depth=(wall+inner_wall_inset)*ramp_slope
assert 0<ramp_angle<30
ramp_cutters=[]
for axis,outer_side,inner_side,lo,upper in openings:
 a=min(inner_side,outer_side)-lip-0.5
 c=max(inner_side,outer_side)+lip+0.5
 local_slope=ramp_slope if outer_side>0 else 0
 def tangent_opening_station(at):
  floor_z=seat_z-(at-inner_side)*local_slope
  # The top remains above the perimeter even after oblique extrusion.
  top_z=seat_z+wall_h+2+(c-a)*abs(local_slope)
  cross=Pos((lo+upper)/2,(floor_z+top_z)/2)*Rectangle(upper-lo,top_z-floor_z)
  lower_vertices=[v for v in cross.vertices() if abs(v.Y-floor_z)<eps]
  assert len(lower_vertices)==2
  cross=fillet(lower_vertices,radius=turn)
  if axis=='x':
   return (Pos(at,0,0)*(Plane.YZ*cross)).faces()[0]
  return (Pos(0,at,0)*(Plane.XZ*cross)).faces()[0]
 direction=(1,0,-local_slope) if axis=='x' else (0,1,-local_slope)
 distance=(c-a)*(1+local_slope**2)**0.5
 ramp_cutters.append(extrude(tangent_opening_station(a),amount=distance,dir=direction))
body-=ramp_cutters
assert len(body.solids())==1
print('Tangent lower corners',turn,'constant ramp angle',ramp_angle,'virtual outer drop',ramp_depth)

# Round the complete access rim after cutting the ramps, before camera relief trims it.
# This shares the existing R0.3 parameter with the original opening edges.
opening_edges=[]
ramp_opening_edge_counts=[]
for axis,outer_side,inner_side,lo,upper in openings:
 chosen=[]
 for e in body.edges():
  bb=e.bounding_box()
  amin,amax=(bb.min.X,bb.max.X) if axis=='x' else (bb.min.Y,bb.max.Y)
  bmin,bmax=(bb.min.Y,bb.max.Y) if axis=='x' else (bb.min.X,bb.max.X)
  on_outer=abs(amin-outer_side)<eps and abs(amax-outer_side)<eps
  in_span=bmin>=lo-turn-eps and bmax<=upper+turn+eps
  above_floor=bb.min.Z>=seat_z-ramp_depth-eps
  if on_outer and in_span and above_floor:
   chosen.append(e)
 assert len(chosen)>=6, 'Incomplete access rim including its tangent lower corners'
 ramp_opening_edge_counts.append(len(chosen))
 opening_edges.extend(chosen)
body=fillet(opening_edges,radius=opening_soft)
# Assemble the ramped button section with the unchanged bottom interface.
body=(body&upper_access_mask)+original_bottom_body
assert body.is_valid and len(body.solids())==1
print('Shared access edge radius',opening_soft,'rim segment counts',ramp_opening_edge_counts)
for axis,outer_side,inner_side,lo,upper in openings:
 center=(lo+upper)/2
 span=upper-lo-2*turn
 if axis=='x':
  access=Pos(outer_side,center,seat_z+wall_h/2)*Box(2*wall+2,span,wall_h)
 else:
  access=Pos(center,outer_side,seat_z+wall_h/2)*Box(span,2*wall+2,wall_h)
 assert (body&access).volume<1e-6, 'Original rectangular button passage obstructed'

# Cut the camera relief after blending the button rim: the expanded relief trims the blend locally.
body-=funnel
body-=Pos(cam_x,cam_y,camera_mouth_z-0.1)*extrude(land_profile,amount=0.15)

# Exterior back remains a continuous plane without engraving.
# User-sized blind annulus for a MagSafe magnet; center inferred from the reference photo.
mag_id=param('back_cover_magsafe_inner_diameter',46.2)
mag_od=param('back_cover_magsafe_outer_diameter',54.2)
mag_depth=param('back_cover_magsafe_depth',0.81)
mag_x=param('back_cover_magsafe_x',2.05)
mag_y=param('back_cover_magsafe_y',-5.0)
assert 0<mag_id<mag_od and 0<mag_depth<plate
mag_profile=Pos(mag_x,mag_y)*(Circle(mag_od/2)-Circle(mag_id/2))
mag_disk=Pos(mag_x,mag_y)*Circle(mag_od/2)
mag_floor=seat_z-mag_depth
mag_cut=Pos(0,0,mag_floor)*extrude(mag_profile,amount=mag_depth+0.01)
mag_area=3.141592653589793*((mag_od/2)**2-(mag_id/2)**2)
assert abs((body&mag_cut).volume-mag_area*mag_depth)<1e-4, 'Magnet annulus intersects an existing opening or edge'
cam_inner_profile=Pos(cam_x,cam_y)*offset(glass,amount=cam_inner_expand)
mag_cam_gap=mag_disk.distance_to(cam_inner_profile)
assert mag_cam_gap>0, 'Magnet ring touches camera relief'
body-=mag_cut
# Verify a continuous solid floor below the whole annulus, without exterior engraving.
mag_support=Pos(0,0,outside_z)*extrude(mag_profile,amount=mag_floor-outside_z)
assert abs((body&mag_support).volume-mag_area*(mag_floor-outside_z))<1e-4, 'Magnet pocket breaks through the back surface'
mag_floor_faces=[]
for f in body.faces():
 bb=f.bounding_box()
 if f.geom_type==GeomType.PLANE and abs(bb.min.Z-mag_floor)<1e-6 and abs(bb.max.Z-mag_floor)<1e-6 and abs(f.area-mag_area)<1e-4:
  mag_floor_faces.append(f)
assert len(mag_floor_faces)==1, 'Magnet pocket floor must be one continuous annulus'
print('MagSafe inner/outer diameter',mag_id,mag_od,'depth',mag_depth,'center',mag_x,mag_y,'remaining floor',mag_floor-outside_z,'camera clearance',mag_cam_gap)

# Lower alignment magnet: capsule footprint inferred from the uploaded 18.5 mm tail.
mag_tail_l=param('back_cover_magsafe_tail_length',18.5)
mag_tail_w=param('back_cover_magsafe_tail_width',6.0)
mag_tail_gap=param('back_cover_magsafe_tail_gap',2.0)
assert mag_tail_l>mag_tail_w>0 and mag_tail_gap>0
mag_tail_x=mag_x
mag_tail_y=mag_y-mag_od/2-mag_tail_gap-mag_tail_l/2
mag_tail_profile=Pos(mag_tail_x,mag_tail_y)*SlotOverall(mag_tail_l,mag_tail_w,rotation=90)
mag_tail_cut=Pos(0,0,mag_floor)*extrude(mag_tail_profile,amount=mag_depth+0.01)
assert abs((body&mag_tail_cut).volume-mag_tail_profile.area*mag_depth)<1e-5, 'Tail magnet must be a full-depth blind recess on the inside face'
body-=mag_tail_cut
# Continuous full backing beneath the tail magnet.
mag_tail_support=Pos(0,0,outside_z)*extrude(mag_tail_profile,amount=mag_floor-outside_z)
assert abs((body&mag_tail_support).volume-mag_tail_support.volume)<1e-5, 'Tail pocket has insufficient solid backing'
assert mag_tail_profile.bounding_box().min.Y>-hi/2+inner_wall_inset, 'Tail pocket reaches the end wall'
print('MagSafe tail L/W/depth',mag_tail_l,mag_tail_w,mag_depth,'center',mag_tail_x,mag_tail_y,'ring gap',mag_tail_gap,'minimum remaining backing',mag_floor-outside_z)

# User-marked hinge-side upper wall endpoints: R3 in side elevation (XZ), both Y ends.
end_top_r=param('back_cover_hinge_wall_top_radius',3.0)
end_top_z=seat_z+wall_h
assert 0<end_top_r<wall_h-lip_h
end_corner_box=Pos(edge_x+(end_top_r-1)/2,0,end_top_z+(1-end_top_r)/2)*Box(end_top_r+1,ho+2,end_top_r+1)
end_corner_disk=Pos(edge_x+end_top_r,0,end_top_z-end_top_r)*Cylinder(end_top_r,ho+4,rotation=(90,0,0))
end_round_cutter=end_corner_box-end_corner_disk
body-=end_round_cutter
end_round_faces=[]
for face in body.faces():
 bb=face.bounding_box()
 if face.geom_type==GeomType.CYLINDER and bb.min.X>=edge_x-1e-5 and bb.max.X<=edge_x+end_top_r+1e-5 and bb.min.Z>=end_top_z-end_top_r-1e-5 and bb.max.Z>=end_top_z-1e-5:
  end_round_faces.append(face)
assert len(end_round_faces)==2, 'Expected exactly two matching hinge-end R3 faces'
print('Hinge wall upper endpoint radius',end_top_r,'matching faces',len(end_round_faces),'tangent X',edge_x+end_top_r,'vertical tangent Z',end_top_z-end_top_r)

# Full rectangular end lands are solid from the recess floor to the phone-seat plane.
for side in (-1,1):
 stop_probe=Pos(edge_x+glue_l/2,glue_y+side*(stop_gap/2+stop_land/2),seat_z-glue_depth/2)*Box(glue_l,stop_land,glue_depth)
 assert abs((body&stop_probe).volume-stop_probe.volume)<1e-6, 'End stop is incomplete'
 clear_probe=Pos(edge_x+glue_l/2,glue_y+side*(stop_gap/2-0.05),seat_z-glue_depth/2)*Box(glue_l-0.1,0.05,glue_depth-0.1)
 assert (body&clear_probe).volume<1e-7, 'End stop intrudes into sheet opening'

assert plate-glue_depth>=1.2
assert len(body.solids())==1
assert abs(body.bounding_box().min.X-edge_x)<1e-6
assert abs(body.bounding_box().min.Z-outside_z)<1e-6, 'Camera surround must be flush with back plane'
land_faces=[]
for face in body.faces():
 bb=face.bounding_box()
 if face.geom_type==GeomType.CYLINDER and bb.min.Y>=cam_y-cam_h/2-1 and bb.max.Y<=cam_y+cam_h/2+1 and abs(bb.min.Z-outside_z)<1e-5 and abs(bb.max.Z-(outside_z+land_h))<1e-5:
  land_faces.append(face)
assert len(land_faces)==2, 'Both camera round ends must have a full-height vertical land'
print('Camera nominal upper Y',cam_y+cam_h/2,'lower Y',cam_y-cam_h/2)
print('Camera vertical land height',land_h,'radial enlargement',land_expand,'outer mouth',cam_w+2*land_expand,cam_h+2*land_expand)
# Both return walls still reach the hinge edge below the new upper-end radius; the lip remains beyond its tangent.
for side in (-1,1):
 for xx,yy,zz in ((edge_x+0.025,side*(hi/2+0.3),end_top_z-end_top_r-0.2),(edge_x+end_top_r+0.1,side*(hi/2-lip+0.2),seat_z+wall_h-lip_h/2)):
  probe=Pos(xx,yy,zz)*Box(0.05,0.05,0.05)
  assert (body&probe).volume>0.05**3*0.999, 'Rounded wall end or retaining lip beyond tangent is incomplete'
for side in (-1,1):
 nub_check=Pos((edge_x+hinge_cut_end)/2,side*(hi/2-lip/2),seat_z+(wall_h-lip_h)/2)*Box(hinge_cut_end-edge_x,lip,wall_h-lip_h)
 assert (body&nub_check).volume<1e-7, 'Residual hinge-end corner protrusion'
assert abs(glue_h-hi)<1e-6, 'Long recess must reach both marked clip inner planes'
assert abs(body.bounding_box().max.Z-closing_mag_top)<1e-6
# Check inward ledge presence on all seven retained straight wall segments.
probe_size=0.05
for px,py in ((-30,hi/2-lip+0.05),(30,hi/2-lip+0.05),(-30,-hi/2+lip-0.05),(30,-hi/2+lip-0.05),(shift+wi/2-lip+0.05,40),(shift+wi/2-lip+0.05,0),(shift+wi/2-lip+0.05,-44)):
 probe=Pos(px,py,seat_z+wall_h-lip_h/2)*Box(probe_size,probe_size,probe_size)
 assert (body&probe).volume>probe_size**3*0.999, 'Retaining lip missing from a retained wall segment'
hinge_probe=Pos(shift-wi/2+lip-0.05,0,seat_z+wall_h-lip_h/2)*Box(probe_size,probe_size,probe_size)
assert (body&hinge_probe).volume<1e-8, 'Unsupported lip spans open hinge side'
print('Rear wall height',wall_h,'top Z',seat_z+wall_h,'inward lip',lip,'seven segments present; hinge and four passages clear')

closing_mag_cut=Pos(closing_mag_x,closing_mag_y,closing_mag_top-closing_mag_d/2+0.005)*Box(closing_mag_w,closing_mag_l,closing_mag_d+0.01)
closing_mag_removed=(body&closing_mag_cut).volume
assert abs(closing_mag_removed-closing_mag_l*closing_mag_w*closing_mag_d)<1e-6
body-=closing_mag_cut
closing_mag_support=Pos(closing_mag_x,closing_mag_y,closing_mag_bottom+closing_mag_floor/2)*Box(closing_mag_w,closing_mag_l,closing_mag_floor)
assert abs((body&closing_mag_support).volume-closing_mag_support.volume)<1e-6
assert len(body.solids())==1
print('Lower closing magnet L/W/D',closing_mag_l,closing_mag_w,closing_mag_d,'XY center',closing_mag_x,closing_mag_y,'mouth/floor Z',closing_mag_top,closing_mag_top-closing_mag_d,'outward extension',closing_mag_x+closing_mag_boss_w/2-(shift+wo/2))



# recycle_badge_bond: matching full-footprint shallow recess, no arrow engraving.
badge = part("recycle_badge")
recycle_x = param('back_cover_recycle_x', 2.05)
recycle_y = param('back_cover_recycle_y', -45.0)
badge_recess_depth = param('back_cover_badge_recess_depth', 0.1)
badge_seat_profile = Pos(recycle_x,recycle_y)*badge.base_profile
badge_seat_floor_z = outside_z+badge_recess_depth
badge_seat_cutter = Pos(0,0,outside_z-0.01)*extrude(badge_seat_profile,amount=badge_recess_depth+0.01,dir=(0,0,1))
body -= badge_seat_cutter
# Perimeter guide cut: 0.3 mm inward, a further 0.1 mm below the full seat.
badge_guide_width = param('back_cover_badge_guide_width',0.3)
badge_guide_extra_depth = param('back_cover_badge_guide_extra_depth',0.1)
badge_guide_profile = badge_seat_profile-offset(badge_seat_profile,amount=-badge_guide_width)
badge_guide_floor_z = badge_seat_floor_z+badge_guide_extra_depth
badge_guide_cutter = Pos(0,0,outside_z-0.01)*extrude(badge_guide_profile,amount=badge_recess_depth+badge_guide_extra_depth+0.01,dir=(0,0,1))
body -= badge_guide_cutter
print('Rear inward perimeter guide width/extra depth/total depth',badge_guide_width,badge_guide_extra_depth,badge_recess_depth+badge_guide_extra_depth)

assert len(body.solids())==1 and body.is_valid
print('Rear badge recess depth/floor/area',badge_recess_depth,badge_seat_floor_z,badge_seat_profile.area)
publish('back_cover',body,'01 开边胶接背盖')