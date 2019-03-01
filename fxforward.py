import pandas as pd

class FXForward:
    
    def __init__(self, pay_cur, rec_cur, pay_note, rec_note, base_cur="GBP"):
        self.contract = {
            "PaymentIn":pay_cur,
            "ReceiveIn":rec_cur,
            "Pay":pay_note,
            "Receive":rec_note
        }
        self.base_currency = base_cur
        
    def calc_price(self, pay_fx, rec_fx):
        payment = self.contract["Pay"] / pay_fx
        receive = self.contract["Receive"] / rec_fx
        return receive - payment
    
    def calc_scenario(self, scenario_paycur, scenario_reccur):
        """Args:
        scenario_paycur: fxrates of payment currency
        scenario_reccur: fxrates of receive currency
        """
        mapped_prices = map(lambda x : self.calc_price(x[0], x[1]), zip(scenario_paycur, scenario_reccur))
        return pd.Series(mapped_prices)
    
    def calc_simulations(self,sims_pay, sims_rec):
        # zip will return colnames
        sim_res = pd.DataFrame()
        n_scenario = 1
        for paycol, reccol in zip(sims_pay, sims_rec):
            sim_res["Scenario " + str(n_scenario)] = self.calc_scenario(sims_pay[paycol], sims_rec[reccol])
            n_scenario += 1
        return sim_res


def ee(sim_res):
    """calculate expected exposure
    """
    return sim_res[sim_res > 0].fillna(0).mean(axis=1)

def pfe(sim_res, p):
    """calc percentile of exposure
    """
    return sim_res.fillna(0).quantile(q=p, axis=1)