from solid       import *
from solid.utils import *

def universal_tube_adapter(ID1=None, t1=None, h1=None, hmid=None, ID2=None,t2=None,h2=None,c1_in=0,c1_out=0,c2_in=0,c2_out=0,segments=180,minthick=False):
    '''constructs a tube adapter from specified inner diameters, lengths, and thicknesses; consult the drawing to understand what the dimensional arguments do. Optional parameter minthick (not implemented yet) will invoke some clever tricks to guarantee that the thickness of the transition region is at least min(t1,t2) at all points, but requires the two tubes on either side are longer than min(t1,t2). The parameters c1_in through c2_out control the size of chamfers on the insides and outsides of the tubes.
    '''

    # first construct the inside of the shape.
    inner_profile = polygon(points = [
        [0     , 0]
        ,[ID1/2, 0]
        ,[ID1/2, h1]
        ,[ID2/2, h1+hmid]
        ,[ID2/2, h1+hmid+h2]
        ,[0    , h1+hmid+h2]
    ])

    # constructing the outer profile is harder. We have to do some clever bullshit to maintain minimum thickness.
    # first the tubes on either end:
    tube1_profile = square([(ID1/2)+t1, h1])
    tube2_profile = forward(h1+hmid) (
                        square([(ID2/2)+t2, h2])
                    )

    # now the tricky part: transition profile. constructed from the hull of two semicircles, then cropped
    semicircle1 = right(ID1/2) (
                    forward(h1) (
                        arc(rad=t1,start_degrees=0,end_degrees=180,segments=segments)
                    )
                  )
    semicircle2 = right(ID2/2) (
                    forward(h1+hmid) (
                        arc(rad=t2,start_degrees=180,end_degrees=360,segments=segments)
                    )
                  )

    hulled_shape = hull() (semicircle1 + semicircle2)
    # must confine this to the bounding box of the transition region.
    transition_profile = intersection() (
        hulled_shape,
        forward(h1) (
            square([ max( (ID1/2)+t1 , (ID2/2)+t2) , hmid])
        )
    )

    # assemble the outer profile
    outer_profile = tube1_profile+tube2_profile+transition_profile
    
    # get the general profile of the object
    overall_profile = outer_profile - inner_profile

    # now construct and apply the chamfers
    chamfer1_in = polygon(points= [
        [ID1/2,0]
        ,[(ID1/2)+c1_in,0]
        ,[ID1/2,c1_in]
    ])
    chamfer1_out = polygon(points= [
        [(ID1/2)+t1-c1_out , 0]
        ,[(ID1/2)+t1 , 0]
        ,[(ID1/2)+t1 , c1_out]
    ])
    fullheight = h1+h2+hmid
    chamfer2_in = polygon(points= [
        [(ID2/2) , fullheight - c2_in]
        ,[(ID2/2) + c2_in , fullheight ]
        ,[(ID2/2) , fullheight ]
    ])
    chamfer2_out = polygon(points= [
        [(ID2/2) + t2 , fullheight]
        ,[(ID2/2) + t2 - c2_out , fullheight ]
        ,[(ID2/2) + t2 , fullheight - c2_out]
    ])

    chamfered_profile = overall_profile - chamfer1_in - chamfer1_out - chamfer2_in - chamfer2_out

    # now revolve and make the shape 
    return rotate_extrude(segments=segments)( chamfered_profile) 

test_cases = [
    [2,2,2,1,5,1,5]
    ,[0,0,0,0,0,0,0]
    ,[2,1,1,0,0,0,0]
    ,[2,1,1,1,0,0,0]
    ,[2,1,1,1,0.01,0.01,0.01]
    ,[0.01,0.01,0.01,1,2,1,1]
    ,[5   ,5,2,30,60,1,4]
    ,[5   ,5,2,30,60,1,0]
    ,[5   ,5,2,30,60,1,4,2,.5]
    ,[5   ,5,2,30,60,1,4,2,.5,.3,0]
]

def main():
    obj = universal_tube_adapter(*test_cases[-1])
    scad_render_to_file(obj,'scratch.scad')

if __name__=='__main__':
    main()
