from solid import *
from solid.utils import *
from settings_library import *
from snorkel_plug_to_round import snorkel_plug_to_round
#from tube_to_barb_adapter import  *
hose_barb = import_scad('assets/hose_barb.scad')

def snorkel_plug_to_barb(hose_od = None, hose_id = None, swell = None, barb_wall_thickness = None,barb_length = None, barbs = 3 , segments=180 ):
    ''' create an adapter that adapts from the $BRANDNAME snorkel to a hose barb of your choice.

    TODO: this docstring

    '''

    barb = hose_barb.barb(hose_od = hose_od, hose_id = hose_id, swell = swell, barb_wall_thickness = barb_wall_thickness, barbs = barbs, barb_length = barb_length, shell = True, bore = True, ezprint=False)
    barb.add_param('$fn',segments)
    
    barb_OD = hose_id
    barb_ID = barb_OD - 2* barb_wall_thickness
    plug = snorkel_plug_to_round(round_ID=barb_ID,round_OD=barb_OD, standoff_dist=None, rect_tube_thickness=1.4)

    return barb + plug


def main():
    obj = snorkel_plug_to_barb( **very_flexible_hose_barb_dims) 

    scad_render_to_file(obj,'scratch.scad')

if __name__=='__main__':
    main()
    
