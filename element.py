class Element:
    def __init__(self, symbol, data, language):
        self.symbol = symbol
        self.A = data.get_info(symbol, 'A')
        self.Z = data.get_info(symbol, 'Z')
        self.B = data.get_info(symbol, 'BE/A') / 1000  # MeV
        self.name = data.list_elements(language)[self.Z]
        
