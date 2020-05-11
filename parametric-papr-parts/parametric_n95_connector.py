from solid import *
from solid.utils import *
from universal_tube_adapter import universal_tube_adapter

def parametric_n95_connector(tube_ID=None, tube_thick=None, tube_len=None,chamfer_in=0,chamfer_out=0,segments=180):
    '''cone-shaped object with the flange pattern for Daryl's N95 holder (assets/PAPR_BlowerConnect_3_Flange.DXF) on one end and on the other a tube of specified length, inner diameter, and wall thickness, with optional chamfers on the inside and/or outside'''
    if (tube_ID==None) or (tube_thick==None) or (tube_len==None):
        raise ValueError('missing required dimension')

    # import the flange as a SCAD object:
    flange_height = 4 #as found on Daryl's base part
    flange = linear_extrude(flange_height) (  
        import_('assets/PAPR_BlowerConnect_3_Flange.DXF',convexity=20,layer='0') 
    )
    flange.add_param('$fn',segments) # set the segments on the flange to get smooth curves out of the DXF import

    # then make the tube:
    cone_ID = 97.29 
    flange_thickness=15.1  # these two taken from flange drawing
    cone_height = cone_ID/2 # make it a 45 degree angle at the shallowest (aids printing, ensures thickness)


    tube_adapter = universal_tube_adapter(ID1=tube_ID, t1=tube_thick, h1=tube_len, hmid=cone_height, ID2=cone_ID,t2=flange_thickness,h2=0,c2_in=chamfer_in,c2_out=chamfer_out,segments=segments)

    adapter_height = cone_height+tube_len

    # finally, move the flange into position and union it to the cone.:
    return up(adapter_height)(flange) + tube_adapter


def main():
    obj = parametric_n95_connector(21,14,3) # adapts to the flextailgear blower
    scad_render_to_file(obj,'scratch.scad')

if __name__=='__main__':
    main()
