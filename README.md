## U-DynamicLight

<code><a href="https://github.com/umarurize/UTP"><img height="25" src="./logo/logo.png" alt="U-DynamicLight" /></a>&nbsp;U-DynamicLight</code>

![Total Git clones](https://img.shields.io/badge/dynamic/json?label=Total%20Git%20clones&query=$&url=https://cdn.jsdelivr.net/gh/umarurize/U_DynamicLight@master/clone_count.txt&color=brightgreen)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/umarurize/U_DynamicLight/total)

### 🔔Introductions
* **40+ glowing items support**
* **Offhand mode support**
* **Localized languages support**
* **No damage to data**: Since dynamic light implemented through network packets delivery, it will not do any damage to your Bedrock level.

### 🔨Installation
<details>
<summary>Check your Endstone's version</summary>

* **Endstone 0.10.0+**
  * 251221 (Bedrock Edition 1.21.111+)
  * 250813
* **Endstone 0.9.0 - Endstone 0.9.4**
  * 250619
* **Endstone 0.7.2 - Endstone 0.8.2**
  * 250415
  * 250414
    
</details>

Put `.whl` file into the endstone plugins folder, and then start the server. 

Enter the command `/offhand` to switch glowing items which are allowed by the server to offhand. 

If a player has glowing items in both their mainhand and offhand, the light level will be set to the greater of the two.

### 💻Download
Now, you can get the release version form this repo or <code><a href="https://www.minebbs.com/resources/u-dynamiclight.11035/"><img height="20" src="./logo/minebbs.png" alt="Minebbs" /></a>&nbsp;Minebbs</code>.

### 📁File structure
```
Plugins/
├─ u-dynamic-light/
│  ├─ config.json
│  ├─ lang/
│  │  ├─ zh_CN.json
│  │  ├─ en_US.json
```

### 📝Configurations
`config.json`
```json5
{
    "item_type_id_allow_in_offhand": {
      "minecraft:torch": true,
      "minecraft:soul_torch": true,
      "minecraft:redstone_torch": true,
      "minecraft:copper_torch": true,
      "minecraft:lantern": true,
      "minecraft:soul_lantern": true,
      "minecraft:copper_lantern": true,
      "minecraft:exposed_copper_lantern": true,
      "minecraft:oxidized_copper_lantern": true,
      "minecraft:waxed_copper_lantern": true,
      "minecraft:waxed_exposed_copper_lantern": true,
      "minecraft:waxed_oxidized_copper_lantern": true,
      "minecraft:waxed_weathered_copper_lantern": true,
      "minecraft:weathered_copper_lantern": true,
      "minecraft:lava_bucket": true,
      "minecraft:campfire": false,
      "minecraft:soul_campfire": false,
      "minecraft:beacon": false,
      "minecraft:enchanting_table": false,
      "minecraft:glowstone": false,
      "minecraft:lit_pumpkin": false,
      "minecraft:sculk_catalyst": false,
      "minecraft:ochre_froglight": false,
      "minecraft:pearlescent_froglight": false,
      "minecraft:verdant_froglight": false,
      "minecraft:conduit": false,
      "minecraft:sea_lantern": false,
      "minecraft:sea_pickle": false,
      "minecraft:brown_mushroom": false,
      "minecraft:glow_berries": false,
      "minecraft:glow_lichen": false,
      "minecraft:small_amethyst_bud": false,
      "minecraft:medium_amethyst_bud": false,
      "minecraft:large_amethyst_bud": false,
      "minecraft:amethyst_cluster": false,
      "minecraft:magma": false,
      "minecraft:shroomlight": false,
      "minecraft:crying_obsidian": false,
      "minecraft:end_rod": false,
      "minecraft:ender_chest": false,
      "minecraft:dragon_egg": false
    },
    "refresh_tick": 1    // light refresh interval in ticks
}
```
Operators can enter the command `/ud` to call out the GUI form to edit/update configurations in detail.

### 🌐Languages
- [x] `zh_CN`
- [x] `en_US`

Of course, you can add your mother language to U-DynamicLight, just creat `XX_XX.json` (such as `ja_JP.json`) and translate value with reference to `en_US.json`.

You can also creat a PR to this repo to make your mother language one of the official languages of U-DynamicLight.

### 💥Glowing items
<div style="width: 100%; text-align: center;">
  <img src="./images/item_list.png" style="max-width: 100%; height: auto;">
</div>

### :heart_eyes:Specially thanks
- [x] [@zimuya4153](https://github.com/zimuya4153)
- [x] [@KobeBryant114514](https://github.com/KobeBryant114514)

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=GlacieTeam&repo=BinaryStream-Python)](https://github.com/GlacieTeam/BinaryStream-Python)

![](https://img.shields.io/badge/language-python-blue.svg) [![GitHub License](https://img.shields.io/github/license/umarurize/UTP)](LICENSE)

