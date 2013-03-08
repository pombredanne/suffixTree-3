position = -1


def addChar(c):
    remainder = 1
    position += 1
    while remainder > 0:
        if active_length == 0: active_edge = position

        if not nodes[active_node].next.containsKey(active_edge()):
            leaft  = newNode(position, end)
            nodes[active_node].next.put(active_edge(), leaf)
            active_length -= 1
            addSuffixLink(active_node)
        else:
            leaf = nodes[active_node].next.get(active_edge())
            if walkDown(leaf): continue
            if text[nodes[leaf].start + active_length] == c:
                remainder += 1
                active_length += 1
                addSuffixLink(active_node)
                break
            split = newNode(nodes[leaf].start + active_length, end)
            leaf = newNode(
