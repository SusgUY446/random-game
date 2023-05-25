from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

chat_input = InputField(position=(-0.45, -0.45))

#scalechat
chat_input.scale=(0.5, 0.05)
# Textbereich für die Chat-Nachrichten
chat_output = Text(position=(-0.45, 0.45), scale=(0.5, 0.4), background=True)
#chat vivible (default:false)
chat_visible = False
#last time the chat was visible
last_chat_visible_time = 0

def teleport_player():
    player.position = (0, 0, 0)

def update():
    if player.y < -10:
        teleport_player()

        global chat_visible, last_chat_visible_time

    # Prüfe, ob die Taste "T" gedrückt wird, um den Chat sichtbar zu machen
    if held_keys['t']:
        chat_visible = True
        last_chat_visible_time = time.time()
        chat_input.active = True

    # Prüfe, ob der Chat nach 10 Sekunden unsichtbar gemacht werden soll
    if chat_visible and time.time() - last_chat_visible_time >= 10:
        chat_visible = False

    # Aktualisiere die Sichtbarkeit des Chats basierend auf dem chat_visible-Status
    chat_input.enabled = chat_visible
    chat_output.enabled = chat_visible

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.lime,
        )





def generate_world():
    for z in range(10):
        for x in range(10):
            for y in range(10):
                voxel = Voxel(position=(x,y,z))
generate_world()

def input(key):
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)
    if key == 'right mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)
    if key== 'escape':
        print("application.quit...")
        application.quit()

def send_chat_message():
    message = chat_input.text.strip()
    if message:
        chat_output.text += '\n' + message
        chat_input.text = ''


def handle_input(key):
    if key == 'enter':
        send_chat_message()

# Binde die Methode `handle_input()` an den Event-Handler für die Eingabe von Zeichenketten
chat_input.on_submit = handle_input

spawn_position = Vec3(10, 10, 10)

player = FirstPersonController()
player.position = spawn_position
app.run()
