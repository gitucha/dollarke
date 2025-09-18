class Fund:

    def __init__(self,name,yield_rate,fees,min_deposit):
        self.name = name
        self.yield_rate = yield_rate
        self.fees = fees
        self.min_deposit = min_deposit

    def net_return(self):
        return self.yield_rate - self.fees
    
    def __repr__(self):
        return f"{self.name} (Net Return : {self.net_return():.2f}) "