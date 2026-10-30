# cell: front_cover
# cell: front_cover
# Front cover and its coordinated decorative pocket interfaces.
w=param('front_cover_width',87.8)
h=param('front_cover_height',121.5)
t=param('front_cover_thickness',4.0)
r=param('front_cover_corner_radius',11.6)
reduction=param('front_cover_hinge_side_reduction',3.1)
inset=param('front_cover_extra_hinge_inset',1.0)
shift=(reduction+inset)/2
depth=param('front_cover_storage_depth',2.6)
storage_border=param('front_cover_storage_side_border',2.5)
storage_stop_x=shift+w/2-r
length=storage_stop_x-(shift-w/2)
height=param('front_cover_storage_height',85.4)
storage_y=param('front_cover_storage_y',13.7)
seat_l=param('front_cover_cap_seat_length',51.4)
seat_h=param('front_cover_cap_seat_height',90.6)
seat_depth=param('front_cover_cap_seat_depth',1.4)
seat_r=param('front_cover_cap_seat_radius',10.35)
seat_left_r=param('front_cover_cap_seat_left_radius',0.8)
bond_gap=param('front_cover_cap_bond_gap',0.2)
pin_d=param('front_cover_pin_diameter',2.4)
pin_x=param('front_cover_pin_x',-18.9)
pin_y1=param('front_cover_pin_y1',-25.0)
pin_y2=param('front_cover_pin_y2',25.0)
pin_tip=param('front_cover_pin_tip',1.3)
pin_long=param('front_cover_pin_longitudinal_length',7.4)
assert pin_long>pin_d

# Flat outer face; decorative inserts and their seats are removed.
corner_soft=param('front_cover_left_corner_radius',1.0)
outline=Pos(shift,0)*(RectangleRounded(w,h,r)+Pos(-w/4,0)*Rectangle(w/2,h))
left_vertices=[v for v in outline.vertices() if abs(v.X+w/2-shift)<1e-6]
assert len(left_vertices)==2
outline=fillet(left_vertices,radius=corner_soft)
body=extrude(outline,amount=t)
# Integral side tab aligned to the retained rear wall between its two side openings.
# Height is measured from the front cover's inner rim plane (local Z=0), toward the back.
back=part('back_cover')
side_tab_h=param('front_cover_side_tab_height',5.9)
side_tab_t=param('front_cover_side_tab_thickness',1.6)
side_tab_y_min=back.shutter_y+back.shutter_l/2+back.turn
side_tab_y_max=back.power_y-back.power_l/2-back.turn
side_tab_w=side_tab_y_max-side_tab_y_min
side_tab_y=(side_tab_y_min+side_tab_y_max)/2
side_tab_outer_x=shift+w/2
# Four side-profile rounds match the rear wall: concave at the root, convex at the tip.
side_tab_r=back.turn
side_tab_edge_r=back.opening_soft
tab_profile=Pos(side_tab_y,-side_tab_h/2)*Rectangle(side_tab_w,side_tab_h)
tip_vertices=[v for v in tab_profile.vertices() if abs(v.Y+side_tab_h)<1e-6]
assert len(tip_vertices)==2
tab_profile=fillet(tip_vertices,radius=side_tab_r)
for end,sign in ((side_tab_y_min,-1),(side_tab_y_max,1)):
 root_square=Pos(end+sign*side_tab_r/2,-side_tab_r/2)*Rectangle(side_tab_r,side_tab_r)
 root_disk=Pos(end+sign*side_tab_r,-side_tab_r)*Circle(side_tab_r)
 tab_profile+=root_square-root_disk
side_tab=Pos(side_tab_outer_x-side_tab_t,0,0)*extrude(Plane.YZ*tab_profile,amount=side_tab_t)
body+=side_tab
print('Side tab four profile rounds',side_tab_r,'outside edge roll',side_tab_edge_r)
assert abs(side_tab_w-17.2)<1e-6
assert abs(body.bounding_box().min.Z+side_tab_h)<1e-6
print('Integral front side tab height',side_tab_h,'width matched to rear wall',side_tab_w,'Y range',side_tab_y_min,side_tab_y_max,'wall thickness',side_tab_t)



# Matching blind magnet pocket opens from the downward-facing tip toward the front cover.
closing_mag_l=back.closing_mag_l
closing_mag_w=back.closing_mag_w
closing_mag_d=back.closing_mag_d
closing_mag_wall=back.closing_mag_wall
closing_mag_floor=back.closing_mag_floor
closing_mag_x=back.closing_mag_x
closing_mag_y=back.closing_mag_y
closing_mag_boss_w=back.closing_mag_boss_w
closing_mag_boss_l=back.closing_mag_boss_l
closing_mag_boss_h=t+side_tab_h
closing_mag_mouth=-side_tab_h
closing_mag_boss=Pos(0,0,closing_mag_mouth)*extrude(back.closing_mag_fair_profile,amount=closing_mag_boss_h)
# Continue the original R1 side silhouette through the extended carrier ends.
closing_mag_side_profile=tab_profile+Pos(side_tab_y,t/2)*Rectangle(side_tab_w+2*side_tab_r,t)
closing_mag_end_mask=Pos(back.closing_mag_inner_x-1,0,0)*extrude(Plane.YZ*closing_mag_side_profile,amount=closing_mag_boss_w+2)
closing_mag_boss &= closing_mag_end_mask
body+=closing_mag_boss
# Match the lower shell's small outer edge roll around the rounded tab outline.
tab_outer_edges=[]
for edge in body.edges():
 bb=edge.bounding_box()
 on_original_side=abs(bb.min.X-side_tab_outer_x)<1e-6 and abs(bb.max.X-side_tab_outer_x)<1e-6 and bb.min.Z<-1e-6 and bb.max.Z<1e-6
 at_new_tip=abs(bb.min.Z+side_tab_h)<1e-6 and abs(bb.max.Z+side_tab_h)<1e-6 and bb.max.X>side_tab_outer_x+1e-6
 if (on_original_side or at_new_tip) and bb.min.Y>=side_tab_y_min-side_tab_r-1e-6 and bb.max.Y<=side_tab_y_max+side_tab_r+1e-6:
  tab_outer_edges.append(edge)
assert len(tab_outer_edges) in (9,11), 'Expected rounded side tab outer U perimeter'
body=fillet(tab_outer_edges,radius=side_tab_edge_r)


# User-marked external rim on the decorative face, not the internal seating step.
outer_round=param('front_cover_outer_rim_radius',0.8)
rim_edges=[]
for edge in body.edges():
 bb=edge.bounding_box()
 at_outer_face=abs(bb.min.Z-t)<1e-6 and abs(bb.max.Z-t)<1e-6
 on_hinge=abs(bb.min.X-(shift-w/2))<1e-6 and abs(bb.max.X-(shift-w/2))<1e-6
 if at_outer_face and not on_hinge:
  rim_edges.append(edge)
assert len(rim_edges) in (11,15), 'Expected one continuous outer rim including the fairing'
body=fillet(rim_edges,radius=outer_round)
print('Front external rim radius',outer_round,'selected perimeter edges',len(rim_edges))
# Full inset cover seat, matching the asymmetrical outline.
seat=Pos(shift,0)*(RectangleRounded(seat_l,seat_h,seat_r)+Pos(-seat_l/4,0)*Rectangle(seat_l/2,seat_h))
seat=fillet([v for v in seat.vertices() if abs(v.X+seat_l/2-shift)<1e-6],radius=seat_left_r)
# Open the full hinge-side seating edge instead of leaving the painted narrow strip.
hinge_seat_open=param('front_cover_hinge_seat_open',True)
if hinge_seat_open:
 hinge_cut_left=shift-w/2-1
 hinge_cut_right=shift-seat_l/2+seat_left_r
 seat+=Pos((hinge_cut_left+hinge_cut_right)/2,0)*Rectangle(hinge_cut_right-hinge_cut_left,seat_h)
# Matching hinge-end pads at both ends, flush with the retainer's visible face.
end_pad_raise=param('front_cover_hinge_end_pad_raise',1.4)
assert 0<=end_pad_raise<=seat_depth
strip_width=(w-seat_l)/2
pad_height=seat_h/2-(height/2-storage_y)
assert pad_height>0
pad_x=shift-w/2+strip_width/2
pad_y=seat_h/2-pad_height/2
pad_profile=Pos(pad_x,-pad_y)*Rectangle(strip_width,pad_height)+Pos(pad_x,pad_y)*Rectangle(strip_width,pad_height)
seat_cut=extrude(seat,amount=seat_depth)
if end_pad_raise>0:
 seat_cut-=Pos(0,0,seat_depth-end_pad_raise-0.01)*extrude(pad_profile,amount=end_pad_raise+0.02)
body-=seat_cut
print('Both hinge pads floor local Z',seat_depth-end_pad_raise,'footprint',strip_width,pad_height)
# Recess stays open at the hinge only at the sheet's sliding height.
mouth_floor=seat_depth-bond_gap
# The far-side recess ends at the large outer corner's tangent (R end).
# Material beyond this boundary remains at seat_depth, coplanar with the adjacent step.
# The storage opening has a continuous boundary without internal magnet supports.
assert 0<storage_border<r and height<h
storage_profile=offset(outline,amount=-storage_border)
hinge_ext_left=shift-w/2-1
hinge_ext_right=shift-w/2+storage_border+1
storage_profile+=Pos((hinge_ext_left+hinge_ext_right)/2,storage_y)*Rectangle(hinge_ext_right-hinge_ext_left,height)
storage_profile &= Pos(shift-w/2+(length-1)/2,storage_y)*Rectangle(length+1,height)
# Round only the two marked planar corners of the deep storage opening.
storage_corner_r=param('front_cover_storage_corner_radius',3.0)
storage_corners=[v for v in storage_profile.vertices() if abs(v.X-storage_stop_x)<1e-6 and abs(abs(v.Y-storage_y)-height/2)<1e-6]
assert len(storage_corners)==2, 'Expected the two marked far-side storage corners'
area_before=storage_profile.area
storage_profile=fillet(storage_corners,radius=storage_corner_r)
expected_loss=2*(1-3.141592653589793/4)*storage_corner_r**2
assert abs(area_before-storage_profile.area-expected_loss)<1e-5, 'Corner rounding must affect exactly two quarter circles'
print('Storage planar corner radius',storage_corner_r,'count',len(storage_corners),'opening area removed',area_before-storage_profile.area)
# Capacity only: the complete developed free segment and tail fit the open cavity in XY.
# Fixed guide travel is an independent constraint; passing this does not prove retraction.
shield=part('spine')
packed_length=shield.free_l+shield.tail_l
packed=Pos(shift-w/2+packed_length/2,storage_y)*Rectangle(packed_length,shield.tail_h)
assert abs((storage_profile&packed).area-packed.area)<1e-5, 'Cavity cannot contain the complete free sheet footprint'
print('Complete free sheet XY capacity fits',packed_length,shield.tail_h,'guide travel is separate')
body-=Pos(0,0,mouth_floor)*extrude(storage_profile,amount=depth-mouth_floor)
print('Storage reach from hinge',length,'corner tangent X',storage_stop_x,'height',height,'end border',(h-height)/2)
print('Far side raised by',depth-seat_depth,'to seat local Z',seat_depth,'outer tangent band',r)
# Check solid support across the uninterrupted raised side.
raised_probe_right=shift+w/2-storage_border
raised_probe=Pos((storage_stop_x+raised_probe_right)/2,0,(seat_depth+depth)/2)*Box(raised_probe_right-storage_stop_x,2*storage_corner_r,depth-seat_depth)
assert abs((body&raised_probe).volume-raised_probe.volume)<1e-5, 'Far side was not raised to the step'

for yy in (pin_y1,pin_y2):
 body+=Pos(pin_x,yy,pin_tip)*extrude(SlotOverall(pin_long,pin_d,rotation=90),amount=depth+0.05-pin_tip)
if hinge_seat_open:
 strip_width=(w-seat_l)/2
 strip_profile=Pos(shift-w/2+strip_width/2,0)*Rectangle(strip_width,seat_h)
 probe=extrude(strip_profile-pad_profile,amount=mouth_floor)
 assert (body&probe).volume<1e-6, 'Hinge-side narrow strip remains'
 print('Removed hinge seating strip width',strip_width,'Y extent',seat_h)

closing_mag_cut=Pos(closing_mag_x,closing_mag_y,closing_mag_mouth+closing_mag_d/2-0.005)*Box(closing_mag_w,closing_mag_l,closing_mag_d+0.01)
closing_mag_removed=(body&closing_mag_cut).volume
assert abs(closing_mag_removed-closing_mag_l*closing_mag_w*closing_mag_d)<1e-6
body-=closing_mag_cut
closing_mag_support=Pos(closing_mag_x,closing_mag_y,closing_mag_mouth+closing_mag_d+closing_mag_floor/2)*Box(closing_mag_w,closing_mag_l,closing_mag_floor)
assert abs((body&closing_mag_support).volume-closing_mag_support.volume)<1e-6
print('Upper closing magnet L/W/D',closing_mag_l,closing_mag_w,closing_mag_d,'XY center',closing_mag_x,closing_mag_y,'local mouth/floor Z',closing_mag_mouth,closing_mag_mouth+closing_mag_d)


# Shared glue footprint; the separate lunch panel reads these dimensions.
glue_w=param('front_cover_glue_footprint_width',76.0)
glue_h=param('front_cover_glue_footprint_height',113.0)
glue_r=param('front_cover_glue_footprint_radius',12.0)
glue_x=param('front_cover_glue_footprint_x',2.05)
glue_y=param('front_cover_glue_footprint_y',0.0)
guide_width=param('front_cover_glue_guide_width',0.25)
guide_depth=param('front_cover_glue_guide_depth',0.08)
glue_outline=Pos(glue_x,glue_y)*RectangleRounded(glue_w,glue_h,glue_r)
guide_ring=offset(glue_outline,amount=guide_width/2)-offset(glue_outline,amount=-guide_width/2)
body-=Pos(0,0,t-guide_depth)*extrude(guide_ring,amount=guide_depth+0.01)
assert t-depth-guide_depth>=1.3
assert len(body.solids())==1
print('Glue guide width/depth',guide_width,guide_depth,'nominal footprint',glue_w,glue_h)
body.color=Color(0.80,0.015,0.055)
publish('front_cover',body,'04 定位线面盖',material='petg')
