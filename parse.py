import pandas as pd
import pyparsing as pp

df = pd.read_csv("ftx_origin.csv")
 
# Define the grammar of the input string
float_num = pp.Regex(r'-?\d+\.\d+').setParseAction(lambda t: float(t[0]))
pair = pp.Group(pp.Word(pp.alphas + pp.nums + '_' + '-' + '.') + pp.Suppress('[') + float_num + pp.Suppress(']'))
grammar = pp.delimitedList(pair, delim=',')
 
# Parse the input string
input_str = 'NFT (371174812525093527)[1],TRX[0.0000560000000000],USD[0.0059561696228493]'
parsed_data = grammar.parseString(','.join([p for p in input_str.split(',') if not p.startswith('NFT')]))
 
# Convert the parsed data into a pandas series
data_dict = {pair[0]: pair[1] for pair in parsed_data}
series = pd.Series(data_dict)
 
print(series)
 
s_list = []
for data in df.iloc[:,1].items():
    # print(data)
    if type(data[1]) != float:
        if not data[1].endswith('NFT'):
            if not data[1].startswith('Token'):
                if not data[1].startswith('('):
                    # Convert the parsed data into a pandas series
                    parsed_data = grammar.parseString(','.join([p for p in data[1].replace("\n", "").replace(" ", "").split(',') if not p.startswith('NFT')]))
 
                    # Convert the parsed data into a pandas series
                    data_dict = {pair[0]: pair[1] for pair in parsed_data}
                    series = pd.Series(data_dict)
 
                    s_list.append(series)
 
full = pd.DataFrame(s_list)

full.to_csv("tmp.csv")