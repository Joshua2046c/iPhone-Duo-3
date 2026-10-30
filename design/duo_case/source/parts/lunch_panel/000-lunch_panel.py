# cell: lunch_panel
# cell: lunch_panel
# Separate glue-on lunch panel. Local base is Z=0, assembled against the lid at world Z18.85.
front=part('front_cover')
t=0.0
w=front.w
h=front.h
lunch_x=front.glue_x
lunch_y=front.glue_y
whole_inset=param('lunch_panel_whole_inset',1.0)
base_rise=param('lunch_panel_platform_rise',3.5)
center_extra=param('lunch_panel_center_extra_rise',2.0)
rib_rise=param('lunch_panel_rib_relief',0.8)
edge_round=param('lunch_panel_platform_edge_radius',0.3)
lunch_rib_w=param('lunch_panel_rib_width',2.4)
lunch_rib_pitch=param('lunch_panel_rib_pitch',9.0)
height_scale=param('lunch_panel_height_scale',0.7)
step_extension=param('lunch_panel_step_extension',1.0)
lunch_w=front.glue_w-2*step_extension
lunch_h=front.glue_h-2*step_extension
lunch_r=front.glue_r-step_extension
recess_depth=param('lunch_panel_recess_depth',1.0)
recess_margin=param('lunch_panel_recess_margin',0.8)
recess_chamfer=param('lunch_panel_recess_chamfer',0.2)
text_size=param('lunch_panel_text_size',18.0)
text_raise=param('lunch_panel_text_raise',0.5)
text_angle=param('lunch_panel_text_angle',90.0)
terrace_rise=base_rise*height_scale
central_rise=(base_rise+center_extra)*height_scale
rib_height=rib_rise*height_scale
assert 0<recess_depth<central_rise and 0<text_raise<recess_depth
motif_w=lunch_w-2*whole_inset
motif_h=lunch_h-2*whole_inset
motif_r=lunch_r-whole_inset
assert 0<rib_rise<center_extra and base_rise>0
assert lunch_w+2*step_extension<w-6 and lunch_h+2*step_extension<h-6
def lunch_profile(ww,hh,rr,zz):
 return Pos(lunch_x,lunch_y,zz)*RectangleRounded(ww,hh,rr)
# Slightly tapered whole platform starts at the outermost striped frame boundary.
flange_root=lunch_profile(lunch_w+2*step_extension,lunch_h+2*step_extension,lunch_r+step_extension,t)
flange=loft([flange_root,
             lunch_profile(motif_w+2*step_extension,motif_h+2*step_extension,motif_r+step_extension,t+terrace_rise)])
flange=fillet(flange.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],radius=edge_round*height_scale)
# Rolled rim and short ribs sit on the raised platform.
outer_sk=RectangleRounded(motif_w-2,motif_h-2,motif_r-1)-RectangleRounded(motif_w-6,motif_h-6,motif_r-3)
outer=Pos(lunch_x,lunch_y,t+terrace_rise-0.1)*extrude(outer_sk,amount=rib_height+0.1)
outer=fillet(outer.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],radius=0.45*height_scale)
# Central frame height follows the 70 percent vertical reduction.
center=loft([lunch_profile(motif_w-10,motif_h-10,motif_r-2,t+terrace_rise-0.1),
             lunch_profile(motif_w-14,motif_h-14,motif_r-4,t+central_rise)])
center=fillet(center.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],radius=0.6*height_scale)
body=flange
body+=outer
body+=center
rib=extrude(SlotOverall(6.2,lunch_rib_w),amount=rib_height+0.1)
rib=fillet(rib.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1],radius=0.55*height_scale)
for side in (-1,1):
 for i in range(-4,5):
  body+=Pos(lunch_x+side*(motif_w/2-4.1),lunch_y+i*lunch_rib_pitch,t+terrace_rise-0.1)*rib
 for i in range(-2,3):
  body+=Pos(lunch_x+i*lunch_rib_pitch,lunch_y+side*(motif_h/2-4.1),t+terrace_rise-0.1)*Rot(0,0,90)*rib

# A true 0.8 mm planar land is measured from the actual rounded top edge.
central_top=[f for f in center.faces() if f.geom_type==GeomType.PLANE and abs(f.center().Z-(t+central_rise))<1e-6 and f.normal_at().Z>0.99]
assert len(central_top)==1
recess_mouth_profile=offset(central_top[0],amount=-recess_margin)
# Keep the visible 0.8 mm land by moving the vertical wall inward before beveling.
recess_profile=offset(central_top[0],amount=-(recess_margin+recess_chamfer))
recess_floor_z=t+central_rise-recess_depth
body-=extrude(recess_profile,amount=-recess_depth)
assert 0<recess_chamfer<min(recess_depth,recess_margin)
recess_rim_edges=[]
for edge in body.edges():
 bb=edge.bounding_box()
 if abs(bb.min.Z-(t+central_rise))<1e-6 and abs(bb.max.Z-(t+central_rise))<1e-6:
  if edge.distance_to(recess_profile.faces()[0].outer_wire())<1e-6:
   recess_rim_edges.append(edge)
assert len(recess_rim_edges)==8, 'Expected four straight and four rounded pocket-mouth edges'
body=chamfer(recess_rim_edges,length=recess_chamfer)
print('Pocket-mouth full-perimeter chamfer',recess_chamfer,'at 45 degrees; visible land remains',recess_margin)
# Songti SC from the installed macOS Songti family; no substitute font.
font_file="/System/Library/Fonts/Supplemental/Songti.ttc"
lettering=Text("降解餐盒",text_size,font="Songti SC",font_path=font_file,font_style=FontStyle.REGULAR)
letter_bb=lettering.bounding_box()
lettering=Pos(-(letter_bb.min.X+letter_bb.max.X)/2,-(letter_bb.min.Y+letter_bb.max.Y)/2)*lettering
lettering=Pos(lunch_x,lunch_y,recess_floor_z-0.01)*Rot(0,0,text_angle)*lettering
letters=extrude(lettering,amount=text_raise+0.01)
body+=letters
print('Height reduction',height_scale,'terrace',terrace_rise,'highest frame',central_rise)
print('Pocket depth',recess_depth,'actual planar border width',recess_margin,'local floor Z',recess_floor_z)
print('Outer step extension per side',step_extension,'text Songti SC / size / raise',text_size,text_raise)

assert len(body.solids())==1
assert abs(body.bounding_box().max.Z-(t+central_rise))<1e-6
print('Whole motif terrace rise',terrace_rise,'center additional rise',center_extra*height_scale,'center total rise',central_rise)
print('Whole footprint at root',lunch_w,lunch_h,'at terrace',motif_w,motif_h,'inset per side',whole_inset)
body.color=Color(0.80,0.015,0.055)
publish('lunch_panel',body,'06 饭盒粘合面片',material='petg')
