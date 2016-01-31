import cx_Freeze

executables = [cx_Freeze.Executable("firstrl.py")]

cx_Freeze.setup(
    name="Jons Roguelike",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["fade.png", "sidefade.png", "thebase.png", "explosion.png", "poof.png", "rabbits.png", "charsheet.png", "foresttiles.png", "tilesetposx.txt", "tilesetposy.txt", "tilecollision.txt", "draw_over_player.txt", "special_collision_1.txt", "special_collision_2.txt", "special_collision_3.txt", "special_collision_4.txt", "tilecollisionv2.txt",
					 "map_L_one_1.txt", "map_L_one_1.1.txt", "map_L_one_1.2.txt", "map_L_one_1.3.txt", "map_L_one_2.txt", "map_L_one_3.01.txt", "map_L_one_3.1.txt", "map_L_one_3.02.txt", "map_L_one_3.2.txt", "map_L_one_3.03.txt", "map_L_one_3.txt", "map_L_one_4.1.txt", "map_L_one_4.2.txt", "map_L_one_4.txt",
					 "map_L_two_1.txt", "map_L_two_1.1.txt", "map_L_two_1.2.txt", "map_L_two_1.3.txt", "map_L_two_2.txt", "map_L_two_3.01.txt", "map_L_two_3.1.txt", "map_L_two_3.02.txt", "map_L_two_3.2.txt", "map_L_two_3.03.txt", "map_L_two_3.txt", "map_L_two_4.1.txt", "map_L_two_4.2.txt", "map_L_two_4.txt",
					 "map_L_three_1.txt", "map_L_three_1.1.txt", "map_L_three_1.2.txt", "map_L_three_1.3.txt", "map_L_three_2.txt", "map_L_three_3.01.txt", "map_L_three_3.1.txt", "map_L_three_3.02.txt", "map_L_three_3.2.txt", "map_L_three_3.03.txt", "map_L_three_3.txt", "map_L_three_4.1.txt", "map_L_three_4.2.txt", "map_L_three_4.txt"]}},
    executables = executables
    )
