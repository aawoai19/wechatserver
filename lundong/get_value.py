#coding=utf-8


from lundong.sel import my_sel
from lundong.models import Zhishu
import time

sh300_Num = '002987'
cyb_Num = '001593'
sz50_Num = '001549'
zz500_Num = '002903'
url = 'http://fund.eastmoney.com/f10/jjjz_%s.html'

class sel_value():
    def __init__(self):
        self.f_dir = {
            'sz50':sz50_Num,
            'sh300':sh300_Num,
            'zz500':zz500_Num,
            'cyb':cyb_Num
        }
        self.url = url
        self.sel = my_sel()

    def get_value(self,name,num):
            sel = self.sel
            url = self.url%num
            sel.driver.get(url)
            for times in range(3):
                for row in range(1,21):
                    value = sel.get_xpath('//*[@id="jztable"]/table/tbody/tr[%s]/td[2]'%row).text
                    date = sel.get_xpath('//*[@id="jztable"]/table/tbody/tr[%s]/td[1]'%row).text
                    name_id = int(num)*100000000+int(date.replace('-',''))
                    u = Zhishu.objects.filter(name_id=name_id)
                    if len(u)>0:
                        ob = Zhishu.objects.get(name_id=name_id)
                        ob.idkey = times*20+row
                        ob.save()
                    else:
                        Zhishu.objects.create(name=name, name_id=name_id, idkey=times * 20 + row, value=value,date=date)
                sel.get_xpath('//*[@id="pagebar"]/div[1]/label[8]').click()
                time.sleep(0.5)

    def close(self):
        self.sel.close()
        time.sleep(0.5)

    def get_all(self):
        for k,v in self.f_dir.items():
            self.get_value(k,v)


if __name__ == '__main__':
    value = sel_value()
    value.get_value('sh300',sh300_Num)