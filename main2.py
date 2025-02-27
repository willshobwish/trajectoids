import viewscad
r = viewscad.Renderer(openscad_exec="openscad")
#@title ## ↓↓↓ Press this button after setting the parameters below. Be patient: execution can take several minutes.

#@markdown ### Parameters of the trajectoid shape to be generated (leave them at default values if you are going to use 1"-diameter steel ball as an insert):

#@markdown Diameter of inner cavity in millimeters (e.g. diameter of your ball bearing):
diameter_of_inner_cavity = '25'#@param {type:"string"}

#@markdown Minimum diameter of trajectoid in millimeters (corresponds to value of 2r in the research article):
min_diameter_of_trajectoid = '40' #@param {type:"string"}

#@markdown Maximum diameter of trajectoid in millimeters (corresponds to value of 2R in the research article):
max_diameter_of_trajectoid = '50' #@param {type:"string"}
number_of_boxes=298
cavity_r = float(diameter_of_inner_cavity)/float(min_diameter_of_trajectoid)
outer_geosphere_R = float(max_diameter_of_trajectoid)/float(min_diameter_of_trajectoid)
# print(f'r: {cavity_r}, R: {outer_geosphere_R}')

trajectoid_oscad = """masterscale=$masc;

module cutter_cube(i) {
    import(str("C:/Users/Willian Murayama/github/trajectoids/test/cut_meshes/test_",i,".stl"));
}

module geosphere(radius) {
    scale([radius, radius, radius]) import("C:/Users/Willian Murayama/github/trajectoids/unit_geosphere.stl");
}

module cube_for_halving() {
    translate([-10,0,-10]) cube(size = [20, 20, 20], center = false);
}

scale([masterscale, masterscale, masterscale]) difference() {
    geosphere(radius=$outergeorad);
    geosphere(radius=$innergeorad);
    cube_for_halving();
    for (i =[0:$numberofboxes]) cutter_cube(i);
    // cutter_cube(0);
    // cutter_cube(189);
}
""".replace('$numberofboxes', str(number_of_boxes))\
.replace('$innergeorad', str(cavity_r))\
.replace('$outergeorad', str(outer_geosphere_R))\
.replace('$masc', str(float(min_diameter_of_trajectoid)/2))

print('Calculating the left half of the shape...')
r.render(trajectoid_oscad, outfile='trajectoid_half_left.stl')

print('Calculating the right half of the shape...')
r.render(trajectoid_oscad.replace('translate([-10,0,-10])',
                                  'translate([-10,-20,-10])'),
         outfile='trajectoid_half_right.stl')

print("Execution finished.")