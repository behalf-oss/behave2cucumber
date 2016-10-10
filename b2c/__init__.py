def convert(json_file):
    nodes = ['feature', 'elements', 'steps']
    unneeded_fields = ['status', 'step_type']

    def format_level(tree, index=0, counter=0):
        for item in tree:
            uri, line = item.pop("location").split(":")
            item["line"] = int(line)
            for field in unneeded_fields:
                if field in item:
                    item.pop(field)
            if 'tags' in item:
                item['tags'] = [{"name": tag, "line": item["line"] - 1} for tag in item['tags']]
            if nodes[index] == 'steps':
                if 'result' in item:
                    if 'error_message' in item["result"]:
                        error_msg = item["result"].pop('error_message')
                        item["result"]["error_message"] = str(error_msg).replace("\"", "")
                else:
                    item["result"] = {"status": "skipped", "duration": 0}
            else:
                item["uri"] = uri
                item["description"] = ""
                item["id"] = counter
                counter += 1
            if index != len(nodes) - 1 and nodes[index + 1] in item:
                item[nodes[index + 1]] = format_level(
                    item[nodes[index + 1]], index + 1, counter=counter
                )
        return tree

    return format_level(json_file)
