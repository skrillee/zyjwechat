# from collections import namedtuple
#
# websites = [
#     ('Sohu', 'http://www.google.com/', u'张朝阳'),
#     ('Sina', 'http://www.sina.com.cn/', u'王志东'),
#     ('163', 'http://www.163.com/', u'丁磊')
# ]
#
# Website = namedtuple('Website', ['name', 'url', 'founder'])
#
# for website in websites:
#     website = Website._make(website)
#
#     print(website)


import collections
AirContent = collections.namedtuple('AirContent', ('tvoc', 'co2'))


class AirQuality(object):
    def __init__(self):
        self._contents = []

    def report_content(self, tvoc, co2):
        self._contents.append(AirContent(tvoc, co2))

    def average_content(self):
        average = {
            'tvoc': '',
            'co2': ''
        }
        tvoc_total, co2_total = 0, 0
        quantity = len(self._contents)
        for content in self._contents:
            tvoc_total += content.tvoc
            co2_total += content.co2
        average['tvoc'] = tvoc_total / quantity
        average['co2'] = co2_total / quantity
        return average


class Equipment(object):
    def __init__(self):
        self._equipments = {}

    def subject(self, name):
        if name not in self._equipments:
            self._equipments[name] = AirQuality()
        return self._equipments[name]

    def average_grade(self):
        for subject in self._equipments.values():
            return subject.average_content()


class CustomerData(object):
    def __init__(self):
        self._customers = {}

    def customer(self, equipment_number):
        if equipment_number not in self._customers:
            self._customers[equipment_number] = Equipment()
        return self._customers[equipment_number]


data = CustomerData()
# user = data.customer('A1001')
# tvoc_co2 = user.subject('tvoc_co2')
# tvoc_co2.report_content(6, 500)
# tvoc_co2.report_content(5, 200)
# tvoc_co2.report_content(6, 400)
# tvoc_co2.report_content(9, 300)
#
# user_2 = data.customer('A1002')
# tvoc_co2_2 = user_2.subject('tvoc_co2')
# tvoc_co2_2.report_content(6, 500)
# tvoc_co2_2.report_content(5, 200)
# print(user.average_grade())


data_list = ['A1001','A1002','A1001']
for i in data_list:
    user = data.customer(i)
    tvoc_co2 = user.subject('tvoc_co2')
    tvoc_co2.report_content(6, 500)
    tvoc_co2.report_content(5, 200)
    tvoc_co2.report_content(6, 400)
    tvoc_co2.report_content(9, 300)
tvoc_co2.report_content(9, 300)
tvoc_co2.report_content(9, 300)
tvoc_co2.report_content(9, 300)
print(user.average_grade())