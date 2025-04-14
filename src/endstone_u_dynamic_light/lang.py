import os
import json


class lang():
    def load_lang(self, lang_dir: str) -> dict:
        zh_CN_lang_data_file_path = os.path.join(lang_dir, 'zh_CN.json')
        en_US_lang_data_file_path = os.path.join(lang_dir, 'en_US.json')

        if not os.path.exists(zh_CN_lang_data_file_path):
            zh_CN = {
                'switch.message.fail_1': '你的主手和副手上都没有物品...',
                'switch.message.fail_2': '此物品不能被切换至副手...'
            }
            with open(zh_CN_lang_data_file_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(zh_CN, indent=4, ensure_ascii=False)
                f.write(json_str)

        if not os.path.exists(en_US_lang_data_file_path):
            en_US = {
                'switch.message.fail_1': 'There are no itmes in both your mainhand and offhand...',
                'switch.message.fail_2': 'This item can not be switched to offhand...'
            }
            with open(en_US_lang_data_file_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(en_US, indent=4, ensure_ascii=False)
                f.write(json_str)

        lang_data = {}
        lang_list = os.listdir(lang_dir)
        for lang in lang_list:
            lang_name = lang.strip('.json')
            lang_data_file_path = os.path.join(lang_dir, lang)
            with open(lang_data_file_path, 'r', encoding='utf-8') as f:
                lang_data[lang_name] = json.loads(f.read())

        return lang_data

