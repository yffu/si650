'''
Created on Jan 14, 2015

@author: Yuan-Fang
'''
# how was this done? use a recursive descent parser.

import ex0102, re
from collections import namedtuple

def parse(expr):
    #matrix = ex0102.invert_matrix('../../data/ch01/collection02');
    
    token_map = {'AND':'&', 'OR':'|',
                 '(':'LPAR', ')':'RPAR'}
    Token = namedtuple('Token', ['name', 'value'])
    split_expr = re.findall('[a-z.]+|[%s]' % ''.join(token_map), expr)
    tokens = [Token(token_map.get(x, 'NUM'), x) for x in split_expr]
    print tokens

def qresult(filename):
    with open(filename, 'r') as in_hand:
        for line in in_hand:
            tkn=parse(line);
            print tkn;
            
qresult('../../data/ch01/query03');

'''
    A Calculator Implemented With A Top-Down, Recursive-Descent Parser
    # Author: Erez Shinan, Dec 2012
    import re, collections
    from operator import add,sub,mul,div
    Token = collections.namedtuple('Token', ['name', 'value'])
    RuleMatch = collections.namedtuple('RuleMatch', ['name', 'matched'])
    token_map = {'+':'ADD', '-':'ADD', '*':'MUL', '/':'MUL', '(':'LPAR', ')':'RPAR'}
    rule_map = {
        'add' : ['mul ADD add', 'mul'],
        'mul' : ['atom MUL mul', 'atom'],
        'atom': ['NUM', 'LPAR add RPAR', 'neg'],
        'neg' : ['ADD atom'],
    }
    fix_assoc_rules = 'add', 'mul'
    bin_calc_map = {'*':mul, '/':div, '+':add, '-':sub}
    def calc_binary(x):
        while len(x) > 1:
            x[:3] = [ bin_calc_map[x[1]](x[0], x[2]) ]
        return x[0]
    calc_map = {
        'NUM' : float,
        'atom': lambda x: x[len(x)!=1],
        'neg' : lambda (op,num): (num,-num)[op=='-'],
        'mul' : calc_binary,
        'add' : calc_binary,
    }
    def match(rule_name, tokens):
        if tokens and rule_name == tokens[0].name:      # Match a token?
            return tokens[0], tokens[1:]
        for expansion in rule_map.get(rule_name, ()):   # Match a rule?
            remaining_tokens = tokens
            matched_subrules = []
            for subrule in expansion.split():
                matched, remaining_tokens = match(subrule, remaining_tokens)
                if not matched:
                    break   # no such luck. next expansion!
                matched_subrules.append(matched)
            else:
                return RuleMatch(rule_name, matched_subrules), remaining_tokens
        return None, None   # match not found
    def _recurse_tree(tree, func):
        return map(func, tree.matched) if tree.name in rule_map else tree[1]
    def flatten_right_associativity(tree):
        new = _recurse_tree(tree, flatten_right_associativity)
        if tree.name in fix_assoc_rules and len(new)==3 and new[2].name==tree.name:
            new[-1:] = new[-1].matched
        return RuleMatch(tree.name, new)
    def evaluate(tree):
        solutions = _recurse_tree(tree, evaluate)
        return calc_map.get(tree.name, lambda x:x)(solutions)
    def calc(expr):
        split_expr = re.findall('[\d.]+|[%s]' % ''.join(token_map), expr)
        tokens = [Token(token_map.get(x, 'NUM'), x) for x in split_expr]
        tree = match('add', tokens)[0]
        tree = flatten_right_associativity( tree )
        return evaluate(tree)
    if __name__ == '__main__':
        while True:
            print( calc(raw_input('> ')) )
'''