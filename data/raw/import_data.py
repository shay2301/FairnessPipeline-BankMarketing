from ucimlrepo import fetch_ucirepo 
  
bank_marketing = fetch_ucirepo(id=222) 
  
X = bank_marketing.data.features 
y = bank_marketing.data.targets 
  
print(bank_marketing.metadata) 
  
print(bank_marketing.variables) 
