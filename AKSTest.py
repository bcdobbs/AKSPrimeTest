# -*- coding: utf-8 -*-
"""
Class File for AKS Primality Test
https://en.wikipedia.org/wiki/AKS_primality_test

Created on Tue Apr 11 20:28:57 2017
@author: Ben Dobbs
"""
import math
from sympy import *

class AKSTest:
    'Class to run an AKS Primality Test on a given number.'
    
    def __init__(self, IntegerToTest):
        #Initialise an instance of the class and set up private variables.
        self._n = IntegerToTest
        
        self._NotPrimeAtStep1 = False
        self._SmallestR = 0
        self._NotPrimeAtStep3 = False
        self._PrimeAtStep4 = False
        self._NotPrimeAtStep5 = False
        
        self._IsPrime = False
        self._AnswerString = 'Not Yet Tested'
        
        self._RunAlorithm()
        
    def _EulerTotient(self, n):
        """
        The Euler Totient of a number is a count of how 
        many numbers are coprime with it.
        """
        
        Count = 0

        for i in range(1,n+1):
            if math.gcd(i, self._n) == 1: #gcd is american for HCF.
                Count = Count + 1

        return Count
    

        
    def _Step1TestPerfectPower(self):
        """
        Check to see if n can be written in form a^b
        """
        
        for b in range(2,int(math.log(self._n,2))+1):
            a = self._n ** (1 / b) #** is python sytax for power.

            if a-int(a) == 0:
                self._NotPrimeAtStep1 = True
                self._AnswerString = 'Perfect power so not prime.'
                self._IsPrime = False
                return
            
        self._NotPrimeAtStep1 = False
        self._AnswerString = 'Passed step 1.'
        return
    
    def _Step2FindSmallestR(self):
        """
        Find the smallest r such that ord_r(n) > (log_2 n)^2. 
        (if r and n are not coprime, then skip this r)
        
        ord_r(n) means find value k such that n^k == 1 mod r 
        where n and r are coprime.
        
        NEW:
        A multiplicative order is gauranteed to exist and we don't need
        to know what it is sufficient to only check for values of k up to (log_2 n)^2, 
        if ord(n) not found by this point then we have the correct value of R because
        we know that when it is found it will be bigger than (log_2 n_^2)
        """
        
        MaxK = int(math.log(self._n, 2)) ** 2 #If or(n) is not found by this point then we have finished.
        RUpperBound = int((math.log(self._n, 2)) ** 5) #R will be found long before this.
        
        for r in range (2,RUpperBound+1):
            NextR = False
            
            if math.gcd(r, self._n) == 1: #Check that r and n are coprime skip if not.
                for k in range(1,MaxK+1): #Checks through each value of k - note k is the multiplicative order of n modulo r.
                    if (self._n ** k) % r == 1: # % is python for mod.
                        NextR = True
            if NextR == False:
                self._SmallestR = r
                print(self._SmallestR)
                break #Exits R loop.
        return
    
    def _Step3CheckAnyADoesNotDivide(self):
        """
        Checks through numbers up to smallest r to see if they divide into n.
        """
        
        AUpperBound = min(self._SmallestR, self._n - 1)

        for a in range(2, AUpperBound+1):
            if math.gcd(a, self._n) != 1:
                self._NotPrimeAtStep3 = True
                self._IsPrime = False
                self._AnswerString = 'Not prime at step 3 because ' + str(a) + ' divides ' + str(self._n) + '.'
                return
            
        self._NotPrimeAtStep3 = False
        self._AnswerString = 'Passed step 3.'
        return
    
    def _Step4CheckNLessThanR(self):
        """
        Checks whether n is less than SmallestR
        """
        
        if self._n < self._SmallestR:
            self._PrimeAtStep4 = True
            self._IsPrime = True
            self._AnswerString = 'Proven prime after step 4.'
        else:
            self._PrimeAtStep4 = False
            self._IsPrime = False
            self.AnswerString = 'Not concluded after step 4 so moving to step 5.'
        return
    
    def _Step5CheckUptoEulerTotient(self):
        Phi = self._EulerTotient(self._SmallestR) #Computes euler totient of n.
        UpperBound = int((Phi ** (1 / 2)) * math.log(self._n,2)) #Sets upper bound.
        
        x, a = symbols("x a") #Tells sympy we will use x and a as symbols.
        init_printing(use_unicode=True)  #Makes sympy print nicely if we want it.

        n=self._n
        r=self._SmallestR #not really required but makes the symbolic algebra more readable.

        expr1 = (x+a)**n #Sets up the parts of the expression where ** is power sign.
        expr2 = x**n + a
        expr3 = x**r - 1

        LHSRemainder = rem(expr1, expr3) #finds the remainder of expr1/expr3)
        RHSRemainder = rem(expr2, expr3) # finds the remainder of expr2/expr3)

        LHSRemModN = polys.polytools.trunc(LHSRemainder,n) #reduces coefficients of the Remainders modulo n. 
        RHSRemModN = polys.polytools.trunc(RHSRemainder,n)
        Diff = LHSRemModN - RHSRemModN
        
        for k in Range(1,UpperBound+1):
            """
            #Loops through values of a up to upper bound and substitutes 
            them into the Diff before again reducing modulo n.
            """
            Answer = Diff.subs(a, k) % n 
            if Answer != 0:
                self._NotPrimeAtStep5 = True
                self._AnswerString = 'Not prime at step 5. Fails with a = ' + str(a)
                return
        
        self._NotPrimeAtStep5 = False
        self._IsPrime = True
        self._AnswerString = 'Proven prime after full completion of all 5 steps.'
        return
            

    def _RunAlorithm(self):
        
        if self._n == 0:
            self._IsPrime = False
            self._AnswerString = 'Zero is not prime.'
            return
        
        if self._n == 1:
            self._IsPrime = False
            self._AnswerString = 'One is not prime.'
            return
            
        if self._n == 2:
            self._IsPrime = True
            self._AnswerString = 'Two is prime.'
            return
            
        """
        First three statements are there to catch 0, 1 and 2 which cause division by 0 errors.
        """
        
        self._Step1TestPerfectPower()
        if self._NotPrimeAtStep1 == True:
            return
        
        self._Step2FindSmallestR()
        
        self._Step3CheckAnyADoesNotDivide()
        if self._NotPrimeAtStep3 == True:
            return
        
        self._Step4CheckNLessThanR()
        if self._PrimeAtStep4 == True:
            return
        
        self._Step5CheckUptoEulerTotient()
        return
    
    def IsPrime(self):
        return self._IsPrime
    
    def GetSmallestR(self):
        return self._SmallestR
    
    def GetAnswer(self):
        return self._AnswerString
        
        
        