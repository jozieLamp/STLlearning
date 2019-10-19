
class SymbolArray:
    def __init__(self):
        values = [] #size 16 array of doubles
        evolvingContinuously = [] #new boolean[16];
        names = [] #new ArrayList < String > (16);
        numberOfSymbols = 0
        symbolLookupTable = {} #new HashMap < String, Integer > ();
        initialValueExpression = [] #new ArrayList < Expression > (16);

