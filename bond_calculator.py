'''

@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Group Name    :
@Student Name  : Jonathan Dinh, Chihoon Kim

@Date          : Fall 2021

A Bond Calculator Class

'''

import math
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from bisection_method import bisection

import enum
import calendar

from datetime import date

from bond import Bond, DayCount, PaymentFrequency


def get_actual360_daycount_frac(start, end):
    day_in_year = 360
    day_count = (end - start).days
    return(day_count / day_in_year)

def get_30360_daycount_frac(start, end):
    day_in_year = 360
    day_count = 360*(end.year - start.year) + 30*(end.month - start.month - 1) + \
                max(0, 30 - start.day) + min(30, end.day)
    return(day_count / day_in_year)


def get_actualactual_daycount_frac(start, end):
    # TODO
    if (start.year < end.year):
        if (calendar.isleap(start.year)):
           year1 = (date(start.year, 12,31)-start).days/366
        year1 = (date(start.year, 12,31)-start).days/365
        if (calendar.isleap(end.year)):
            year2 = (end-date(end.year, 1,1)).days/366
        year2 = (end-date(end.year, 1,1)).days/365
    result = year1 + year2
    # end TODO
    return(result)

class BondCalculator(object):
    '''
    Bond Calculator class for pricing a bond
    '''

    def __init__(self, pricing_date):
        self.pricing_date = pricing_date

    def calc_one_period_discount_factor(self, bond, yld):
        # calculate the future cashflow vectors
        # TODO: calculate the one period discount factor
        # hint: need to use if else statement for different payment frequency cases
        df = None
        if bond.payment_freq == PaymentFrequency.MONTHLY:
            df=1/(1+yld/12)
        elif bond.payment_freq == PaymentFrequency.QUARTERLY:
            df=1/(1+yld/4)
        elif bond.payment_freq==PaymentFrequency.SEMIANNUAL:
            df=1/(1+yld/2)
        elif bond.payment_freq==PaymentFrequency.ANNUAL:
            df=1/(1+yld)
        else:
            raise Exception("Invalid Payment Frequency.")

        return(df)

        # end TODO

        #NOT DONE -- done?
    def calc_clean_price(self, bond, yld):
        '''
        Calculate bond price as of the pricing_date for a given yield
        bond price should be expressed in percentage eg 100 for a par bond
        '''
        result = None
        one_period_factor = self.calc_one_period_discount_factor(bond, yld)
        # TODO: implement calculation here
        DiscountFactor = [math.pow(one_period_factor, i+1) for i in range(len(bond.coupon_payment))]
        CashFlow = [cash for cash in bond.coupon_payment]
        CashFlow[-1] += bond.principal
        PresentValues = [CashFlow[i] * DiscountFactor[i] for i in range(len(bond.coupon_payment))]
        TotalPresent=0
        for index in PresentValues:
            TotalPresent = TotalPresent + index
        result = TotalPresent/bond.principal

        return(result*100)

        # end TODO:

        #NOT DONE
    def calc_accrual_interest(self, bond, settle_date):
        '''
        calculate the accrual interest on given a settle_date
        by calculating the previous payment date first and use the date count
        from previous payment date to the settle_date
        '''
        prev_pay_date = bond.get_previous_payment_date(settle_date)
        end_date = settle_date

        # TODO:

        if (bond.day_count == DayCount.DAYCOUNT_30360):
            frac = get_30360_daycount_frac(prev_pay_date, settle_date)
        elif (bond.day_count == DayCount.DAYCOUNT_ACTUAL_360):
            frac = get_actual360_daycount_frac(prev_pay_date, settle_date)


        result = frac * bond.coupon * bond.principal/100



        # end TODO
        return(result)

    #NOT DONE -> done?
    def calc_macaulay_duration(self, bond, yld):
        '''
        time to cashflow weighted by PV
        '''

        # TODO: implement details here
        #PVs = Cash Flow * Discount Factor
        one_period_factor = self.calc_one_period_discount_factor(bond, yld)
        DisFactor = [math.pow(one_period_factor, i+1) for i in range(len(bond.coupon_payment))]
        CashFlow = [cash for cash in bond.coupon_payment]
        CashFlow[-1] += bond.principal
        PresentValues = [ CashFlow[i]*DisFactor[i] for i in range(len(bond.coupon_payment))]
        wavg = [bond.payment_times_in_year[1] * PresentValues[i] for i in range(len(bond.coupon_payment))]
        result =( sum(wavg) / sum(PresentValues))

        # end TODO
        return(result)

    def calc_modified_duration(self, bond, yld):
        '''
        calculate modified duration at a certain yield yld
        '''
        D = self.calc_macaulay_duration(bond, yld)

        # TODO: implement details here
        result = None
        if bond.payment_freq == PaymentFrequency.MONTHLY:
            result = (D/(1+yld/12))
        elif bond.payment_freq == PaymentFrequency.QUARTERLY:
            result = (D/(1+yld/4))
        elif bond.payment_freq == PaymentFrequency.SEMIANNUAL:
            result = (D/(1+yld/2))
        elif bond.payment_freq == PaymentFrequency.ANNUAL:
            result = (D/(1+yld))
        # end TODO:
        return(result)

    def calc_yield(self, bond, bond_price):
        '''
        Calculate the yield to maturity on given a bond price using bisection method
        '''

        def match_price(yld):
            calculator = BondCalculator(self.pricing_date)
            px = calculator.calc_clean_price(bond, yld)
            return(px - bond_price)

        # TODO: implement details here
        yld, n_iteractions = bisection(match_price, 0, 1000, eps=1.0e-6)
        # end TODO:
        return(yld)

    def calc_convexity(self, bond, yld):
        # calculate convexity of a bond at a certain yield yld

        # TODO: implement details here
        # result = sum(wavg) / sum(PVs))
        return(result)


##########################  some test cases ###################

def _example2():
    pricing_date = date(2021, 1, 1)
    issue_date = date(2021, 1, 1)
    engine = BondCalculator(pricing_date)

    # Example 2
    bond = Bond(issue_date, term=10, day_count = DayCount.DAYCOUNT_30360,
                 payment_freq = PaymentFrequency.ANNUAL, coupon = 0.05)

    yld = 0.06
    px_bond2 = engine.calc_clean_price(bond, yld)
    print("The clean price of bond 2 is: ", format(px_bond2, '.4f'))
    assert( abs(px_bond2 - 92.640) < 0.01)


def _example3():
    pricing_date = date(2021, 1, 1)
    issue_date = date(2021, 1, 1)
    engine = BondCalculator(pricing_date)


    bond = Bond(issue_date, term = 2, day_count =DayCount.DAYCOUNT_30360,
                 payment_freq = PaymentFrequency.SEMIANNUAL,
                 coupon = 0.08)

    yld = 0.06
    px_bond3 = engine.calc_clean_price(bond, yld)
    print("The clean price of bond 3 is: ", format(px_bond3, '.4f'))
    assert( abs(px_bond3 - 103.717) < 0.01)


def _example4():
    # unit tests
    pricing_date = date(2021, 1, 1)
    issue_date = date(2021, 1, 1)
    engine = BondCalculator(pricing_date)

    # Example 4 5Y bond with semi-annual 5% coupon priced at 103.72 should have a yield of 4.168%
    price = 103.72
    bond = Bond(issue_date, term=5, day_count = DayCount.DAYCOUNT_30360,
                payment_freq = PaymentFrequency.SEMIANNUAL, coupon = 0.05, principal = 100)


    yld = engine.calc_yield(bond, price)

    print("The yield of bond 4 is: ", yld)

    assert( abs(yld - 0.04168) < 0.01)

def _test():
    # basic test cases
    _example2()
    _example3()
    _example4()



if __name__ == "__main__":
    _test()
