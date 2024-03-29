#建物の損害額を算出するclass
class bldg:
    #建物の損害額の計算
    def dmg_value(self, cost, total_area, dpc_rate, age, dmg_rate):
            #建物の金額
            house_price = cost * total_area
            #償却された金額
            dpc_price = house_price * 0.9 * dpc_rate * age
            #時価総額
            tmp_price = house_price - dpc_price
            #築年が多いため時価総額がマイナスになった場合の条件分岐
            if (tmp_price / house_price) < 0.05:
                    tmp_price = house_price * 0.05
            #損害額
            dmg = tmp_price * dmg_rate
            return dmg

    def house_price(self, cost, total_area):
            #減価償却なしの住宅の金額
            house_price = cost * total_area
            return house_price
