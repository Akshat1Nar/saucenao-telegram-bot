import logging
from saucenao import SauceNao
from pprint import pprint

saucenao = SauceNao(directory='directory', databases=999, minimum_similarity=65, combine_api_types=False, api_key='<YOUR_API_KEY>',
                    exclude_categories='', move_to_categories=False,  use_author_as_category=False,
                    output_type=SauceNao.API_HTML_TYPE, start_file='', log_level=logging.ERROR,
                    title_minimum_similarity=90)
filtered_results = saucenao.check_file(file_name = "<FILE_PATH>")
pprint(filtered_results)

print(filtered_results[2]["data"]["content"][1])
