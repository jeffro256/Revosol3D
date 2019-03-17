from pyparsing import Literal,Word,Group,\
	ZeroOrMore,Forward,alphas,alphanums,Regex,ParseException,\
	CaselessKeyword, Suppress
import math
import operator

__all__ = ['MathParser']

class MathParser(object):
	def __init__(self):
		self._exprStack = []
		self._parseStr = None

		self.ops = {
			'+'     : operator.add,
			'-'     : operator.sub,
			'*'     : operator.mul,
			'/'     : operator.truediv,
			'^'     : operator.pow
		}

		self.funcs = {
			'sqrt'   : math.sqrt,
			'ln'     : math.log,
			'log'    : math.log10,
			'abs'    : abs,
			'sign'   : lambda x: (x >= 0) - (x < 0),
			'sin'    : math.sin,
			'cos'    : math.cos,
			'tan'    : math.tan,
			'csc'    : lambda x: 1 / math.sin(x),
			'sec'    : lambda x: 1 / math.cos(x),
			'cot'    : lambda x: 1 / math.tan(x),
			'arcsin' : math.asin,
			'acccos' : math.acos,
			'arctan' : math.atan,
			'arccsc' : lambda x: math.asin(1 / x),
			'arcsec' : lambda x: math.acos(1 / x),
			'arccot' : lambda x: math.atan(1 / x) + (x < 0) * math.pi,
			'floor'  : int,
			'round'  : round

		}

		self.setup()

	def setup(self):
		e = CaselessKeyword('E')
		pi = CaselessKeyword('PI')
		var = CaselessKeyword('X')

		fnumber = Regex(r'[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?')
		ident = Word(alphas, alphanums+'_$')

		plus, minus, mult, div = map(Literal, '+-*/')
		lpar, rpar = map(Suppress, '()')
		addop  = plus | minus
		multop = mult | div
		expop = Literal('^')

		expr = Forward()

		atom = ((0,None)*minus + (pi | e | var | fnumber | ident + lpar + expr + rpar | ident).setParseAction(self._pushFirst) |
				Group(lpar + expr + rpar)).setParseAction(self._pushUMinus)

		# by defining exponentiation as "atom [ ^ factor ]..." instead of 
		# "atom [ ^ atom ]...", we get right-to-left exponents, instead of
		# left-to-right. that is, 2^3^2 = 2^(3^2), not (2^3)^2.
		factor = Forward()
		factor << atom + ZeroOrMore((expop + factor).setParseAction(self._pushFirst))

		term = factor + ZeroOrMore((multop + factor).setParseAction(self._pushFirst))
		expr << term + ZeroOrMore((addop + term).setParseAction(self._pushFirst))

		self._parseExpr = expr

	def feed(self, s):
		self._exprStack.clear()
		res = self._parseExpr.parseString(s, parseAll=True)

		self._parseStr = s

		for op in self._exprStack:
			if op.isalpha() and op not in self.funcs and op not in ('PI', 'E', 'X'):
				raise Exception("invalid identifier '%s'" % op)

		return res

	def eval(self, x_val=None, stack=None):
		if stack is None:
			stack = self._exprStack[:]

		op = stack.pop()
		if op == 'unary -':
			return -self.eval(x_val, stack)
		if op in self.ops:
			op2 = self.eval(x_val, stack)
			op1 = self.eval(x_val, stack)
			return self.ops[op](op1, op2)
		elif op == 'PI':
			return math.pi 
		elif op == 'E':
			return math.e
		elif op == 'X':
			if x_val is None:
				raise ValueError("No value provided for x")
			else:
				return x_val
		elif op in self.funcs:
			func = self.funcs[op]
			arg = self.eval(x_val, stack)
			try:
				return func(arg)
			except ValueError:
				raise ValueError("{}({}) causes a math domain error. x={}".format(op, arg, x_val)) from None
		elif op[0].isalpha():
			raise Exception("invalid identifier '%s'" % op)
		else:
			return float(op)

	def parse_string(self):
		return self._parseStr

	def _pushFirst(self, strg, loc, toks):
		self._exprStack.append(toks[0])

	def _pushUMinus(self, strg, loc, toks):
		for t in toks:
			if t == '-':
				self._exprStack.append('unary -')
			else:
				break

	def __call__(self, x_val=None):
		return self.eval(x_val=x_val)

if __name__ == '__main__':
	parser = MathParser()

	str_in = input("Enter mathematical expression of x: ")
	var_val = float(input("Enter value of x: "))

	toks = parser.feed(str_in)

	res = parser.eval(var_val)

	print("Result:", res)
