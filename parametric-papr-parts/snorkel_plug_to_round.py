from solid       import *
from solid.utils import *

def snorkel_plug_to_round(round_ID=None,round_OD=None, standoff_dist=None, rect_tube_thickness=1.4):
    '''Creates an object that adapts from a rectangular plug that can plug into a $BRANDNAME full face snorkel to a flat circle interface. One can then union a barb, universal tube adapter, etc onto the circle.
    
    round_ID = inner diameter of flat circle (annular, really) interface
    round_OD = outer diameter of flat circle (annular, really) interface
    '''

    plug_W = 16.2
    plug_H = 12.1 # measured and tested these in lab
    plug_D = 25

    epsilon = 0.001 # we use this for some bullshit where things are almost flat

    # first, if a standoff distance isn't provided, choose one that will guarantee an underhang angle of atmost 45 degree
    if standoff_dist==None:
        standoff_dist = abs( (round_OD/2) - 10 )  # 10mm: distance from center to corner of outer_rect

    # start building the chute, which transfers from circular to rectangle:
    
    outer_rect = up(standoff_dist) (cube([plug_W,plug_H,epsilon],center=True))
    inner_rect = up(standoff_dist) (cube([plug_W-2*rect_tube_thickness,plug_H-2*rect_tube_thickness,epsilon],center=True))

    outer_circle = cylinder(d=round_OD,h=epsilon)
    inner_circle = cylinder(d=round_ID,h=epsilon)

    outer_hull = hull() (outer_rect + outer_circle)
    inner_hull = hull() (inner_rect + inner_circle)

    chute = outer_hull - inner_hull

    # now build the rectangular plug:
    tower = up(standoff_dist) (
        up(plug_D/2) (
            cube([plug_W,plug_H,plug_D],center=True)
        )
    )

    chamfer_height = rect_tube_thickness
    # now construct the void in the center. (we'll use a hull to create the chamfer shape)
    tube_center = up(standoff_dist) (
        up( (plug_D+chamfer_height) /2  ) ( 
            cube([plug_W-2*rect_tube_thickness,plug_H-2*rect_tube_thickness,plug_D+chamfer_height],center=True)
        )
    )
    rectangular_plug = hull()(tower + tube_center) - tube_center
    return chute + rectangular_plug

    # note to readers -- from here to the end of the function is pure sleep-deprived bullshit. 
    # write it all over again if you have to
    # pyramid shape will sit ontop the plug, lets us make the chamfer

    #pyramid_H = 12
    #top_of_tower_height = standoff_dist+plug_D
    #pyramid = hull() (
    #    up(top_of_tower_height) (
    #        up(epsilon/2) (
    #            cube([plug_W,plug_H,epsilon],center=True)
    #        )
    #    )
    #    +
    #    up(top_of_tower_height+pyramid_H) ( # i just decided to make the pyramid this tall
    #        sphere(r=0.001)
    #    )
    #)

    ## now make a thing that will cut through all of it
    #cutter =  (
    #    # cuts thru center
    #    linear_extrude(100000) ( 
    #        square([plug_W-2*rect_tube_thickness,plug_H-2*rect_tube_thickness],center=True)
    #    )
    #    +
    #    up(top_of_tower_height) (
    #        up (rect_tube_thickness*pyramid_H*2 / max(plug_H,plug_W)) ( # do not ask me to explain this line. i'm on a tight deadline here!
    #            left(500) (
    #                back(500) (
    #                    cube([1000,1000,1000])
    #                )
    #            )
    #        )
    #    )
    #) 
    #rectangular_plug = (tower + pyramid) - cutter
    #return chute + rectangular_plug
    

def main():
    obj = snorkel_plug_to_round(10,12) 
    scad_render_to_file(obj,'scratch.scad')

if __name__=='__main__':
    main()
