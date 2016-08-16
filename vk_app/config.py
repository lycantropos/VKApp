VK_SCRIPT_GET_ALL = """var params = {2};
var max_count = params.count, init_offset = params.offset, key = "{1}", offset_count = init_offset;
var vk_api_req = API.{0}(params), c = vk_api_req.count, items_count = vk_api_req[key], i = 1;

while (i < 25 && offset_count + max_count <= c) {{
    offset_count = i * max_count + init_offset;
    params.offset = offset_count;
    items_count = items_count + API.{0}(params)[key];
    i = i + 1;
}}

return {{count: c, items: items_count, offset: offset_count + max_count, max_c: max_count}};
"""
