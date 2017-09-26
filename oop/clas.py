import re


class CountIp(object):
    def __init__(self, patt):
        self.cpatt = re.compile(ip)
        # print(self.cpatt)

    def count_patt(self, fname):
        patt_disct = {}
        with open(fname) as fobj:
            for line in fobj:
                m = self.cpatt.search(line)
                if m:
                    key = m.group()
                    patt_disct[key] = patt_disct.get(key, 0) + 1
        return patt_disct


    def sort2(self, patt_list):
        if len(patt_list) <= 1:
            return patt_list
        middle = patt_list.pop()
        larger = []
        smaller = []
        for i in patt_list:
            if i[1] <= middle[1]:
                smaller.append(i)
            else:
                larger.append(i)
        return self.sort2(larger) + [middle] + self.sort2(smaller)


if __name__ == '__main__':
    ip = '^(\d+\.){3}\d+'
    file = 'access.log'
    countip = CountIp(ip)
    ip_dict = countip.count_patt(file)
    print(ip_dict.items())
    print(countip.sort2(list(ip_dict)))
