class asset:
    def lost_assets(self, assets, add_assets, dmg_rate):
        lost_assets = (assets + add_assets) * dmg_rate
    
        return lost_assets