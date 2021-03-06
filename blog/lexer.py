from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

class BlogLexer(RegexLexer):
  name = 'BLOG'
  aliases = ['blog']
  filenames = ['*.blog', '*.dblog']
  operators = ['\\-\\>','=','~',':', '\\+', '\\-', '\\*', '/', '\\[', ']', 
         '\\{', '}', '!', '\\<', '\\>', '\\<=', '\\>=', '==', '!=', 
         '&', '\\|', '#', '\\^']
  deliminators = [',', ';', '\\(', '\\)']
  keywords = ['extern','import','fixed','distinct','random','origin',
        'param','type', 'forall', 'exists', 'obs', 'query', 
        'if', 'then', 'else']
  types = ['Integer','Real','Boolean','NaturalNum','List','Map',
       'TabularCPD','Categorical','Distribution','Gaussian']

  def gen_regex(ops):
    return "|".join(ops)

  tokens = {
    'root' : [
      (r'([a-zA-Z]+[0-9]*)(\()', bygroups(Name.Function, Punctuation)),
      ('('+gen_regex(types)+r')', Name.Class),
      ('('+gen_regex(keywords)+')\\b', Token.Keyword),
      (gen_regex(operators), Token.Operator),
      (r'(true|false|null)\b', Keyword.Constant),
      (r'([a-zA-Z_]\w*)\b', Name),
      (r'"(\\\\|\\"|[^"])*"', String),
      (gen_regex(deliminators), Punctuation),
      (r'\d+\.\d+', Number.Float),
      (r'\d+', Number.Integer),
      (r'//.*?\n', Comment.Single),
      (r'/\*.*?\*/', Comment.Multiline),
      (r'\s+', Text),
    ]
  }

def run_tests():
  tests = [
    "type Person;",
    "distinct Person Alice, Bob, P[100];",
    "random Real x ~ Gaussian(0, 1);\nrandom Real y ~ Gaussian(x, 1);",
    "random type0 funcname(type1 x) =expression;\nrandom type0 funcname(type1 x) dependency-expression;",
    "random NaturalNum x ~ Poisson(a);",
    "param Real a: 0 < a & a < 10 ;"
    "random Real funcname(type1 x);",
    "1.0 + 2.0 * 3.0 - 4.0",
    "Twice( 10.0 ) * 5.5",
    "fixed NaturalNum[] c = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];",
    "fixed NaturalNum[][] table = [1, 2, 3; 4, 5, 6];",
    "fixed List<NaturalNum> a = List(1, 2, 3, 4, 5, 6);",
    "fixed Map<Boolean, Real> map1 = {true -> 0.3, false -> 0.7};",
    "Categorical<Boolean> cpd1 =Categorical({true -> 0.3, false -> 0.7});",
    "List"
  ]
  lexer = BlogLexer()
  for test in tests:
    print(test)
    for token in (lexer.get_tokens(test)):
      print(token)

if __name__ == '__main__':
  run_tests()

