class ObjectDescription():
    def __init__(self, file_name, description):
        self.file_name = file_name
        self.description = description

OBJECTS_TO_TRAIN_DISSASSEMBLER = [
    ObjectDescription("baking_mold_1", "A rectangular baking mold"),
    ObjectDescription("ball_1", "A ball"),
    ObjectDescription("bottle_1", "A bottle with a narrow neck"),
    ObjectDescription("bowl_1", "A rounded bowl"),
    ObjectDescription("bowl_2", "A bowl"),
    ObjectDescription("box_1", "A rectangular box that expands slightly upwards"),
    ObjectDescription("box_2", "A box with a lid with an hemisphere handle"),
    ObjectDescription("cooking_pot_1", "A Cooking pot"),
    ObjectDescription("cooking_pot_2", "A 10 cm high cooking pot without a lid"),
    ObjectDescription("cup_1", "A capuccino cup"),
    # ObjectDescription("ellipse_baking_mold_1", "An oval-shaped baking dish with a half-pipe-shaped border around the body of the dish"),
    ObjectDescription("flower_pot_1", "A round flower pot that expands upwards with protruding edges and with a perforated bottom"),
    ObjectDescription("glass_1", "A 30 cm high glass"),
    ObjectDescription("hook_1", "S shape hook with rounded caps"),
    ObjectDescription("jar_1", "A jar"),
    ObjectDescription("jar_2", "A jar with side handle"),
    ObjectDescription("kettle_1", "A kettle"),
    ObjectDescription("kettle_2", "Alessi Kettle Plisse"),
    ObjectDescription("ladle_1", "A ladle"),
    ObjectDescription("lampshade_1", "A lampshade in a shape of hemisphere"),
    ObjectDescription("lampshade_2", "A table lamp in the shape of an elongated semicircle with a round base and a leg that connects between the base and the lamp"),
    ObjectDescription("measuring_jug_1", "A measuring jug"),
    ObjectDescription("mug_1", "A mug"),
    ObjectDescription("mug_2", "A mug with a rounded body, narrow base, and rim that expands toward the middle. The handle is large and C-shaped, providing a comfortable grip"),
    ObjectDescription("pan_1", "A pan with radius of 20cm and long handle"),
    ObjectDescription("plate_1", "A plate"),
    ObjectDescription("round_baking_mold_1", "A circle-shaped baking pan"),
    ObjectDescription("salt_shaker_1", "A salt shaker in a rounded shape and perforated lid."),
    ObjectDescription("soup_plate_1", "A soup plate with a rounded rim"),
    ObjectDescription("teapot_1", "A teapot"),
    ObjectDescription("toothbrush_holder_cup_1", "Toothbrush holder cup in a shape of cylinder with preforated bottom"),
    ObjectDescription("toothpick_dispenser_1", "Toothpick dispenser in a round shape with a perforated upper lid"),
    ObjectDescription("vase_1", "A spherical vase with narrow neck"),
    ObjectDescription("vase_2", "A vase with narrow neck and 2 handles at both sides"),
    ObjectDescription("vase_3", "A rounded vase with a pleated surface. The very bottom part of the vase is smooth circle"),
    ObjectDescription("wine_glass_1", "A Wine glass")    
]

OBJECTS_TO_TRAIN_CODE_WRITER = [
    ObjectDescription("baking_mold_1", "A rectangular baking mold"),
    ObjectDescription("bottle_1", "A bottle with a narrow neck"),
    ObjectDescription("bowl_2", "A bowl"),
    ObjectDescription("box_1", "A rectangular box that expands slightly upwards"),
    ObjectDescription("ellipse_baking_mold_1", "An oval baking dish"),
    ObjectDescription("flower_pot_1", "A round flower pot that expands upwards with protruding edges and with a perforated bottom"),
    ObjectDescription("glass_1", "A 30 cm high glass"),
    ObjectDescription("hook_1", "S shape hook with rounded caps"),
    ObjectDescription("plate_1", "A plate"),
    ObjectDescription("toothpick_dispenser_1", "Toothpick dispenser in a round shape with a perforated upper lid")
]

OBJECTS_TO_TRAIN_FULL_PROGRAM = [
    ObjectDescription("baking_mold_1", "A rectangular baking mold"),
    ObjectDescription("bottle_1", "A bottle with a narrow neck"),
    ObjectDescription("bowl_2", "A bowl"),
    ObjectDescription("box_1", "A rectangular box that expands slightly upwards"),
    ObjectDescription("ellipse_baking_mold_1", "An oval baking dish"),
    ObjectDescription("flower_pot_1", "A round flower pot that expands upwards with protruding edges and with a perforated bottom"),
    ObjectDescription("glass_1", "A 30 cm high glass"),
    ObjectDescription("hook_1", "S shape hook with rounded caps"),
    ObjectDescription("plate_1", "A plate"),
    ObjectDescription("toothpick_dispenser_1", "Toothpick dispenser in a round shape with a perforated upper lid")
]


# vase
# capuccino cap
# different handles
# 
