#�����̑��Q�z���Z�o����class
class bldg:
    #�����̑��Q�z�̌v�Z
    def dmg_value(self, cost, total_area, dpc_rate, age, dmg_rate):
            #�����̋��z
            house_price = cost * total_area
            #���p���ꂽ���z
            dpc_price = house_price * 0.9 * dpc_rate * age
            #�������z
            tmp_price = house_price - dpc_price
            #�z�N���������ߎ������z���}�C�i�X�ɂȂ����ꍇ�̏�������
            if (tmp_price / house_price) < 0.05:
                    tmp_price = house_price * 0.05
            #���Q�z
            dmg = tmp_price * dmg_rate
            return dmg

    def house_price(self, cost, total_area):
            #�������p�Ȃ��̏Z��̋��z
            house_price = cost * total_area
            return house_price
