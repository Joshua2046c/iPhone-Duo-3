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



# Exact reference artwork with the three original fold slits preserved.
# Trace evidence: product/references/recycling-symbol-trace.json.
recycle_w=param('back_cover_recycle_width',18.0)
recycle_depth=param('back_cover_recycle_depth',0.3)
recycle_x=param('back_cover_recycle_x',2.05)
recycle_y=param('back_cover_recycle_y',-45.0)
recycle_contours=[[[56.166667,48.708333],[55.75,48.708333],[55.416667,48.541667],[54.916667,48.125],[54.083333,47.791667],[53.333333,47.041667],[52.916667,46.875],[52.5,46.541667],[51.666667,46.125],[51.25,46.041667],[50.416667,45.625],[49.916667,45.208333],[48.75,44.708333],[48.083333,44.125],[47.166667,43.791667],[46.25,43.041667],[45.833333,42.875],[45.666667,42.708333],[45.25,42.541667],[44.75,42.208333],[44.166667,42.041667],[43.333333,41.625],[42.833333,41.125],[41.833333,40.708333],[41.416667,40.291667],[39.916667,39.625],[39.083333,39.041667],[38.5,38.791667],[38.125,38.416667],[38.041667,38],[38.375,37.25],[38.875,36.5],[38.958333,36.083333],[39.208333,35.583333],[39.708333,35],[40.125,34],[40.791667,33.25],[41.125,32.75],[41.625,31.75],[41.625,31.583333],[41.791667,31.416667],[41.875,31.166667],[42.375,30.416667],[42.625,30.166667],[43.041667,29.166667],[43.708333,28.5],[44.291667,27],[44.791667,26.333333],[45.125,25.666667],[45.208333,25.25],[45.708333,24.583333],[45.875,24.166667],[46.208333,23.666667],[46.458333,23.416667],[46.875,22.583333],[46.958333,22.25],[47.708333,21.5],[48.291667,20.5],[48.875,19.833333],[49.041667,19.416667],[49.416667,19.041667],[49.75,18.875],[50.25,18.291667],[51.416667,17.708333],[52.166667,16.958333],[52.5,16.791667],[52.75,16.791667],[52.833333,16.708333],[53.25,16.625],[54.083333,16.041667],[54.25,16.041667],[54.333333,15.958333],[55.416667,15.958333],[55.5,15.875],[56.666667,15.791667],[56.75,15.708333],[58.333333,15.708333],[58.416667,15.791667],[59.75,15.875],[59.833333,15.958333],[60.666667,15.958333],[60.75,16.041667],[61.166667,16.125],[61.833333,16.625],[62.416667,16.791667],[62.916667,17.041667],[63.75,17.958333],[64.416667,18.208333],[64.708333,18.5],[64.875,18.833333],[65.625,19.5],[66.041667,20.416667],[66.416667,20.791667],[66.5,20.791667],[66.875,21.25],[66.958333,21.666667],[67.041667,21.75],[67.041667,22],[67.291667,22.583333],[67.625,22.833333],[68.208333,24],[68.541667,24.333333],[68.708333,24.666667],[68.875,25.333333],[69.375,26.166667],[69.375,26.666667],[68.875,27.583333],[68.875,27.75],[68.708333,28.083333],[68.125,28.75],[67.708333,29.583333],[67.041667,30.5],[66.875,30.916667],[66.375,31.5],[65.791667,32.833333],[65.208333,33.583333],[64.791667,34.666667],[64.125,35.333333],[63.875,35.833333],[63.875,36],[63.041667,37.166667],[63.041667,37.333333],[62.791667,37.75],[62.791667,37.916667],[62.541667,38.416667],[62.041667,39.083333],[61.875,39.666667],[61.708333,39.916667],[61.208333,40.333333],[61.041667,40.583333],[61.041667,40.75],[60.875,41.083333],[60.291667,41.833333],[60.125,42.166667],[60.041667,42.583333],[59.708333,43.25],[59.208333,43.833333],[58.625,45.25],[58.375,45.5],[58.041667,46.083333],[58.041667,46.25],[57.791667,46.833333],[57.208333,47.333333],[56.875,48.083333],[56.625,48.416667]],[[92.416667,43.125],[91.5,43.125],[91.416667,43.041667],[90.666667,43.041667],[90.583333,43.125],[88.166667,43.125],[88.083333,43.041667],[83.083333,43.041667],[83,42.958333],[79.166667,42.958333],[79.083333,42.875],[76.25,42.875],[76.166667,42.791667],[75.75,42.791667],[75.666667,42.875],[75.333333,42.875],[75.25,42.958333],[74.916667,42.958333],[74.833333,43.041667],[74,43.041667],[73.666667,42.875],[73.541667,42.666667],[73.541667,42.5],[73.916667,42.041667],[75.166667,41.541667],[76,40.958333],[77.333333,40.291667],[77.541667,40.083333],[77.708333,39.666667],[77.708333,39.166667],[77.625,39.083333],[77.625,38.916667],[77.208333,38.333333],[76.791667,37.333333],[76.125,36.75],[75.958333,36.416667],[75.875,35.916667],[75.208333,34.666667],[75.208333,34.5],[74.458333,33],[74.291667,32.833333],[74.041667,32.333333],[73.875,31.666667],[73.625,31.25],[73.125,30.833333],[72.958333,30.5],[72.791667,29.666667],[72.625,29.333333],[72.291667,29],[72.125,28.666667],[72.125,28.5],[71.958333,28.25],[71.958333,28.083333],[71.541667,27.583333],[71.291667,27.083333],[71.208333,26.5],[70.791667,25.583333],[70.291667,25.083333],[69.958333,24.5],[69.958333,24.333333],[69.791667,24],[69.125,23.166667],[69.125,23],[68.458333,21.666667],[68.291667,21.5],[67.791667,20.416667],[67.291667,19.75],[67.041667,19.25],[66.125,18.416667],[65.958333,18.083333],[65.583333,17.708333],[65.166667,17.458333],[64.666667,16.958333],[64.416667,16.875],[64.041667,16.5],[64.125,16.083333],[64.583333,15.875],[65.833333,15.875],[65.916667,15.958333],[66,15.875],[66.083333,15.958333],[66.166667,15.875],[68.083333,15.875],[68.166667,15.791667],[71.666667,15.791667],[71.75,15.708333],[80.583333,15.708333],[80.666667,15.791667],[80.916667,15.708333],[81,15.791667],[84.75,15.791667],[84.833333,15.875],[85.916667,15.875],[86,15.958333],[88.583333,15.958333],[89,16.208333],[89.208333,16.5],[89.583333,16.791667],[90.416667,17.041667],[91.791667,18.666667],[92.125,19.583333],[92.708333,20.25],[92.875,20.583333],[92.875,20.75],[93.125,21.166667],[93.125,21.333333],[93.291667,21.666667],[93.291667,21.916667],[93.375,22],[93.458333,22.416667],[93.875,23],[94.291667,24.083333],[94.791667,24.75],[95.125,25.75],[95.625,26.333333],[96.125,27.5],[96.666667,28.041667],[97.083333,28.208333],[97.75,28.208333],[98.583333,27.791667],[99,27.708333],[100,27.125],[100.25,26.875],[100.583333,26.708333],[101,26.291667],[101.583333,26.041667],[102.25,25.458333],[102.666667,25.291667],[102.916667,25.375],[103.041667,25.5],[103.041667,25.75],[102.708333,26.5],[102.208333,27.083333],[101.541667,28.25],[101.208333,28.583333],[100.875,29.25],[100.791667,29.583333],[100.208333,30.333333],[99.875,31.083333],[99.458333,31.666667],[98.958333,32.666667],[98.958333,32.833333],[98.208333,33.833333],[98.125,34.166667],[97.958333,34.416667],[97.958333,34.583333],[97.791667,34.833333],[97.208333,35.333333],[96.791667,36.416667],[96.125,37.333333],[95.875,37.833333],[95.708333,38.416667],[95.208333,39],[94.958333,39.5],[94.958333,39.666667],[94.708333,40.083333],[94.291667,40.5],[93.791667,41.75],[93.375,42.166667],[93.208333,42.5],[92.666667,43.041667],[92.5,43.041667]],[[102.5,87.875],[102.291667,87.75],[102.125,87.416667],[102.125,86.333333],[102.041667,86.25],[102.041667,86],[101.375,85],[101.375,84.583333],[101.541667,84.166667],[101.541667,83.5],[101.458333,83.416667],[101.458333,83.25],[100.875,82.5],[100.875,81.5],[100.791667,81.416667],[100.791667,81.25],[100.208333,80.666667],[100.041667,80.25],[99.958333,79.583333],[99.791667,79.25],[99.291667,78.666667],[99.125,78.333333],[98.958333,77.666667],[98.625,77],[98.291667,76.583333],[97.708333,75.25],[97.208333,74.583333],[96.708333,73.5],[96.208333,73],[95.958333,72.583333],[95.958333,72.416667],[95.791667,72.083333],[95.291667,71.5],[95.041667,71],[94.958333,70.583333],[94.625,69.916667],[94.291667,69.5],[93.791667,68.333333],[93.291667,67.916667],[93.125,67.666667],[92.958333,67.333333],[92.875,66.75],[92.625,66.25],[92.291667,65.916667],[91.958333,65.166667],[91.625,64.666667],[91.208333,64.25],[90.958333,63.75],[90.875,63.333333],[90.625,62.833333],[90.125,62.166667],[89.791667,61.333333],[89.125,60.666667],[88.958333,60.333333],[88.875,59.916667],[88.291667,58.833333],[88.291667,58.666667],[88.041667,58.166667],[87.875,58],[87.625,57.416667],[87.125,56.916667],[86.625,55.666667],[86.208333,55.166667],[85.958333,54.666667],[85.791667,54],[85.708333,53.916667],[85.708333,53.5],[86.083333,53.041667],[87,52.708333],[87.333333,52.375],[87.833333,52.041667],[90,50.958333],[91,50.208333],[91.5,49.958333],[91.75,49.958333],[92.333333,49.708333],[92.833333,49.208333],[93.416667,48.875],[93.75,48.791667],[94.333333,48.291667],[97.166667,46.875],[98,46.125],[98.333333,46.041667],[98.583333,45.875],[98.75,45.875],[99.5,45.208333],[99.833333,45.041667],[100.25,44.958333],[100.5,44.791667],[100.666667,44.791667],[101.583333,44.125],[102.416667,43.791667],[103.083333,43.041667],[103.25,42.958333],[104,42.958333],[104.625,43.5],[105.125,44.583333],[105.625,45.166667],[106.125,46.333333],[106.541667,46.833333],[106.875,47.5],[107.208333,48.583333],[107.791667,49.083333],[107.958333,49.333333],[108.208333,50.25],[108.875,51.083333],[109.041667,51.666667],[109.791667,53],[109.791667,53.166667],[110.125,53.833333],[110.125,54],[110.291667,54.333333],[110.791667,54.916667],[111.375,56.333333],[111.625,56.583333],[111.958333,57.166667],[112.125,57.75],[112.708333,58.5],[113.208333,59.5],[113.625,60.083333],[114.208333,61.416667],[114.791667,62],[114.958333,62.333333],[114.958333,62.75],[115.041667,62.833333],[115.041667,65.916667],[114.958333,66],[114.958333,66.583333],[114.875,66.666667],[114.875,66.833333],[114.375,67.416667],[114.041667,68.25],[113.958333,68.75],[113.208333,69.75],[112.875,70.416667],[112.875,70.583333],[112.708333,70.833333],[112.625,71.166667],[112.041667,71.916667],[111.625,72.75],[111.041667,73.416667],[110.791667,74],[110.208333,74.666667],[109.708333,75.666667],[109.125,76.416667],[108.791667,77.333333],[108.041667,78.25],[107.875,78.75],[107.208333,79.5],[106.458333,81.083333],[105.958333,81.75],[105.625,82.5],[105.208333,83],[104.791667,83.916667],[104.208333,84.583333],[104.208333,84.75],[104.041667,85],[104.041667,85.25],[103.708333,85.916667],[103.208333,86.5],[102.791667,87.666667]],[[35.166667,87.958333],[34.833333,87.958333],[34.666667,87.875],[34.291667,87.5],[33.708333,86.333333],[33.125,85.666667],[32.875,85.083333],[32.875,84.833333],[32.625,84.333333],[32.416667,84.208333],[32.041667,83.75],[31.875,83.416667],[31.875,83.166667],[31.541667,82.5],[31.041667,81.916667],[30.541667,80.5],[30.125,80],[29.708333,79.083333],[29.208333,78.583333],[28.958333,78.083333],[28.875,77.666667],[28.291667,76.833333],[27.958333,76.166667],[27.791667,75.583333],[26.708333,73.416667],[26.125,72.833333],[25.708333,71.833333],[25.291667,71.416667],[25.125,71.083333],[24.875,70.25],[24.125,69.25],[23.875,68.75],[23.708333,68],[23.458333,67.5],[23.125,67.083333],[22.958333,66.666667],[22.958333,63.25],[23.041667,63.166667],[23.125,62.75],[23.291667,62.583333],[23.708333,61.75],[23.875,61.083333],[24.291667,60.25],[24.791667,59.583333],[25.208333,58.666667],[25.958333,57.833333],[26.041667,57.583333],[26.375,57.083333],[26.708333,56.75],[26.875,56.333333],[27.208333,55.833333],[27.708333,55.333333],[28.208333,54.25],[28.791667,53.5],[29.125,52.416667],[29.208333,52.333333],[29.208333,52],[29.291667,51.916667],[29.208333,51.416667],[28.833333,51.041667],[28.333333,50.791667],[27.666667,50.125],[26.916667,49.791667],[26.333333,49.375],[25.166667,48.875],[24.916667,48.625],[24.833333,48.625],[24.375,48],[24.375,47.75],[24.75,47.541667],[25.083333,47.541667],[25.166667,47.625],[42.583333,47.625],[42.666667,47.541667],[43.5,47.541667],[44,47.791667],[44.708333,48.5],[44.958333,49.083333],[45.041667,49.5],[45.208333,49.833333],[45.625,50.333333],[46.041667,51.166667],[46.041667,51.333333],[46.291667,51.916667],[46.291667,52.166667],[46.458333,52.5],[46.875,53],[47.208333,53.666667],[47.791667,54.416667],[47.958333,55],[48.125,55.25],[48.125,55.416667],[48.791667,56.166667],[49.041667,57],[49.791667,58.416667],[49.791667,58.583333],[50.208333,59.5],[50.791667,60.166667],[50.958333,60.5],[51.041667,60.916667],[51.291667,61.416667],[51.708333,61.833333],[52.208333,63.083333],[52.791667,63.75],[52.958333,64.083333],[52.958333,64.333333],[53.041667,64.416667],[52.958333,64.833333],[52.75,64.958333],[52.416667,64.958333],[52,64.791667],[51.333333,64.125],[50.5,63.791667],[50,63.375],[49.5,63.125],[48.666667,63.041667],[48.333333,63.208333],[48.125,63.416667],[47.791667,64],[47.375,64.416667],[47.041667,65.083333],[46.958333,65.416667],[46.041667,66.416667],[46.041667,66.583333],[45.875,66.916667],[45.875,67.166667],[45.625,67.666667],[45.125,68.166667],[44.791667,69],[44.291667,69.583333],[43.708333,70.833333],[43.125,71.583333],[43.041667,71.916667],[42.625,72.75],[42.375,73],[42.041667,73.583333],[42.041667,73.75],[41.875,74],[41.875,74.166667],[41.708333,74.5],[41.125,75.083333],[40.958333,75.416667],[40.958333,75.583333],[40.791667,75.833333],[40.791667,76],[40.208333,76.666667],[39.541667,78.083333],[39.041667,78.75],[38.708333,79.666667],[38.125,80.25],[37.708333,81.083333],[37.208333,81.583333],[36.791667,82.416667],[36.708333,82.75],[36.291667,83.25],[36.041667,83.75],[35.958333,84.416667],[35.875,84.5],[35.875,84.75],[35.708333,85.166667],[35.541667,87.083333],[35.458333,87.166667],[35.375,87.666667]],[[81.416667,106.541667],[81.208333,106.416667],[80.875,105.916667],[80.125,105.25],[79.708333,104.25],[79.125,103.583333],[78.875,103.083333],[78.875,102.916667],[78.708333,102.75],[77.875,100.916667],[77.041667,99.833333],[77.041667,99.666667],[76.875,99.416667],[76.875,99.25],[76.708333,98.916667],[76.208333,98.333333],[75.958333,97.75],[75.875,97.333333],[75.208333,96.5],[74.958333,96],[74.958333,95.833333],[74.625,95.25],[74.625,95.083333],[74.208333,94.25],[74.041667,94.083333],[74.041667,93.916667],[73.708333,93.25],[73.208333,92.75],[73.041667,92.416667],[72.958333,91.833333],[72.708333,91.25],[72.583333,91.208333],[71.958333,90.5],[71.958333,90.333333],[71.625,89.5],[71.625,88.833333],[72.208333,87.583333],[72.625,87.083333],[72.958333,86.416667],[73.041667,86.083333],[73.708333,85.25],[73.708333,85.083333],[73.875,84.833333],[73.875,84.666667],[74.125,84.083333],[74.875,83.083333],[75.375,82],[75.708333,81.583333],[75.958333,81],[76.625,80.083333],[76.958333,79.25],[77.708333,78.416667],[78.041667,77.583333],[78.041667,77.416667],[78.791667,76.333333],[78.791667,76.166667],[79.208333,75.25],[79.708333,74.75],[80.125,73.916667],[80.458333,73.5],[80.958333,71.916667],[81.25,71.541667],[81.416667,71.541667],[81.5,71.458333],[81.708333,71.583333],[81.958333,72.083333],[81.958333,73.75],[81.875,73.833333],[81.875,76.583333],[81.958333,76.666667],[82.041667,77.25],[82.583333,77.708333],[83.333333,77.708333],[83.416667,77.625],[95.916667,77.625],[96,77.541667],[96.25,77.541667],[97.166667,77.875],[97.416667,77.875],[97.791667,78.25],[97.958333,78.583333],[97.958333,78.916667],[98.208333,79.5],[98.625,79.833333],[98.958333,80.416667],[99.041667,80.833333],[99.541667,81.75],[99.541667,81.916667],[100.125,82.916667],[100.125,84],[100.208333,84.083333],[100.208333,84.5],[100.458333,84.916667],[100.666667,85.041667],[100.958333,85.416667],[100.958333,86.416667],[100.875,86.5],[100.958333,89.666667],[100.208333,91.416667],[100.208333,91.916667],[100.125,92],[100.125,92.333333],[99.958333,92.666667],[99.875,93.083333],[99.125,94.166667],[99.125,94.333333],[98.875,94.75],[98.333333,95.208333],[97.583333,96.041667],[97.333333,96.125],[96.666667,96.791667],[96.083333,97.041667],[95.25,97.708333],[94.916667,97.875],[94.25,98.041667],[93.166667,98.708333],[92.083333,98.791667],[91.75,98.958333],[91.25,99.041667],[90.75,99.291667],[90.416667,99.291667],[90.333333,99.375],[89.083333,99.375],[89,99.458333],[83.416667,99.458333],[83.333333,99.375],[82.75,99.291667],[82.333333,99.458333],[81.958333,99.833333],[81.791667,100.166667],[81.708333,100.75],[81.625,100.833333],[81.625,101.333333],[81.541667,101.416667],[81.541667,101.75],[81.458333,101.833333],[81.458333,102.166667],[81.375,102.25],[81.375,102.916667],[81.291667,103],[81.291667,103.5],[81.375,103.583333],[81.375,105.333333],[81.625,106],[81.625,106.333333]],[[55,99.708333],[50.166667,99.708333],[50.083333,99.625],[49,99.625],[48.916667,99.541667],[48.166667,99.541667],[48.083333,99.458333],[46.75,99.458333],[46.666667,99.375],[45.916667,99.375],[44.666667,98.875],[43.583333,98.791667],[43,98.541667],[42.5,98.125],[41.333333,97.791667],[40.583333,97.125],[39.916667,96.791667],[38.458333,95.333333],[37.958333,94.583333],[37.875,94.25],[37.625,93.833333],[37.625,93.666667],[37.041667,92.916667],[36.958333,92.5],[36.875,92.416667],[36.791667,89],[36.875,88.916667],[36.875,88.166667],[36.958333,88.083333],[36.958333,86.333333],[37.041667,86.25],[37.041667,85.916667],[37.125,85.833333],[37.291667,85.166667],[37.708333,84.416667],[37.791667,83.916667],[37.875,83.833333],[38.208333,82.666667],[39.208333,80.666667],[39.708333,80.083333],[40.125,79.083333],[40.333333,78.875],[40.833333,78.625],[41.166667,78.291667],[41.5,78.125],[42.166667,78.125],[42.25,78.208333],[48,78.208333],[48.083333,78.125],[55.583333,78.125],[55.666667,78.041667],[65.416667,78.041667],[65.708333,78.25],[65.875,78.583333],[65.875,81.916667],[65.791667,82],[65.791667,96.666667],[65.708333,96.75],[65.791667,98.583333],[65.708333,98.666667],[65.708333,98.916667],[65.333333,99.375],[58.333333,99.458333],[58.25,99.541667],[57.083333,99.541667],[57,99.625],[55.083333,99.625]]]
ART_WIDTH=92.08333400000001
ART_CENTER_X=69
ART_CENTER_Y=61.125
recycle_scale=recycle_w/ART_WIDTH
recycle_profiles=[]
for contour in recycle_contours:
 pts=[(recycle_x-(px-ART_CENTER_X)*recycle_scale,recycle_y-(py-ART_CENTER_Y)*recycle_scale) for px,py in contour]
 recycle_profiles.append(Polygon(*pts,align=None))
recycle_profile=recycle_profiles[0]
for sk in recycle_profiles[1:]:
 recycle_profile+=sk
assert len(recycle_profile.faces())==6, 'All three fold slits must remain open'
recycle_cutter=Pos(0,0,outside_z-0.01)*extrude(recycle_profile,amount=recycle_depth+0.01)
symbol_removed=(body&recycle_cutter).volume
assert abs(symbol_removed-recycle_profile.area*recycle_depth)<1e-5
body-=recycle_cutter
assert len(body.solids())==1
print('Reference recycling ribbon regions / width / depth',len(recycle_profile.faces()),recycle_w,recycle_depth)
publish('back_cover',body,'01 开边胶接背盖')
