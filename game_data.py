level_0 = {
    'terrain':'Tiled/Levels/0/Level_0_terrain.csv',
    'player':'Tiled/Levels/0/Level_0_player.csv',
    'coins':'Tiled/Levels/0/Level_0_coins.csv',
    'constraints':'Tiled/Levels/0/Level_0_constraints.csv',
    'crates':'Tiled/Levels/0/Level_0_crates.csv',
    'enemies':'Tiled/Levels/0/Level_0_enemies.csv',
    'fg_palm':'Tiled/Levels/0/Level_0_fg_palm.csv',
    'node_pos':(250,360),
    'unlock':1,
    'node_graphics':'Assets/overworld/0'
}

level_1 = {
    'terrain':'Tiled/Levels/1/Level_1_terrain.csv',
    'player':'Tiled/Levels/1/Level_1_player.csv',
    'coins':'Tiled/Levels/1/Level_1_coins.csv',
    'constraints':'Tiled/Levels/1/Level_1_constraints.csv',
    'crates':'Tiled/Levels/1/Level_1_crates.csv',
    'enemies':'Tiled/Levels/1/Level_1_enemies.csv',
    'fg_palm':'Tiled/Levels/1/Level_1_fg_palm.csv',
    'node_pos':(730,750),
    'unlock':2,
    'node_graphics':'Assets/overworld/1'
}


#make more levels and export using tiled
#level_2 = {
#    'terrain':'Tiled/Levels/0/Level_0_terrain.csv',
#    'player':'Tiled/Levels/0/Level_0_player.csv',
#    'coins':'Tiled/Levels/0/Level_0_coins.csv',
#    'constraints':'Tiled/Levels/0/Level_0_constraints.csv',
#    'crates':'Tiled/Levels/0/Level_0_crates.csv',
#    'enemies':'Tiled/Levels/0/Level_0_enemies.csv',
#    'fg_palm':'Tiled/Levels/0/Level_0_fg_palm.csv',
#    'node_pos':(1200,300),
#    'unlock':2,
#    'node_graphics':'Assets/overworld/2'
#}

level_2 = {
    'terrain':'Tiled/Levels/2/Level_2_terrain.csv',
    'player':'Tiled/Levels/2/Level_2_player.csv',
    'coins':'Tiled/Levels/2/Level_2_coins.csv',
    'constraints':'Tiled/Levels/2/Level_2_constraints.csv',
    'crates':'Tiled/Levels/2/Level_2_crates.csv',
    'enemies':'Tiled/Levels/2/Level_2_enemies.csv',
    'fg_palm':'Tiled/Levels/2/Level_2_fg_palm.csv',
    'node_pos':(1200,300),
    'unlock':2,
    'node_graphics':'Assets/overworld/2'
}

level_0_overworld = {'node_pos':(250,360),
                     'content':'level 0',
                     'unlock':1}
level_1_overworld = {'node_pos':(730,750),
                     'content':'level 1',
                     'unlock':2}
level_2_overworld = {'node_pos':(1200,300),
                     'content':'level 2',
                     'unlock':2}

levels = {
    0: level_0,
    1: level_1,
    2: level_2,
}