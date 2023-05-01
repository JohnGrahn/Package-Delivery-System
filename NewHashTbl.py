# Creates NewHashTbl class
# Modified version of the Greedy Algorithm from C950 Webinar 2
# W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py

class NewHashTbl:
    def __init__(self, init_cap=20):
        self.tbl = []
        for i in range(init_cap):
            self.tbl.append([])

# Insertion method to add item into hash table

    def insertion(self, key, item):
        bkt = hash(key) % len(self.tbl)
        bkt_list = self.tbl[bkt]
# O(N) Runtime
        for kv in bkt_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bkt_list.append(key_value)
        return True
# Method looks for item in hash table

    def item_lookup(self, key):
        bkt = hash(key) % len(self.tbl)
        bkt_list = self.tbl[bkt]
# O(N) Runtime
        for match in bkt_list:
            if key == match[0]:
                return match[1]
        return None
# Method deletes corresponding item from hash table

    def item_removal(self, key):
        bkt = hash(key) % len(self.tbl)
        bkt_list = self.tbl[bkt]

        if key in bkt_list:
            bkt_list.remove(key)
