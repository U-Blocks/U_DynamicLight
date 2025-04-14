## U-DynamicLight

<code><a href="https://github.com/umarurize/UTP"><img height="25" src="https://github.com/umarurize/U_DynamicLight/blob/master/logo/logo.png" alt="U-DynamicLight" /></a>&nbsp;U-DynamicLight</code>

[![Minecraft - Version](https://img.shields.io/badge/minecraft-v1.21.71_(Bedrock)-black)](https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs)
[![PyPI - Version](https://img.shields.io/pypi/v/endstone)](https://pypi.org/project/endstone)
![Total Git clones](https://img.shields.io/badge/dynamic/json?label=Total%20Git%20clones&query=$&url=https://cdn.jsdelivr.net/gh/umarurize/U_DynamicLight@master/clone_count.txt&color=brightgreen)

### Introductions
* **30+ glowing items support**
* **Offhand mode support**
* **Localized languages support**
* **No damage to data**: Since dynamic light implemented through network packets delivery, it will not do any damage to your Bedrock level.

### Installation
Put `.whl` file into the endstone plugins folder, and then start the server. 

Enter the command `offhand` to switch glowing items to offhand. 

If a player both has glowing items in mainhand and offhand, the light emission level with be set to the greater of the two.

### Download
Now, you can get the release version form this repo or <code><a href="https://www.minebbs.com/resources/u-dynamiclight.11035/"><img height="20" src="https://github.com/umarurize/umaru-cdn/blob/main/images/minebbs.png" alt="Minebbs" /></a>&nbsp;Minebbs</code>.

### File structure
```
Plugins/
├─ u-dynamic-light/
│  ├─ lang/
│  │  ├─ zh_CN.json
│  │  ├─ en_US.json
```

### Languages
- [x] `zh_CN`
- [x] `en_US`

Off course you can add your mother language to U-DynamicLight, just creat `XX_XX.json` (such as `ja_JP.json`) and translate value with reference to `en_US.json`.

You can also creat a PR to this repo to make your mother language one of the official languages of U-DynamicLight.

### Glowing items
<div style="width: 100%; text-align: center;">
  <img src="https://github.com/umarurize/U_DynamicLight/blob/master/images/item_list.png" style="max-width: 100%; height: auto;">
</div>

### Specially thanks
- [x] [@zimuya4153](https://github.com/zimuya4153)
- [x] [@zimuya4153](https://github.com/KobeBryant114514)

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=GlacieTeam&repo=BinaryStream-Python)](https://github.com/GlacieTeam/BinaryStream-Python)

![](https://img.shields.io/badge/language-python-blue.svg) [![GitHub License](https://img.shields.io/github/license/umarurize/UTP)](LICENSE)

