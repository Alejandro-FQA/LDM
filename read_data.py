import pandas as pd
import elements_diccionaries as eldic

class AtomicMassData:
    def __init__(self, filename='atomic_mass.txt'):
        self.df = pd.read_fwf(filename,    
                            usecols=(2, 3, 4, 6, 11),
                            names=['N', 'Z', 'A', 'Element', 'Experimental'],
                            widths=(1,3,5,5,5,1,3,4,1,14,12,13,1,10,1,2,13,11,1,3,1,13,12,1),
                            header=28, 
                            index_col=False)
        self.df['Experimental'] = pd.to_numeric(
            self.df['Experimental'].str.replace('#',''), errors='coerce'
        )
    
    def get_info(self, element, value=None):
        data = self.df[self.df['Element'] == element]
        if value is None:
            return data
        else:
            match value:
                case 'A':
                    return data.iloc[:,2].values
                case 'Z': 
                    return data.iloc[0,1]
                case 'BE/A':
                    return data.iloc[:,4].values    

    def list_elements(self, language=None):
        elements = self.df['Element'].unique()  # unique element symbols from DataFrame

        if language is None:
            return elements.tolist()

        # Dynamically get the appropriate dictionary
        dict_name = f"elements_{language}"
        if not hasattr(eldic, dict_name):
            raise ValueError(f"Unsupported language: {language}")

        element_dict = getattr(eldic, dict_name)

        # Build "Symbol - Name" list
        return [f"{el} - {element_dict.get(el, 'Unknown')}" for el in elements]
    

# Usage:
# data = AtomicMassData()
# carbon = data.get_element('O','BE/A')
# list_elements = data.list_elements()
# print(list_elements)

# print(element('Cs').name)
