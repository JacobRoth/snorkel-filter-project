# this file is just a place to put settings for various connections that go into various functions!

# the dimension settings for a half inch ID, three-quarter inch OD vinyl hose
half_inch_barb_dims = {
    'hose_od':0.75*25.4, 
    'hose_id':0.5*25.4, 
    'swell':1.75, 
    'barb_length':4, 
    'barb_wall_thickness':1.4,
    'barbs':3
}
one_inch_barb_dims = { # modeled off the plastic ones
    'hose_od':1.5*25.4, 
    'hose_id':25.4, 
    'swell':1, 
    'barb_length':10, 
    'barb_wall_thickness':2.4,
    'barbs':2
}
very_flexible_hose_barb_dims = {
    'hose_od':1.5*25.4, 
    'hose_id':25.4, 
    'swell':2.25, 
    'barb_length':10, 
    'barb_wall_thickness':2.4,
    'barbs':2
}
# the dimension settings for the output of the flextailgear blower:
flextail_output_dims = {
    'tube_ID':20.5, 
    'tube_thick':2,
    'tube_len':7.92, 
    'chamfer_in':.66
}
flextail_output_dims_thicker = {
    'tube_ID':20.5, 
    'tube_thick':5,
    'tube_len':7.92, 
    'chamfer_in':.66
}
# dimension settings for fitting Jeff's "buck" mask
buck_intake_dims = {
    'tube_ID':34.65,
    'tube_thick':3.5,
    'tube_len':10, 
    'chamfer_in':.66
}

