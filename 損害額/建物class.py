#Œš•¨‚Ì‘¹ŠQŠz‚ğZo‚·‚éclass
class bldg:
    #Œš•¨‚Ì‘¹ŠQŠz‚ÌŒvZ
    def dmg_value(self, cost, total_area, dpc_rate, age, dmg_rate):
            #Œš•¨‚Ì‹àŠz
            house_price = cost * total_area
            #‹p‚³‚ê‚½‹àŠz
            dpc_price = house_price * 0.9 * dpc_rate * age
            #‰¿‘Šz
            tmp_price = house_price - dpc_price
            #’z”N‚ª‘½‚¢‚½‚ß‰¿‘Šz‚ªƒ}ƒCƒiƒX‚É‚È‚Á‚½ê‡‚ÌğŒ•ªŠò
            if (tmp_price / house_price) < 0.05:
                    tmp_price = house_price * 0.05
            #‘¹ŠQŠz
            dmg = tmp_price * dmg_rate
            return dmg

    def house_price(self, cost, total_area):
            #Œ¸‰¿‹p‚È‚µ‚ÌZ‘î‚Ì‹àŠz
            house_price = cost * total_area
            return house_price
