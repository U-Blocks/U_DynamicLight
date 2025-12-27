import json
import math
import os

from binarystream import BinaryStream

from endstone_u_dynamic_light.lang import load_lang

from endstone import Player, ColorFormat

from endstone.plugin import Plugin
from endstone.level import Dimension
from endstone.form import ModalForm, Toggle, TextInput
from endstone.inventory import ItemStack
from endstone.command import Command, CommandSender

current_dir = os.getcwd()

first_dir = os.path.join(current_dir, 'plugins', 'u-dynamic-light')

if not os.path.exists(first_dir):
    os.mkdir(first_dir)

config_data_file_path = os.path.join(first_dir, 'config.json')

lang_dir = os.path.join(first_dir, 'lang')

if not os.path.exists(lang_dir):
    os.mkdir(lang_dir)


class u_dynamic_light(Plugin):
    api_version = '0.10'

    def __init__(self):
        super().__init__()

        # Load config data
        if not os.path.exists(config_data_file_path):
            with open(config_data_file_path, 'w', encoding='utf-8') as f:
                config_data = {
                    'item_type_id_allow_in_offhand': {
                        'minecraft:torch': True,
                        'minecraft:soul_torch': True,
                        'minecraft:redstone_torch': True,
                        "minecraft:copper_torch": True,

                        'minecraft:lantern': True,
                        'minecraft:soul_lantern': True,
                        "minecraft:copper_lantern": True,
                        "minecraft:exposed_copper_lantern": True,
                        "minecraft:oxidized_copper_lantern": True,
                        "minecraft:waxed_copper_lantern": True,
                        "minecraft:waxed_exposed_copper_lantern": True,
                        "minecraft:waxed_oxidized_copper_lantern": True,
                        "minecraft:waxed_weathered_copper_lantern": True,
                        "minecraft:weathered_copper_lantern": True,

                        'minecraft:lava_bucket': True,

                        'minecraft:campfire': False,
                        'minecraft:soul_campfire': False,

                        'minecraft:beacon': False,
                        'minecraft:enchanting_table': False,
                        'minecraft:glowstone': False,
                        'minecraft:lit_pumpkin': False,
                        'minecraft:sculk_catalyst': False,

                        'minecraft:ochre_froglight': False,
                        'minecraft:pearlescent_froglight': False,
                        'minecraft:verdant_froglight': False,

                        'minecraft:conduit': False,
                        'minecraft:sea_lantern': False,
                        "minecraft:sea_pickle": False,

                        'minecraft:brown_mushroom': False,
                        'minecraft:glow_berries': False,
                        'minecraft:glow_lichen': False,

                        'minecraft:small_amethyst_bud': False,
                        'minecraft:medium_amethyst_bud': False,
                        'minecraft:large_amethyst_bud': False,
                        'minecraft:amethyst_cluster': False,

                        'minecraft:magma': False,
                        'minecraft:shroomlight': False,
                        'minecraft:crying_obsidian': False,

                        'minecraft:end_rod': False,
                        'minecraft:ender_chest': False,
                        'minecraft:dragon_egg': False
                    },
                    'refresh_tick': 1
                }

                json_str = json.dumps(config_data, indent=4, ensure_ascii=False)

                f.write(json_str)
        else:
            with open(config_data_file_path, 'r', encoding='utf-8') as f:
                config_data = json.loads(f.read())

        self.config_data = config_data

        # Load langs
        self.lang_data = load_lang(lang_dir)

        self.may_glowing_item_type_dict = {
            'minecraft:torch': 14,
            'minecraft:soul_torch': 10,
            'minecraft:redstone_torch': 7,
            "minecraft:copper_torch": 14,

            'minecraft:lantern': 15,
            'minecraft:soul_lantern': 10,
            "minecraft:copper_lantern": 15,
            "minecraft:exposed_copper_lantern": 15,
            "minecraft:oxidized_copper_lantern": 15,
            "minecraft:waxed_copper_lantern": 15,
            "minecraft:waxed_exposed_copper_lantern": 15,
            "minecraft:waxed_oxidized_copper_lantern": 15,
            "minecraft:waxed_weathered_copper_lantern": 15,
            "minecraft:weathered_copper_lantern": 15,

            'minecraft:lava_bucket': 15,

            'minecraft:campfire': 15,
            'minecraft:soul_campfire': 10,

            'minecraft:beacon': 15,
            'minecraft:enchanting_table': 7,
            'minecraft:glowstone': 15,
            'minecraft:lit_pumpkin': 15,
            'minecraft:sculk_catalyst': 6,

            'minecraft:ochre_froglight': 15,
            'minecraft:pearlescent_froglight': 15,
            'minecraft:verdant_froglight': 15,

            'minecraft:conduit': 15,
            'minecraft:sea_lantern': 15,
            "minecraft:sea_pickle": 6,

            'minecraft:brown_mushroom': 1,
            'minecraft:glow_berries': 14,
            'minecraft:glow_lichen': 7,

            'minecraft:small_amethyst_bud': 1,
            'minecraft:medium_amethyst_bud': 2,
            'minecraft:large_amethyst_bud': 4,
            'minecraft:amethyst_cluster': 5,

            'minecraft:magma': 3,
            'minecraft:shroomlight': 15,
            'minecraft:crying_obsidian': 10,

            'minecraft:end_rod': 14,
            'minecraft:ender_chest': 7,
            'minecraft:dragon_egg': 1
        }

        self.may_glowing_item_type_list = [key for key in self.may_glowing_item_type_dict.keys()]

        self.recorder = {}

    def on_enable(self):
        self.server.scheduler.run_task(self, self.light_manage, delay=0, period=self.config_data['refresh_tick'])
        self.logger.info(
            f'{ColorFormat.YELLOW}'
            f'U-DynamicLight is enabled...'
        )

    commands = {
        'offhand': {
            'description': 'Switch items to offhand',
            'usages': ['/offhand'],
            'permissions': ['u_dynamic_light.command.offhand']
        },
        'ud': {
            'description': 'Call out main form of U-DynamicLight',
            'usages': ['/ud'],
            'permissions': ['u_dynamic_light.command.ud']
        }
    }

    permissions = {
        'u_dynamic_light.command.offhand': {
            'description': 'Switch items to offhand',
            'default': True
        },
        'u_dynamic_light.command.ud': {
            'description': 'Call out main form of U-DynamicLight',
            'default': 'Operator'
        }

    }

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> None:
        if command.name == 'offhand':
            if not isinstance(sender, Player):
                sender.send_message(
                    f'{ColorFormat.RED}'
                    f'This command can only be executed by a player...'
                )

                return

            if sender.inventory.item_in_main_hand is None:
                sender.send_message(
                    f'{ColorFormat.RED}'
                    f'{self.get_text(sender, "switch.message.fail_1")}'
                )

                return
            else:
                    item_in_main_hand_type_id = sender.inventory.item_in_main_hand.type.id

                    if not self.config_data['item_type_id_allow_in_offhand'].get(item_in_main_hand_type_id):
                        sender.send_message(
                            f'{ColorFormat.RED}'
                            f'{self.get_text(sender, "switch.message.fail_2")}'
                        )

                        item_allow_offhand_name_list = []

                        for item_type_id, bool_value in self.config_data['item_type_id_allow_in_offhand'].items():
                            if bool_value:
                                itemstack = ItemStack(
                                    type=item_type_id
                                )

                                item_type_translation_key = itemstack.type.translation_key

                                item_name = self.server.language.translate(
                                    item_type_translation_key,
                                    None,
                                    sender.locale
                                )

                                item_allow_offhand_name_list.append(item_name)

                        if len(item_allow_offhand_name_list) != 0:
                            sender.send_message(
                                f'{ColorFormat.YELLOW}'
                                f'{self.get_text(sender, "switch.message.fail_3")}'
                            )

                            for i in item_allow_offhand_name_list:
                                sender.send_message(
                                    f'{ColorFormat.YELLOW}- {i}'
                                )

                        return

                    item_in_main_hand_amount = sender.inventory.item_in_main_hand.amount

                    itemstack_for_off_hand = ItemStack(
                        type=item_in_main_hand_type_id,
                        amount=item_in_main_hand_amount,
                    )

                    if sender.inventory.item_in_off_hand is None:
                        itemstack_for_main_hand = None
                    else:
                        item_in_off_hand_type = sender.inventory.item_in_off_hand.type

                        item_in_off_hand_amount = sender.inventory.item_in_off_hand.amount

                        itemstack_for_main_hand = ItemStack(
                            type=item_in_off_hand_type,
                            amount=item_in_off_hand_amount
                        )

                    sender.inventory.item_in_off_hand = itemstack_for_off_hand
                    sender.inventory.item_in_main_hand = itemstack_for_main_hand

                    sender.send_message(
                        f'{ColorFormat.YELLOW}'
                        f'{self.get_text(sender, "switch.message.success")}'
                    )

        if command.name == 'ud':
            if not isinstance(sender, Player):
                sender.send_message(
                    f'{ColorFormat.RED}'
                    f'This command can only be executed by a player...'
                )

                return

            if sender.is_op:
                textinput = TextInput(
                    label=f'{ColorFormat.GREEN}'
                          f'{self.get_text(sender, "form.textinput.label")}: '
                          f'{ColorFormat.WHITE}'
                          f'{self.config_data["refresh_tick"]} (tick)',
                    placeholder=self.get_text(sender, "form.textinput.placeholder"),
                    default_value=str(self.config_data['refresh_tick'])
                )

                controls = [textinput]

                for item_type_id, bool_value in self.config_data['item_type_id_allow_in_offhand'].items():
                    itemstack = ItemStack(
                        type=item_type_id
                    )

                    item_translation_key = itemstack.type.translation_key

                    item_name = self.server.language.translate(
                        item_translation_key,
                        None,
                        sender.locale
                    )

                    controls.append(
                        Toggle(
                            label=f'{ColorFormat.GREEN}'
                                  f'{item_name}',
                            default_value=bool_value
                        )
                    )

                form = ModalForm(
                    title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}'
                          f'U-DynamicLight',
                    controls=controls,
                    submit_button=f'{ColorFormat.YELLOW}'
                                  f'{self.get_text(sender, "form.submit_button")}',
                    on_close=None
                )

                def on_submit(s: CommandSender, json_str: str):
                    data = json.loads(json_str)

                    try:
                        update_refresh_tick = int(data[0])
                    except:
                        s.send_message(
                            f'{ColorFormat.RED}'
                            f'{self.get_text(s, "reload.message.fail")}'
                        )

                        return

                    if update_refresh_tick <= 0:
                        s.send_message(
                            f'{ColorFormat.RED}'
                            f'{self.get_text(s, "reload.message.fail")}'
                        )

                        return

                    update_bool_value_list = data[1:]

                    index = 0

                    for item_type_id in self.config_data['item_type_id_allow_in_offhand'].keys():
                        self.config_data['item_type_id_allow_in_offhand'][item_type_id] = update_bool_value_list[index]

                        index += 1

                    self.save_config_data()

                    s.send_message(
                        f'{ColorFormat.YELLOW}'
                        f'{self.get_text(s, "reload.message.success")}'
                    )

                form.on_submit = on_submit

                sender.send_form(form)

    # Reload configurations
    def save_config_data(self) -> None:
        with open(config_data_file_path, 'w', encoding='utf-8') as f:
            json_str = json.dumps(
                self.config_data,
                indent=4,
                ensure_ascii=False
            )

            f.write(json_str)

    def light_on(self, player: Player, pos: list, dim: Dimension, runtime_id:int) -> None:
        bs = BinaryStream()
        # NetworkBlockPosition
        bs.write_varint(pos[0])
        bs.write_unsigned_varint(pos[1])
        bs.write_varint(pos[2])
        # Runtime ID of the fake block
        bs.write_unsigned_varint(runtime_id)
        # Flags
        bs.write_unsigned_varint(3)
        # Layer
        bs.write_unsigned_varint(0)

        bytes = bs.get_and_release_data()

        # Send UpdateBlockPacket to the target player
        player.send_packet(21, bytes)

        self.recorder[player.name] = {
            'pos': pos,
            'dim': dim,
            'runtime_id': runtime_id
        }

    def light_off(self, player: Player) -> None:
        if self.recorder.get(player.name) is None:
            return

        pos: list = self.recorder[player.name]['pos']

        bs = BinaryStream()
        # NetworkBlockPosition
        bs.write_varint(pos[0])
        bs.write_unsigned_varint(pos[1])
        bs.write_varint(pos[2])
        # Runtime ID of minecraft:air
        bs.write_unsigned_varint(3690217760)
        # Flags
        bs.write_unsigned_varint(3)
        # Layer
        bs.write_unsigned_varint(0)

        bytes = bs.get_and_release_data()

        # Send UpdateBlockPacket to the target player
        player.send_packet(21, bytes)

        self.recorder.pop(player.name)

    def light_manage(self) -> None:
        if len(self.server.online_players) == 0:
            return

        for online_player in self.server.online_players:
            if (
                    (
                        online_player.inventory.item_in_main_hand is not None
                        and
                        online_player.inventory.item_in_main_hand.type.id in self.may_glowing_item_type_list
                    )
                    or
                    (
                        online_player.inventory.item_in_off_hand is not None
                        and
                        online_player.inventory.item_in_off_hand.type.id in self.may_glowing_item_type_list
                    )
            ):
                pos = [
                    math.floor(online_player.location.x),
                    math.floor(online_player.location.y + 1),
                    math.floor(online_player.location.z)
                ]

                dim = online_player.dimension

                block = dim.get_block_at(pos[0], pos[1], pos[2])

                if block.type == 'minecraft:air':
                    # In summary, there are five possible cases.
                    # Case 1: glowing items in mainhand & nothing in offhand
                    if (
                            (
                                online_player.inventory.item_in_main_hand is not None
                                and
                                online_player.inventory.item_in_main_hand.type.id in self.may_glowing_item_type_list
                            )
                            and
                            online_player.inventory.item_in_off_hand is None
                    ):
                        light_emission_level = self.may_glowing_item_type_dict[online_player.inventory.item_in_main_hand.type.id]

                    # Case2: glowing items in mainhand & unglowing legacy items in offhand
                    elif (
                            (
                                online_player.inventory.item_in_main_hand is not None
                                and
                                online_player.inventory.item_in_main_hand.type.id in self.may_glowing_item_type_list
                            )
                            and
                            (
                                online_player.inventory.item_in_off_hand is not None
                                and
                                online_player.inventory.item_in_off_hand.type.id not in self.may_glowing_item_type_list
                            )
                    ):
                        light_emission_level = self.may_glowing_item_type_dict[online_player.inventory.item_in_main_hand.type.id]

                    # Case 3: glowing items in offhand & nothing in main hand
                    elif (
                            (
                                online_player.inventory.item_in_off_hand is not None
                                and
                                online_player.inventory.item_in_off_hand.type.id in self.may_glowing_item_type_list
                            )
                            and
                            online_player.inventory.item_in_main_hand is None
                    ):
                        light_emission_level = self.may_glowing_item_type_dict[online_player.inventory.item_in_off_hand.type.id]

                    # Case 4: glowing items in offhand & unglowing legacy items in main hand
                    elif (
                            (
                                online_player.inventory.item_in_off_hand is not None
                                and
                                online_player.inventory.item_in_off_hand.type.id in self.may_glowing_item_type_list
                            )
                            and
                            (
                                online_player.inventory.item_in_main_hand is not None
                                and
                                online_player.inventory.item_in_main_hand.type.id not in self.may_glowing_item_type_list
                            )
                    ):
                        light_emission_level = self.may_glowing_item_type_dict[online_player.inventory.item_in_off_hand.type.id]

                    # Case 5: glowing items in mainhand & glowing items in offhand
                    else:
                        light_emission_level_main_hand = self.may_glowing_item_type_dict[online_player.inventory.item_in_main_hand.type.id]

                        light_emission_level_off_hand = self.may_glowing_item_type_dict[online_player.inventory.item_in_off_hand.type.id]

                        light_emission_level = max(light_emission_level_main_hand, light_emission_level_off_hand)

                    fake_block_type = 'minecraft:light_block_' + str(light_emission_level)

                    fake_block = self.server.create_block_data(
                       fake_block_type,
                        None
                    )

                    runtime_id = fake_block.runtime_id

                    # Check whether the player is staying in place and
                    # -hold the same glowing items, if so, stop sending packets.
                    if self.recorder.get(online_player.name) is not None:
                        if not (
                            pos == self.recorder[online_player.name]['pos']
                            and
                            dim == self.recorder[online_player.name]['dim']
                            and
                            runtime_id == self.recorder[online_player.name]['runtime_id']
                        ):
                            self.light_off(online_player)
                        else:
                            return

                    self.light_on(online_player, pos, dim, runtime_id)
                else:
                    self.light_off(online_player)
            else:
                self.light_off(online_player)

    # Get text
    def get_text(self, player: Player, text_key: str) -> str:
        player_lang = player.locale

        try:
            if self.lang_data.get(player_lang) is None:
                text_value = self.lang_data['en_US'][text_key]
            else:
                if self.lang_data[player_lang].get(text_key) is None:
                    text_value = self.lang_data['en_US'][text_key]
                else:
                    text_value = self.lang_data[player_lang][text_key]

            return text_value
        except Exception as e:
            self.logger.error(
                f'{ColorFormat.RED}'
                f'{e}'
            )

            return text_key
