from solid import *
from solid.utils import *
from universal_tube_adapter import universal_tube_adapter
from settings_library import *
hose_barb = import_scad('assets/hose_barb.scad')

def tube_to_barb_adapter(tube_ID=None, tube_thick=None, tube_len=None, chamfer_in=0, chamfer_out=0, hose_od = None, hose_id = None, swell = None, barb_wall_thickness = None,barb_length = None, barbs = None , segments=180 ):
    '''
    adapts 

    arguments:
    tube_ID : inner diameter of tube on the side that isn't the barb
    tube_thick : wall thickness of tube on the side that isn't the barb
    tube_len : length of tube on the side that isn't the barb
    chamfer_in : optional, height of chamfer on inner rim of side that isn't the barb
    chamfer_out : optional, height of chamfer on inner rim of side that isn't the barb

    hose_od : outer diameter of vinyl hose we're creating the barb for 
    hose_id : inner diameter of vinyl hose we're creating the barb for 


    '''


    # first create the barb object.
    # this uses OpenSCAD code I found at https://www.thingiverse.com/thing:2990340
    barb = hose_barb.barb(hose_od = hose_od, hose_id = hose_id, swell = swell, barb_wall_thickness = barb_wall_thickness, barbs = barbs, barb_length = barb_length, shell = True, bore = True, ezprint=False)
    barb.add_param('$fn',segments)

    # now create the tube that adapts out of it
    # first have to calculate what ID to give it
    # the OD of the tube part of the barb part is hose_id
    barb_ID = hose_id - 2* barb_wall_thickness

    # we also need to calculate what length of transition region will give us approx 45 degree cone
    transition_len = abs(tube_ID-barb_ID)/2

    adapter = universal_tube_adapter(ID1=barb_ID, t1=barb_wall_thickness, h1=0, hmid=transition_len, ID2=tube_ID,t2=tube_thick,h2=tube_len,c1_in=0,c1_out=0,c2_in=chamfer_in,c2_out=chamfer_out,segments=segments)

    return barb + adapter

def main():
    # adapt from flextailgear blower to half inch ID vinyl
    # obj = tube_to_barb_adapter(**flextail_output_dims, **half_inch_barb_dims) 

    # adapt from half inch vinyl hose to Jeff's "buck" mask
    obj = tube_to_barb_adapter(**flextail_output_dims_thicker, **very_flexible_hose_barb_dims) 

    scad_render_to_file(obj,'scratch.scad')

if __name__=='__main__':
    main()
